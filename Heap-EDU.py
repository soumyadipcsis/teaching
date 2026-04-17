import streamlit as st
import graphviz
import random
import time

st.set_page_config(layout="wide")
st.title("🧠 Heap Learning Lab — Interactive UG Studio")

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "heap" not in st.session_state:
    st.session_state.heap = []

if "mode" not in st.session_state:
    st.session_state.mode = "Min Heap"

# ---------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------
st.sidebar.header("⚙️ Heap Settings")

mode = st.sidebar.radio(
    "Choose Heap Type",
    ["Min Heap", "Max Heap"]
)

st.session_state.mode = mode

# ---------------------------------------------------
# HEAP HELPERS
# ---------------------------------------------------
def compare(a, b):
    if st.session_state.mode == "Min Heap":
        return a < b
    return a > b


def draw_heap(heap, highlight=None):
    dot = graphviz.Digraph()

    for i, val in enumerate(heap):
        color = "lightblue"
        if highlight == i:
            color = "yellow"

        dot.node(str(i), str(val), style="filled", fillcolor=color)

        l = 2*i+1
        r = 2*i+2

        if l < len(heap):
            dot.edge(str(i), str(l))
        if r < len(heap):
            dot.edge(str(i), str(r))

    return dot

# ---------------------------------------------------
# HEAPIFY UP (ANIMATED)
# ---------------------------------------------------
def heapify_up(heap, i):
    steps = []

    while i > 0:
        parent = (i-1)//2

        if compare(heap[i], heap[parent]):
            heap[i], heap[parent] = heap[parent], heap[i]
            steps.append(heap.copy())
            i = parent
        else:
            break

    return steps

# ---------------------------------------------------
# HEAPIFY DOWN (ANIMATED)
# ---------------------------------------------------
def heapify_down(heap, i):
    steps = []
    n = len(heap)

    while True:
        best = i
        l = 2*i+1
        r = 2*i+2

        if l < n and compare(heap[l], heap[best]):
            best = l
        if r < n and compare(heap[r], heap[best]):
            best = r

        if best != i:
            heap[i], heap[best] = heap[best], heap[i]
            steps.append(heap.copy())
            i = best
        else:
            break

    return steps

# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🏗 Heap Builder",
    "🔄 Heap Sort Animation",
    "🎮 Practice Game",
    "📘 Exercises"
])

# ===================================================
# TAB 1 — HEAP BUILDER
# ===================================================
with tab1:

    st.header("Heap Operations + Animation")

    col1, col2 = st.columns(2)

    with col1:
        val = st.number_input("Insert value", step=1)

        if st.button("Insert"):
            st.session_state.heap.append(val)
            steps = heapify_up(st.session_state.heap,
                               len(st.session_state.heap)-1)

            for s in steps:
                st.graphviz_chart(draw_heap(s))
                time.sleep(0.5)

    with col2:
        if st.button("Delete Root"):
            if st.session_state.heap:

                heap = st.session_state.heap
                heap[0] = heap[-1]
                heap.pop()

                steps = heapify_down(heap, 0)

                for s in steps:
                    st.graphviz_chart(draw_heap(s))
                    time.sleep(0.5)

    st.subheader("Array Representation")
    st.write(st.session_state.heap)

    if st.session_state.heap:
        st.graphviz_chart(draw_heap(st.session_state.heap))

# ===================================================
# TAB 2 — HEAP SORT ANIMATION
# ===================================================
with tab2:

    st.header("Step-by-Step Heap Sort")

    data = st.text_input(
        "Enter numbers",
        "7,2,9,1,5"
    )

    if st.button("Start Heap Sort"):

        arr = list(map(int, data.split(",")))
        heap = []

        st.write("Building Heap")

        for x in arr:
            heap.append(x)
            heapify_up(heap, len(heap)-1)
            st.graphviz_chart(draw_heap(heap))
            time.sleep(0.5)

        sorted_list = []

        st.write("Sorting Phase")

        while heap:
            sorted_list.append(heap[0])
            heap[0] = heap[-1]
            heap.pop()

            if heap:
                heapify_down(heap, 0)

            st.graphviz_chart(draw_heap(heap))
            time.sleep(0.5)

        st.success(f"Sorted Result: {sorted_list}")

# ===================================================
# TAB 3 — GAMIFIED PRACTICE
# ===================================================
with tab3:

    st.header("🎮 Heap Game")

    if "game_heap" not in st.session_state:
        st.session_state.game_heap = random.sample(range(1,50),5)

    st.write("Current Heap:")
    st.write(st.session_state.game_heap)

    guess = st.number_input("Guess Root Element")

    if st.button("Check Answer"):
        correct = min(st.session_state.game_heap) \
            if mode=="Min Heap" else max(st.session_state.game_heap)

        if guess == correct:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong! Correct = {correct}")

    if st.button("New Game"):
        st.session_state.game_heap = random.sample(range(1,50),5)

# ===================================================
# TAB 4 — EXERCISES
# ===================================================
with tab4:

    st.header("📘 Practice Exercises")

    exercises = [
        {
            "q":"Insert 10, 5, 20 into a Min Heap.",
            "steps":[
                "Insert 10 → root",
                "Insert 5 → swap with parent",
                "Insert 20 → no swap"
            ],
            "sol":"Final Heap: [5,10,20]"
        },
        {
            "q":"Delete root from Max Heap [30,20,10,5]",
            "steps":[
                "Replace root with last element",
                "Heapify down",
                "Swap with larger child"
            ],
            "sol":"Final Heap: [20,5,10]"
        }
    ]

    for ex in exercises:
        st.subheader("Problem")
        st.write(ex["q"])

        with st.expander("Possible Steps"):
            for s in ex["steps"]:
                st.write("•", s)

        with st.expander("Solution"):
            st.success(ex["sol"])

# ---------------------------------------------------
# EXAM QUESTION GENERATOR
# ---------------------------------------------------
st.sidebar.header("📝 Exam Question Generator")

if st.sidebar.button("Generate Question"):

    nums = random.sample(range(1,40),5)

    st.sidebar.write(
        f"Build a {mode} from: {nums}"
    )
    st.sidebar.write(
        "Show all heapify steps."
    )