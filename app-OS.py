import streamlit as st
import time

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="OS Process Playground",
    page_icon="🖥️",
    layout="wide",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #666;
        margin-bottom: 1.2rem;
    }

    .card {
        padding: 1rem 1.2rem;
        border-radius: 14px;
        border: 1px solid #ddd;
        background: #fafafa;
        margin-bottom: 0.8rem;
    }

    .process {
        display: inline-block;
        padding: 12px 20px;
        border: 2px solid #555;
        border-radius: 12px;
        margin: 6px;
        text-align: center;
        background: white;
        min-width: 120px;
    }

    .parent {
        border-color: #1565c0;
    }

    .child {
        border-color: #2e7d32;
    }

    .zombie {
        border-color: #c62828;
        background: #fff5f5;
    }

    .arrow {
        font-size: 1.6rem;
        text-align: center;
        margin: 8px;
    }

    .big-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 10px 0;
    }

    .small-note {
        color: #666;
        font-size: 0.9rem;
    }

    .concept {
        padding: 15px;
        border-radius: 12px;
        background: #f7f7f7;
        border: 1px solid #ddd;
        min-height: 140px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🖥️ OS Process Playground</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
    Interactive demonstrations of
    <b>fork(), exec(), exit(), wait(), process trees,
    zombies, orphans, shell execution, pipes, and I/O redirection.</b>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🎛️ Select a Demo")

demo = st.sidebar.radio(
    "Choose a topic",
    [
        "🏠 Overview",
        "🌳 fork() Process Tree",
        "🧠 fork() + Memory",
        "🔢 Nested fork()",
        "⏳ fork() + wait()",
        "🔄 fork() + exec()",
        "☠️ Zombie vs Orphan",
        "🐚 Mini Shell",
        "➡️ I/O Redirection",
        "🔗 Pipes",
        "🎯 Predict Before You Run",
    ],
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    **OS LAB • UG**

    Process API & System Calls

    **Teaching strategy**

    1. Predict
    2. Visualize
    3. Run
    4. Explain
    """
)

# ============================================================
# OVERVIEW
# ============================================================

if demo == "🏠 Overview":

    st.subheader("🎓 OS Process API Playground")

    st.write(
        """
        This interactive playground helps students understand how an operating
        system creates, executes, synchronizes, and terminates processes.
        """
    )

    cols = st.columns(4)

    concepts = [
        ("fork()", "CREATE", "Creates a new child process."),
        ("exec()", "REPLACE", "Replaces the current program image."),
        ("exit()", "FINISH", "Terminates the process."),
        ("wait()", "COLLECT", "Parent waits and reaps a child."),
    ]

    for col, (name, action, description) in zip(cols, concepts):

        with col:

            st.markdown(
                f"""
                <div class="concept">
                    <h3>{name}</h3>
                    <b>{action}</b>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    st.info(
        "💡 Teaching idea: Ask students to predict first, "
        "run the simulation second, and explain why third."
    )

    st.subheader("🧠 Mental Model")

    st.code(
        """
fork()  → create a new process

exec()  → replace program

exit()  → process terminates

wait()  → parent waits/reaps

--------------------------------

Typical shell execution:

User command
     ↓
   shell
     ↓
   fork()
     ↓
   child
     ↓
   exec()
     ↓
  program
     ↓
   exit()
     ↓
   wait()
     ↓
 shell prompt
        """,
        language="text",
    )

    st.success(
        "The goal is to connect individual system calls to the complete "
        "process lifecycle."
    )

# ============================================================
# FORK PROCESS TREE
# ============================================================

elif demo == "🌳 fork() Process Tree":

    st.subheader("🌳 fork() Process Tree")

    st.write(
        "A process calls fork(). The operating system creates a new child process."
    )

    col1, col2 = st.columns([1, 2])

    with col1:

        parent_pid = st.number_input(
            "Parent PID",
            min_value=1,
            value=1000,
            step=1,
        )

        if st.button("🚀 Run fork()", type="primary"):

            st.session_state["fork_done"] = True

    if st.session_state.get("fork_done", False):

        child_pid = parent_pid + 1

        with col2:

            st.markdown("### After fork()")

            st.markdown(
                f"""
                <div style="text-align:center">

                    <div class="process parent">
                        👨 <b>Parent</b><br>
                        PID = {parent_pid}<br>
                        fork() returns {child_pid}
                    </div>

                    <div class="arrow">
                        ↙️ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ↘️
                    </div>

                    <div class="process parent">
                        👨 Parent<br>
                        continues
                    </div>

                    <div class="process child">
                        👶 <b>Child</b><br>
                        PID = {child_pid}<br>
                        fork() returns 0
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            st.success(
                "Two processes now exist. Both continue executing from "
                "the point immediately after fork()."
            )

            st.subheader("C Code")

            st.code(
                """
int ret = fork();

if (ret == 0) {

    // Child

}
else {

    // Parent

}
                """,
                language="c",
            )

            st.info(
                "Remember: fork() returns 0 to the child and the child's PID "
                "to the parent."
            )

# ============================================================
# FORK + MEMORY
# ============================================================

elif demo == "🧠 fork() + Memory":

    st.subheader("🧠 fork() Creates Independent Memory Copies")

    x = st.number_input(
        "Initial value of x",
        value=10,
        step=1,
    )

    st.code(
        f"""
int x = {x};

int ret = fork();

if (ret == 0) {{

    x = x + 1;
    printf("Child: %d\\n", x);

}} else {{

    x = x - 1;
    printf("Parent: %d\\n", x);

}}
        """,
        language="c",
    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("### 👨 Parent")

        st.metric("Initial x", x)

        st.metric(
            "After x = x - 1",
            x - 1,
        )

    with c2:

        st.markdown("### 👶 Child")

        st.metric("Initial x", x)

        st.metric(
            "After x = x + 1",
            x + 1,
        )

    st.success(
        f"Parent gets x = {x - 1}, while Child gets x = {x + 1}."
    )

    st.info(
        "💡 Each process has its own logical memory space. "
        "Changing x in one process does not directly change x in the other."
    )

# ============================================================
# NESTED FORK
# ============================================================

elif demo == "🔢 Nested fork()":

    st.subheader("🔢 Nested fork(): How Many Processes?")

    n = st.slider(
        "Number of sequential fork() calls",
        min_value=1,
        max_value=6,
        value=2,
    )

    processes = 2 ** n

    st.markdown(
        f"""
        <div class="big-number">
        {processes} processes
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        f"Formula: 2ⁿ = 2^{n} = **{processes}**"
    )

    st.code(
        "\n".join(
            ["fork();" for _ in range(n)]
        ),
        language="c",
    )

    if st.button(
        "🌳 Show Process Expansion",
        type="primary",
    ):

        level = ["P0"]

        st.markdown("### Process Expansion")

        for i in range(n):

            new_level = []

            for process in level:

                new_level.append(process + "₀")
                new_level.append(process + "₁")

            level = new_level

            st.write(
                f"After fork {i + 1}: "
                f"**{len(level)} processes**"
            )

            display = "   ".join(level[:32])

            if len(level) > 32:

                display += " ..."

            st.code(display)

    st.warning(
        "⚠️ Assuming every fork() succeeds and the fork() calls are "
        "executed sequentially by all existing processes."
    )

# ============================================================
# WAIT
# ============================================================

elif demo == "⏳ fork() + wait()":

    st.subheader("⏳ fork() + wait(): Synchronization")

    use_wait = st.checkbox(
        "Parent calls wait()",
        value=True,
    )

    if use_wait:

        code = """
fork();

if (child) {

    work();
    exit();

}
else {

    wait();
    printf("Parent continues\\n");

}
        """

    else:

        code = """
fork();

if (child) {

    work();
    exit();

}
else {

    printf("Parent continues\\n");

}
        """

    st.code(code, language="c")

    if st.button(
        "▶️ Simulate Execution",
        type="primary",
    ):

        box = st.empty()

        if use_wait:

            events = [
                "👨 Parent: fork()",
                "👶 Child: running",
                "👶 Child: working...",
                "👶 Child: exit()",
                "👨 Parent: wait() returns",
                "👨 Parent: continues",
            ]

        else:

            events = [
                "👨 Parent: fork()",
                "👶 Child: running",
                "👨 Parent: may continue",
                "👶 Child: working...",
                "👶 Child: exit()",
            ]

        for event in events:

            box.info("▶ " + event)

            time.sleep(0.6)

    if use_wait:

        st.success(
            "wait() blocks the parent until a child terminates "
            "and can be reaped."
        )

    else:

        st.warning(
            "Without wait(), parent and child may execute in "
            "different orders depending on scheduling."
        )

# ============================================================
# EXEC
# ============================================================

elif demo == "🔄 fork() + exec()":

    st.subheader("🔄 fork() + exec(): Same Process, New Program")

    program = st.selectbox(
        "Select program",
        [
            "ls",
            "echo",
            "cat",
        ],
    )

    st.markdown("### Before exec()")

    st.code(
        """
Child Process

┌──────────────────────┐
│ Original Program     │
│                      │
│ code                 │
│ data                 │
│ stack                │
└──────────────────────┘
        """,
        language="text",
    )

    if st.button(
        "🔄 Call exec()",
        type="primary",
    ):

        st.markdown("### After successful exec()")

        st.code(
            f"""
Same Process

┌──────────────────────┐
│ {program}             │
│                      │
│ new program image    │
│ new code/data/stack  │
└──────────────────────┘
            """,
            language="text",
        )

        st.success(
            "exec() replaces the old program image with the new executable."
        )

        st.info(
            "Important: exec() normally does not create another process. "
            "The PID remains associated with the same process."
        )

# ============================================================
# ZOMBIE / ORPHAN
# ============================================================

elif demo == "☠️ Zombie vs Orphan":

    st.subheader("☠️ Zombie vs Orphan")

    scenario = st.radio(
        "Choose a scenario",
        [
            "Zombie",
            "Orphan",
        ],
        horizontal=True,
    )

    if scenario == "Zombie":

        st.markdown(
            """
            <div style="text-align:center">

                <div class="process parent">
                    👨 Parent<br>
                    RUNNING
                </div>

                <div class="arrow">
                    │<br>
                    │ Child exits<br>
                    ▼
                </div>

                <div class="process zombie">
                    ☠️ Child<br>
                    ZOMBIE
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.error(
            "The child has terminated, but the parent has not yet "
            "called wait()."
        )

        if st.button(
            "👨 Parent calls wait()",
            type="primary",
        ):

            st.success(
                "Zombie has been reaped. Its remaining process-table "
                "information can now be cleaned up."
            )

    else:

        st.markdown(
            """
            <div style="text-align:center">

                <div class="process zombie">
                    ☠️ Parent<br>
                    TERMINATES
                </div>

                <div class="arrow">
                    │<br>
                    ▼
                </div>

                <div class="process child">
                    👶 Child<br>
                    STILL RUNNING
                </div>

                <div class="arrow">
                    │<br>
                    ▼
                </div>

                <div class="process parent">
                    🏠 System<br>
                    ADOPTS CHILD
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info(
            "An orphan is a child whose parent terminates while "
            "the child is still running."
        )

    st.divider()

    st.markdown("### Quick Comparison")

    comparison = """
Zombie:
Child exits first → Parent is alive → wait() not called

Orphan:
Parent exits first → Child is still running
"""

    st.code(comparison)

# ============================================================
# MINI SHELL
# ============================================================

elif demo == "🐚 Mini Shell":

    st.subheader("🐚 Mini Shell: fork → exec → exit → wait")

    command = st.selectbox(
        "Choose a command",
        [
            "echo hello",
            "ls",
            "pwd",
            "date",
            "cat notes.txt",
        ],
    )

    if st.button(
        "▶️ Run Command",
        type="primary",
    ):

        executable = command.split()[0]

        steps = [
            (
                "1️⃣ Read Command",
                f"$ {command}",
            ),
            (
                "2️⃣ fork()",
                "Shell creates a child process.",
            ),
            (
                "3️⃣ exec()",
                f"Child loads the executable: {executable}",
            ),
            (
                "4️⃣ Program Runs",
                f"{executable} executes.",
            ),
            (
                "5️⃣ exit()",
                "Child process terminates.",
            ),
            (
                "6️⃣ wait()",
                "Shell waits/reaps the child.",
            ),
            (
                "7️⃣ Prompt",
                "Shell displays the prompt again.",
            ),
        ]

        for title, text in steps:

            st.markdown(f"### {title}")

            st.write(text)

            time.sleep(0.25)

        st.success(
            f"$ {command}\n\nCommand completed."
        )

    st.divider()

    st.markdown("### Shell Mental Model")

    st.code(
        """
User
 │
 │ command
 ▼
Shell
 │
 │ fork()
 ▼
Child
 │
 │ exec()
 ▼
Program
 │
 │ exit()
 ▼
Child terminates
 │
 │ wait()
 ▼
Shell
 │
 ▼
Prompt
        """,
        language="text",
    )

# ============================================================
# I/O REDIRECTION
# ============================================================

elif demo == "➡️ I/O Redirection":

    st.subheader("➡️ I/O Redirection")

    st.write(
        "The shell can redirect standard output from the terminal to a file."
    )

    st.code(
        "ls > foo.txt",
        language="bash",
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("### 🖥️ Normal Output")

        st.code(
            """
ls
 │
 │ STDOUT (1)
 ▼
Screen
            """,
            language="text",
        )

    with c2:

        st.markdown("### 📄 Redirected Output")

        st.code(
            """
ls
 │
 │ STDOUT (1)
 ▼
foo.txt
            """,
            language="text",
        )

    if st.button(
        "➡️ Simulate Redirection",
        type="primary",
    ):

        st.success(
            "The shell arranges for the command's standard output "
            "to be written to foo.txt."
        )

    st.divider()

    st.markdown("### Useful Examples")

    st.code(
        """
ls > output.txt

cat output.txt

echo Hello > message.txt

echo World >> message.txt
        """,
        language="bash",
    )

# ============================================================
# PIPES
# ============================================================

elif demo == "🔗 Pipes":

    st.subheader("🔗 Pipes: stdout → stdin")

    left = st.selectbox(
        "Process A",
        [
            "ls",
            "cat",
        ],
    )

    right = st.selectbox(
        "Process B",
        [
            "grep txt",
            "grep py",
            "grep c",
        ],
    )

    st.markdown(
        f"""
        <div style="text-align:center">

            <div class="process parent">
                Process A<br>
                <b>{left}</b><br>
                STDOUT
            </div>

            <span style="font-size:2rem">
                ➡️
            </span>

            <div class="process child">
                KERNEL PIPE<br>
                communication
            </div>

            <span style="font-size:2rem">
                ➡️
            </span>

            <div class="process parent">
                Process B<br>
                <b>{right}</b><br>
                STDIN
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.code(
        f"$ {left} | {right}",
        language="bash",
    )

    st.info(
        "The output of Process A becomes the input of Process B."
    )

    if st.button(
        "🔗 Show Data Flow",
        type="primary",
    ):

        data = [
            "lecture.pdf",
            "notes.txt",
            "process.txt",
            "image.png",
            "hello.c",
            "fork.c",
            "program.py",
        ]

        st.write("### Process A produces:")

        st.code(
            "\n".join(data)
        )

        keyword = right.split()[-1]

        result = [
            item
            for item in data
            if keyword in item
        ]

        st.write(
            f"### Process B ({right}) receives:"
        )

        if result:

            st.code(
                "\n".join(result)
            )

        else:

            st.code("(no matching lines)")

# ============================================================
# QUIZ
# ============================================================

elif demo == "🎯 Predict Before You Run":

    st.subheader("🎯 Predict Before You Run")

    st.write(
        "First make your prediction. Then click **Reveal Answer**."
    )

    question = st.selectbox(
        "Question",
        [
            "Two sequential fork() calls: how many processes?",
            "What does fork() return in the child?",
            "What does the parent receive from fork()?",
            "Why can wait() make execution order predictable?",
            "What happens after a successful exec()?",
            "What is a zombie process?",
            "What is an orphan process?",
        ],
    )

    answers = {

        "Two sequential fork() calls: how many processes?":
        (
            "4",
            "Each fork can double the number of processes: "
            "1 → 2 → 4."
        ),

        "What does fork() return in the child?":
        (
            "0",
            "The child receives 0 as the return value of fork()."
        ),

        "What does the parent receive from fork()?":
        (
            "The child's PID",
            "The parent receives the process ID of the newly "
            "created child."
        ),

        "Why can wait() make execution order predictable?":
        (
            "The parent blocks until the child terminates",
            "wait() allows the parent to synchronize with child termination."
        ),

        "What happens after a successful exec()?":
        (
            "The old program image is replaced",
            "exec() loads a new executable into the current process."
        ),

        "What is a zombie process?":
        (
            "A terminated child that has not yet been reaped",
            "The child has exited but its parent has not collected "
            "its termination status."
        ),

        "What is an orphan process?":
        (
            "A child whose parent terminates first",
            "The child continues running after its original parent exits."
        ),
    }

    student_answer = st.text_input(
        "✏️ Your prediction"
    )

    if st.button(
        "🎯 Reveal Answer",
        type="primary",
    ):

        correct, explanation = answers[question]

        st.success(
            f"### Answer\n{correct}"
        )

        st.info(
            f"### Why?\n{explanation}"
        )

        if student_answer:

            st.write(
                f"**Your prediction:** {student_answer}"
            )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "OS Process Playground • Undergraduate OS Lab • "
    "Conceptual simulator for teaching process management."
)