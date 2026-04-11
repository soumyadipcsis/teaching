import streamlit as st
import time
import math

st.set_page_config(page_title="Heap Sort Visualizer (Fast)")

st.title("🌳 Heap & Heap Sort Visualizer (No Graphics)")

# -----------------------------
# Print Heap as Levels
# -----------------------------
def show_heap(arr, heap_size=None):
    if heap_size is None:
        heap_size = len(arr)

    levels = int(math.log2(heap_size)) + 1 if heap_size > 0 else 0

    index = 0
    for level in range(levels):
        nodes = 2 ** level
        row = []

        for _ in range(nodes):
            if index < heap_size:
                row.append(f"{arr[index]}({index})")
                index += 1

        st.write("   ".join(row))


# -----------------------------
# Heapify
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

speed = st.slider("Animation Speed", 0.0, 1.0, 0.2)

if st.button("Run Heap Sort"):

    arr = [int(x.strip()) for x in user_input.split(",")]

    st.subheader("Initial Array")
    st.write(arr)
    show_heap(arr)

    # -------------------------
    # Build Heap
    # -------------------------
    st.subheader("🔨 Building Max Heap")

    build_arr = arr.copy()
    steps = build_heap(build_arr)

    placeholder = st.empty()

    for action, state, i, j in steps:
        with placeholder.container():
            st.write(f"{action}: swap index {i} and {j}")
            st.write(state)
            show_heap(state)

        time.sleep(speed)

    st.success("Max Heap Built!")

    # -------------------------
    # Heap Sort
    # -------------------------
    st.subheader("🚀 Heap Sort Steps")

    sort_arr = arr.copy()
    steps = heap_sort(sort_arr)

    heap_size = len(sort_arr)

    for action, state, i, j in steps:
        heap_size -= 1

        with placeholder.container():
            st.write(f"{action}: swap index {i} and {j}")
            st.write(state)
            show_heap(state[:heap_size])

        time.sleep(speed)

    st.success("Sorting Completed!")
    st.write("Sorted Array:", sorted(arr))