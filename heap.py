import streamlit as st
from graphviz import Digraph
import time

st.set_page_config(page_title="Heap Sort Visualizer")

st.title("🌳 Heap & Heap Sort Visualizer")

# -----------------------------
# Draw Heap Tree
# -----------------------------
def draw_heap(arr, heap_size=None):
    dot = Digraph()

    if heap_size is None:
        heap_size = len(arr)

    for i in range(heap_size):
        dot.node(str(i), f"{arr[i]} ({i})")

    for i in range(heap_size):
        left = 2 * i + 1
        right = 2 * i + 2

        if left < heap_size:
            dot.edge(str(i), str(left))

        if right < heap_size:
            dot.edge(str(i), str(right))

    return dot


# -----------------------------
# Heapify Function
# -----------------------------
def heapify(arr, n, i, steps):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        steps.append(("Swap", arr.copy(), i, largest))
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, steps)


# -----------------------------
# Build Heap
# -----------------------------
def build_heap(arr):
    steps = []
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, steps)

    return steps


# -----------------------------
# Heap Sort
# -----------------------------
def heap_sort(arr):
    steps = []
    n = len(arr)

    build_heap(arr)

    for i in range(n - 1, 0, -1):
        steps.append(("Extract Max", arr.copy(), 0, i))
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, steps)

    return steps


# -----------------------------
# User Input
# -----------------------------
user_input = st.text_input(
    "Enter numbers separated by comma",
    "10,4,1,3,2"
)

if st.button("Run Heap Sort Visualization"):

    arr = [int(x.strip()) for x in user_input.split(",")]

    st.subheader("Initial Array")
    st.write(arr)
    st.graphviz_chart(draw_heap(arr))

    # Build Heap
    st.subheader("🔨 Building Max Heap")

    build_arr = arr.copy()
    steps = build_heap(build_arr)

    for action, state, i, j in steps:
        st.write(f"{action}: swap index {i} and {j}")
        st.write(state)
        st.graphviz_chart(draw_heap(state))
        time.sleep(0.5)

    st.success("Max Heap Built!")

    # Heap Sort
    st.subheader("🚀 Heap Sort Steps")

    sort_arr = arr.copy()
    steps = heap_sort(sort_arr)

    heap_size = len(sort_arr)

    for action, state, i, j in steps:
        heap_size -= 1

        st.write(f"{action}: swap index {i} and {j}")
        st.write(state)
        st.graphviz_chart(draw_heap(state, heap_size))
        time.sleep(0.5)

    st.success("Sorting Completed!")
    st.write("Sorted Array:", sorted(arr))