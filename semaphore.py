import os, textwrap, zipfile


import streamlit as st
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional

st.set_page_config(page_title="Process Synchronization Lab", page_icon="🔄", layout="wide")

st.title("🔄 Process Synchronization Lab")
st.caption("An interactive Operating Systems learning app for undergraduate students")
st.markdown("""
Explore **race conditions, critical sections, locks, mutexes, condition variables, and semaphores**.
Each topic includes an intuition, a visual trace, code patterns, worked examples, and practice problems.
""")

with st.sidebar:
    st.header("Learning path")
    page = st.radio("Choose a lab", [
        "Start here", "Race condition & critical section", "Locks and mutexes",
        "Condition variables", "Semaphores", "Classic synchronization problems",
        "Practice problems", "Quick revision"
    ])
    st.divider()
    st.info("Tip: Run a demo, inspect the execution trace, then explain why each operation is safe or unsafe.")

def code_block(code, language="python"):
    st.code(textwrap.dedent(code).strip(), language=language)

def trace_table(rows):
    st.dataframe(rows, use_container_width=True, hide_index=True)

if page == "Start here":
    st.header("1. Why do processes need synchronization?")
    st.write("A process or thread may be paused at almost any instruction. If two threads access shared data without coordination, their operations can interleave and produce an incorrect result.")
    c1,c2,c3 = st.columns(3)
    c1.metric("Shared resource", "Common data")
    c2.metric("Main risk", "Race condition")
    c3.metric("Goal", "Correct coordination")
    st.subheader("Core vocabulary")
    terms = [
        ("Concurrency", "Multiple tasks make progress during overlapping time periods."),
        ("Race condition", "The result depends on the unpredictable order of execution."),
        ("Critical section", "Code that accesses shared state and must obey a coordination rule."),
        ("Mutual exclusion", "At most one thread is in a protected critical section at a time."),
        ("Deadlock", "Tasks wait forever for resources held by one another."),
        ("Starvation", "A task waits indefinitely because others keep getting service.")
    ]
    for term, desc in terms:
        with st.expander(term):
            st.write(desc)
    st.subheader("The main tools at a glance")
    st.table([
        {"Tool":"Lock / Mutex","Mental model":"One key for one room","Typical use":"Protect a shared variable or data structure"},
        {"Tool":"Condition variable","Mental model":"Wait until a condition becomes true","Typical use":"Producer-consumer coordination"},
        {"Tool":"Semaphore","Mental model":"A counter of permits","Typical use":"Limit access to N identical resources"}
    ])
    st.warning("A lock protects a critical section. A condition variable lets a thread sleep until a predicate may have changed. A semaphore manages permits; it is not simply another name for a mutex.")

elif page == "Race condition & critical section":
    st.header("2. Race condition and critical section")
    st.write("Suppose two threads each increment a shared counter once. The high-level statement `counter += 1` is usually a read-modify-write sequence.")
    st.latex(r" counter \leftarrow counter + 1")
    st.subheader("Interactive interleaving demo")
    initial = st.number_input("Initial counter", min_value=0, max_value=100, value=0, step=1)
    schedule = st.selectbox("Choose an execution order", [
        "Unsafe: both read before either writes",
        "Safe: Thread A completes, then Thread B",
        "Safe: Thread B completes, then Thread A"
    ])
    if st.button("Run counter example", type="primary"):
        if schedule.startswith("Unsafe"):
            rows = [
                {"Step":1,"Thread":"A","Operation":"read counter","Local value":initial,"Shared counter":initial},
                {"Step":2,"Thread":"B","Operation":"read counter","Local value":initial,"Shared counter":initial},
                {"Step":3,"Thread":"A","Operation":"add 1 locally","Local value":initial+1,"Shared counter":initial},
                {"Step":4,"Thread":"B","Operation":"add 1 locally","Local value":initial+1,"Shared counter":initial},
                {"Step":5,"Thread":"A","Operation":"write local value","Local value":initial+1,"Shared counter":initial+1},
                {"Step":6,"Thread":"B","Operation":"write local value","Local value":initial+1,"Shared counter":initial+1},
            ]
            result = initial+1
            st.error(f"Lost update! Expected {initial+2}, but got {result}.")
        else:
            first = "A" if "Thread A" in schedule else "B"
            second = "B" if first == "A" else "A"
            rows=[]
            value=initial
            step=1
            for thread in [first,second]:
                rows += [
                    {"Step":step,"Thread":thread,"Operation":"read counter","Local value":value,"Shared counter":value},
                    {"Step":step+1,"Thread":thread,"Operation":"increment and write","Local value":value+1,"Shared counter":value+1}
                ]
                value += 1; step += 2
            result=value
            st.success(f"Correct result: {result}. Both increments are preserved.")
        trace_table(rows)
        st.metric("Final counter", result)
    st.subheader("What makes a good critical-section solution?")
    st.markdown("""
    1. **Mutual exclusion:** at most one thread executes the critical section.
    2. **Progress:** if the critical section is free, choosing who enters should not be postponed forever.
    3. **Bounded waiting:** a thread should not wait forever while others repeatedly enter.
    """)
    code_block("""
    # Pseudocode
    acquire(lock)
    # critical section: read/update shared state
    release(lock)
    # remainder section
    """)

elif page == "Locks and mutexes":
    st.header("3. Locks and mutexes")
    st.write("A mutex (mutual exclusion lock) has an owner: a thread locks it before entering and unlocks it after leaving.")
    st.subheader("Lock-state simulator")
    if "lock_held" not in st.session_state: st.session_state.lock_held=False
    if "lock_owner" not in st.session_state: st.session_state.lock_owner="None"
    a,b = st.columns(2)
    with a:
        if st.button("Thread A: acquire"):
            if not st.session_state.lock_held:
                st.session_state.lock_held=True; st.session_state.lock_owner="A"
                st.success("Thread A acquired the mutex.")
            else: st.warning(f"Thread A blocks: mutex is owned by Thread {st.session_state.lock_owner}.")
        if st.button("Thread A: release"):
            if st.session_state.lock_held and st.session_state.lock_owner=="A":
                st.session_state.lock_held=False; st.session_state.lock_owner="None"
                st.success("Thread A released the mutex.")
            else: st.error("Thread A cannot release a mutex it does not own.")
    with b:
        if st.button("Thread B: acquire"):
            if not st.session_state.lock_held:
                st.session_state.lock_held=True; st.session_state.lock_owner="B"
                st.success("Thread B acquired the mutex.")
            else: st.warning(f"Thread B blocks: mutex is owned by Thread {st.session_state.lock_owner}.")
        if st.button("Thread B: release"):
            if st.session_state.lock_held and st.session_state.lock_owner=="B":
                st.session_state.lock_held=False; st.session_state.lock_owner="None"
                st.success("Thread B released the mutex.")
            else: st.error("Thread B cannot release a mutex it does not own.")
    st.metric("Mutex state", "LOCKED" if st.session_state.lock_held else "UNLOCKED")
    st.write("Owner:", st.session_state.lock_owner)
    if st.button("Reset mutex"):
        st.session_state.lock_held=False; st.session_state.lock_owner="None"
        st.rerun()
    st.subheader("Python example")
    code_block("""
    import threading

    counter = 0
    mutex = threading.Lock()

    def increment():
        global counter
        for _ in range(1000):
            with mutex:          # acquire on entry, release on exit
                counter += 1

    # Start two threads running increment().
    # Expected final counter: 2000
    """)
    st.info("Use `with mutex:` so the lock is released even if an exception occurs. Keep the critical section as short as possible.")
    st.subheader("Common mistakes")
    st.table([
        {"Mistake":"Forgetting to unlock","Consequence":"Other threads may block forever"},
        {"Mistake":"Locking twice with a non-reentrant lock","Consequence":"The same thread may deadlock"},
        {"Mistake":"Different lock order in different threads","Consequence":"Possible deadlock"},
        {"Mistake":"Doing slow I/O while holding a lock","Consequence":"Unnecessary contention"}
    ])

elif page == "Condition variables":
    st.header("4. Condition variables")
    st.write("A condition variable lets a thread sleep until some shared-state predicate may have become true. The predicate is checked while holding a mutex.")
    st.subheader("Producer-consumer: one-slot buffer")
    if "buffer_item" not in st.session_state: st.session_state.buffer_item=None
    x,y = st.columns(2)
    with x:
        st.write("**Producer**")
        item = st.text_input("Item to produce", value="message", key="produce_item")
        if st.button("Produce item"):
            if st.session_state.buffer_item is None:
                st.session_state.buffer_item=item
                st.success("Item placed in the buffer.")
            else: st.warning("Buffer is full. Producer must wait.")
    with y:
        st.write("**Consumer**")
        if st.button("Consume item"):
            if st.session_state.buffer_item is not None:
                st.success(f"Consumed: {st.session_state.buffer_item}")
                st.session_state.buffer_item=None
            else: st.warning("Buffer is empty. Consumer must wait.")
    st.metric("Buffer status", "FULL" if st.session_state.buffer_item is not None else "EMPTY")
    st.write("Current item:", st.session_state.buffer_item if st.session_state.buffer_item is not None else "—")
    if st.button("Reset buffer"):
        st.session_state.buffer_item=None; st.rerun()
    st.subheader("Correct condition-variable pattern")
    code_block("""
    # Shared: mutex, condition variable cv, and boolean/item state

    # Consumer
    with mutex:
        while buffer_is_empty():
            cv.wait()       # atomically releases mutex and sleeps;
                            # reacquires mutex before returning
        item = remove_item()

    # Producer
    with mutex:
        add_item()
        cv.notify()         # wake one waiter; notify_all() wakes all
    """)
    st.warning("Use `while`, not `if`: wakeups can be spurious, and another thread may change the condition before the awakened thread reacquires the mutex.")
    st.markdown("**Important:** notification is not the condition. The shared predicate (for example, `buffer_is_empty()`) is the condition.")

elif page == "Semaphores":
    st.header("5. Semaphores")
    st.write("A semaphore is an integer-like synchronization object. `wait()` (also called P/down) takes a permit; `signal()` (also called V/up) returns a permit.")
    initial = st.slider("Initial semaphore permits", 0, 5, 2)
    if "sem_count" not in st.session_state: st.session_state.sem_count=initial
    if st.button("Reset semaphore to selected initial value"):
        st.session_state.sem_count=initial
    p,q = st.columns(2)
    with p:
        if st.button("wait() / P / acquire"):
            if st.session_state.sem_count>0:
                st.session_state.sem_count-=1
                st.success("Permit acquired.")
            else: st.warning("No permit available: caller would block.")
    with q:
        if st.button("signal() / V / release"):
            st.session_state.sem_count+=1
            st.success("Permit released.")
    st.metric("Available permits", st.session_state.sem_count)
    st.write("Interpretation:", "A new task can enter if at least one permit is available.")
    st.subheader("Binary vs counting semaphore")
    st.table([
        {"Type":"Binary semaphore","Initial value":"Usually 0 or 1","Use":"Simple signaling or binary resource control"},
        {"Type":"Counting semaphore","Initial value":"N","Use":"Allow up to N concurrent users of a resource"}
    ])
    st.subheader("Example: parking lot with 3 spaces")
    st.write("The semaphore starts at 3. Each arriving car performs `wait()`. Each departing car performs `signal()`.")
    code_block("""
    spaces = threading.Semaphore(3)

    def park_car():
        spaces.acquire()     # wait for a free space
        try:
            park()
        finally:
            spaces.release() # return the space
    """)
    st.subheader("Example: ordering two tasks")
    code_block("""
    done = threading.Semaphore(0)

    def task_a():
        do_first_part()
        done.release()       # announce completion

    def task_b():
        done.acquire()       # wait until A signals
        do_second_part()
    """)
    st.info("A semaphore is not automatically owned by the thread that decremented it. A mutex normally has ownership semantics.")

elif page == "Classic synchronization problems":
    st.header("6. Classic synchronization problems")
    topic = st.selectbox("Choose a problem", ["Producer-consumer (bounded buffer)", "Readers-writers", "Dining philosophers", "Sleeping barber"])
    if topic.startswith("Producer"):
        st.markdown("**Problem:** producers insert items into a finite buffer; consumers remove them. Prevent overflow, underflow, and data races.")
        code_block("""
        mutex = Lock()
        empty = Semaphore(N)   # N empty slots
        full  = Semaphore(0)   # initially no full slots

        # Producer
        item = produce()
        empty.acquire()
        with mutex:
            insert(item)
        full.release()

        # Consumer
        full.acquire()
        with mutex:
            item = remove()
        empty.release()
        consume(item)
        """)
        st.caption("The order matters: reserve a slot/item before touching the shared buffer.")
    elif topic == "Readers-writers":
        st.markdown("**Problem:** many readers may read together, but a writer needs exclusive access.")
        code_block("""
        # One common reader-preference sketch
        read_count = 0
        count_lock = Lock()
        room_empty = Semaphore(1)

        # Reader entry
        with count_lock:
            read_count += 1
            if read_count == 1:
                room_empty.acquire()
        read_data()
        with count_lock:
            read_count -= 1
            if read_count == 0:
                room_empty.release()

        # Writer
        room_empty.acquire()
        write_data()
        room_empty.release()
        """)
        st.warning("This reader-preference design can starve writers. Fairness requires a policy such as a turnstile or fair read-write lock.")
    elif topic == "Dining philosophers":
        st.markdown("**Problem:** five philosophers alternate thinking and eating. Each needs two neighboring forks. Naively taking the left fork first can deadlock.")
        code_block("""
        # One simple deadlock-avoidance idea:
        # Allow at most N-1 philosophers to compete for forks.
        room = Semaphore(4)  # for five philosophers

        def philosopher(left, right):
            while True:
                think()
                room.acquire()
                left.acquire()
                right.acquire()
                eat()
                right.release()
                left.release()
                room.release()
        """)
        st.info("Other solutions include resource ordering, a waiter/arbitrator, or asymmetric fork acquisition.")
    else:
        st.markdown("**Problem:** customers arrive for a barber. If no customer is waiting, the barber sleeps; a waiting customer wakes the barber.")
        code_block("""
        customers = Semaphore(0)
        barber_ready = Semaphore(0)
        seats = Semaphore(N)

        # Customer
        if try_to_claim_waiting_seat():
            customers.release()
            barber_ready.acquire()
            get_haircut()
        else:
            leave_shop()

        # Barber
        while True:
            customers.acquire()
            barber_ready.release()
            cut_hair()
        """)
        st.caption("This is a conceptual sketch; a complete implementation must protect the waiting-chair count with a mutex.")

elif page == "Practice problems":
    st.header("7. Practice problems")
    problems = [
        ("Q1 · Lost update", "Two threads each execute `x = x + 1` once. Both read x=10 before either writes. What final value can occur?", ["10","11","12","13"], "11", "Both compute 11 and one write overwrites the other. This is a lost update."),
        ("Q2 · Mutex", "What is the main purpose of a mutex?", ["Count free resources","Ensure mutual exclusion","Wake every sleeping thread","Store a condition"], "Ensure mutual exclusion", "A mutex protects a critical section so only its owner enters at a time."),
        ("Q3 · Condition variable", "Why should a condition-variable wait normally be inside a while loop?", ["To use less memory","To avoid acquiring a mutex","Because wakeups do not guarantee the predicate is true","To make notification permanent"], "Because wakeups do not guarantee the predicate is true", "Spurious wakeups and competition mean the predicate must be rechecked."),
        ("Q4 · Semaphore", "A counting semaphore starts at 4. Three successful wait operations occur and one signal occurs. What is its value?", ["0","1","2","4"], "2", "4 - 3 + 1 = 2 permits."),
        ("Q5 · Deadlock", "Which situation is a deadlock?", ["A thread waits briefly","Two threads each hold one lock and wait for the other's lock","A thread releases a lock","A semaphore has value 1"], "Two threads each hold one lock and wait for the other's lock", "This is circular wait with hold-and-wait."),
        ("Q6 · Producer-consumer", "In a bounded-buffer solution, what does `empty` count?", ["Items currently in buffer","Available empty slots","Number of consumers","Number of locks"], "Available empty slots", "The empty semaphore starts at the buffer capacity.")
    ]
    if "answers" not in st.session_state: st.session_state.answers={}
    for i,(title,question,opts,correct,explain) in enumerate(problems):
        with st.expander(title, expanded=(i==0)):
            st.write(question)
            choice=st.radio("Choose one answer",opts,key=f"q{i}")
            if st.button("Check answer",key=f"check{i}"):
                st.session_state.answers[i]=(choice==correct)
                if choice==correct: st.success("Correct!")
                else: st.error(f"Not quite. Correct answer: {correct}")
                st.caption(explain)
    if st.button("Show score"):
        score=sum(1 for v in st.session_state.answers.values() if v)
        st.metric("Correct answers checked", f"{score} / {len(problems)}")
    st.subheader("Short-answer / discussion questions")
    st.markdown("""
    1. Give an example of a race condition from a banking application.
    2. Explain the difference between a mutex and a counting semaphore.
    3. What can go wrong if a condition-variable wait uses `if` instead of `while`?
    4. Construct a deadlock with two threads and two locks. Then fix it using lock ordering.
    5. Design synchronization for a printer pool containing four printers.
    6. Explain why notifying a condition variable without changing the shared predicate is often a bug.
    7. Can a program be free of race conditions and still deadlock? Explain.
    """)

else:
    st.header("8. Quick revision")
    st.table([
        {"Concept":"Lock / mutex","Key operation":"lock / unlock","Question to ask":"Who owns the critical section?"},
        {"Concept":"Condition variable","Key operation":"wait / notify","Question to ask":"What predicate am I waiting for?"},
        {"Concept":"Semaphore","Key operation":"wait / signal","Question to ask":"How many permits are available?"},
        {"Concept":"Deadlock","Key idea":"Circular waiting","Prevention idea":"Break at least one necessary condition"},
        {"Concept":"Starvation","Key idea":"Unfair progress","Prevention idea":"Use fair scheduling / queueing"}
    ])
    st.subheader("Four conditions for deadlock (Coffman conditions)")
    st.markdown("""
    - **Mutual exclusion:** at least one resource is non-shareable.
    - **Hold and wait:** a process holds a resource while requesting another.
    - **No preemption:** resources cannot be forcibly taken away.
    - **Circular wait:** a cycle exists in the resource-wait graph.

    Breaking any one of these conditions prevents deadlock.
    """)
    st.subheader("Exit ticket")
    st.write("In one sentence each, explain when you would choose a mutex, a condition variable, and a counting semaphore.")

st.divider()
st.caption("Process Synchronization Lab · Teaching aid. Code snippets are instructional patterns; adapt error handling and fairness guarantees before using in production.")
