
import streamlit as st
import time
import textwrap

st.set_page_config(
    page_title="IPC Playground — Operating Systems",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #1f324c;
    margin-bottom: 0.2rem;
}
.subtitle {
    color: #5f6b78;
    font-size: 1.05rem;
    margin-bottom: 1rem;
}
.analogy {
    padding: 1rem 1.2rem;
    border-radius: 12px;
    background: #f2f6fa;
    border-left: 5px solid #e08736;
    margin: 0.7rem 0 1rem 0;
}
.step {
    padding: 0.65rem 0.8rem;
    border-radius: 9px;
    background: #f7f9fb;
    border: 1px solid #dce3ea;
    margin: 0.35rem 0;
}
.good {
    padding: 0.8rem;
    border-radius: 10px;
    background: #edf7ef;
    border-left: 5px solid #46915f;
}
.warn {
    padding: 0.8rem;
    border-radius: 10px;
    background: #fff6e9;
    border-left: 5px solid #e08736;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Helpers
# -----------------------------
def code_block(code):
    st.code(textwrap.dedent(code).strip(), language="c")

def analogy(title, body):
    st.markdown(
        f'<div class="analogy"><b>{title}</b><br>{body}</div>',
        unsafe_allow_html=True,
    )

def process_box(name, content, emoji="⚙️"):
    st.markdown(
        f"""
        <div style="padding:1rem;border:2px solid #dce3ea;border-radius:12px;text-align:center;background:#fafbfd">
        <div style="font-size:1.8rem">{emoji}</div>
        <b>{name}</b><br><span style="color:#5f6b78">{content}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">🔄 IPC Playground</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Interactive programming demonstrations for Inter-Process Communication.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📚 IPC Topics")
topic = st.sidebar.radio(
    "Choose a concept",
    [
        "🏠 IPC Overview",
        "🔢 File Descriptors",
        "🚰 Pipes",
        "📮 Message Queues",
        "📞 Sockets",
        "📝 Shared Memory",
        "🔔 Signals",
        "⏳ Blocking vs Non-Blocking",
        "🍽️ Mini Project: Restaurant",
        "🧠 Quiz",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Teaching idea:\n\n"
    "📞 Socket = telephone\n\n"
    "📮 Queue = mailbox\n\n"
    "🚰 Pipe = conveyor belt\n\n"
    "📝 Shared memory = whiteboard\n\n"
    "🔔 Signal = doorbell"
)

# -----------------------------
# Overview
# -----------------------------
if topic == "🏠 IPC Overview":
    st.header("What problem does IPC solve?")

    analogy(
        "🏠 Hostel-room analogy",
        "Two students live in different rooms. A variable written on one student's desk does not "
        "automatically appear on the other student's desk. Processes are similarly isolated by default."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        process_box("Process A", "Own address space", "🧑‍💻")
    with c2:
        process_box("IPC", "Controlled communication", "🔄")
    with c3:
        process_box("Process B", "Own address space", "🧑‍💻")

    st.subheader("The five communication patterns")
    data = {
        "Mechanism": ["Socket", "Message Queue", "Pipe", "Shared Memory", "Signal"],
        "Analogy": ["Telephone", "Mailbox", "Conveyor belt", "Whiteboard", "Doorbell"],
        "Main idea": [
            "Two-way conversation",
            "Messages can wait",
            "One-way byte stream",
            "Common memory region",
            "Notification/event",
        ],
    }
    st.table(data)

    st.subheader("A familiar application")
    cols = st.columns(4)
    labels = [
        ("🌐 Browser", "Client"),
        ("🖥️ Web Server", "Request handler"),
        ("⚙️ App Server", "Business logic"),
        ("🗄️ Database", "Data storage"),
    ]
    for col, (name, desc) in zip(cols, labels):
        with col:
            process_box(name, desc)

    st.markdown(
        '<div class="good"><b>Teaching takeaway:</b> IPC is needed because a system can be divided into '
        'multiple processes that still need to exchange information.</div>',
        unsafe_allow_html=True,
    )

# -----------------------------
# File descriptors
# -----------------------------
elif topic == "🔢 File Descriptors":
    st.header("File Descriptors: the OS handle")

    analogy(
        "📚 Library-token analogy",
        "Imagine a library gives you token #7. You use #7 to refer to a resource instead of carrying "
        "the entire library around. A file descriptor is an integer handle used by a process to access "
        "an open file, socket, pipe, or similar resource."
    )

    fd = st.slider("Choose a file descriptor", 0, 8, 3)
    resources = {
        0: "STDIN — keyboard/input",
        1: "STDOUT — terminal/output",
        2: "STDERR — error output",
        3: "PIPE / SOCKET / FILE — example open resource",
        4: "Another open resource",
        5: "Another open resource",
        6: "Another open resource",
        7: "Another open resource",
        8: "Another open resource",
    }

    st.metric("Selected fd", fd)
    st.write(f"**OS view:** `{fd}` → {resources[fd]}")

    st.subheader("Programming pattern")
    code_block(r'''
    int fd = open("data.txt", O_RDONLY);

    char buf[64];
    read(fd, buf, 64);

    close(fd);
    ''')

    st.caption("The same handle idea appears when IPC mechanisms return file descriptors.")

# -----------------------------
# Pipes
# -----------------------------
elif topic == "🚰 Pipes":
    st.header("Pipes: a one-way conveyor belt")

    analogy(
        "🚰 Conveyor-belt analogy",
        "Process A puts data onto the conveyor. Process B takes data from the other end. "
        "A normal pipe is unidirectional and follows FIFO ordering."
    )

    direction = st.radio("Choose a communication direction", ["Parent → Child", "Child → Parent"])
    payload = st.text_input("Message to send", "Hello from the child!")

    c1, c2, c3 = st.columns([2, 3, 2])
    with c1:
        process_box("Process A", "write()", "🧑‍💻")
    with c2:
        st.markdown(
            f"<div style='text-align:center;padding-top:2rem;font-size:1.8rem'>➡️ <b>PIPE BUFFER</b> ➡️<br>"
            f"<span style='font-size:1rem;color:#5f6b78'>{payload}</span></div>",
            unsafe_allow_html=True
        )
    with c3:
        process_box("Process B", "read()", "🧑‍💻")

    st.subheader("Try the simulation")
    if st.button("🚀 Send through pipe"):
        st.success(f"Receiver read: **{payload}**")
        st.write("The bytes were conceptually buffered by the pipe until the receiver read them.")

    st.subheader("C programming skeleton")
    code_block(r'''
    int fd[2];
    pipe(fd);

    pid_t pid = fork();

    if (pid == 0) {
        // Child: write
        close(fd[0]);
        write(fd[1], message, strlen(message) + 1);
        close(fd[1]);
    } else {
        // Parent: read
        close(fd[1]);
        read(fd[0], buffer, sizeof(buffer));
        printf("Parent received: %s\n", buffer);
        close(fd[0]);
        wait(NULL);
    }
    ''')

    st.subheader("Programming challenge")
    st.write("Make the child send 10 integers and let the parent calculate their sum.")

    st.markdown(
        '<div class="warn"><b>Question:</b> Why do we close the unused read/write ends?</div>',
        unsafe_allow_html=True,
    )

# -----------------------------
# Message Queues
# -----------------------------
elif topic == "📮 Message Queues":
    st.header("Message Queues: the OS mailbox")

    analogy(
        "📮 Mailbox analogy",
        "The sender drops a message into a mailbox. The receiver does not have to be ready at exactly "
        "the same moment; the message can remain queued until it is retrieved."
    )

    if "mq" not in st.session_state:
        st.session_state.mq = []

    left, right = st.columns(2)
    with left:
        msg = st.text_input("New message", "Order: Pizza")
        priority = st.selectbox("Priority", ["Normal", "VIP", "Emergency"])
        if st.button("📨 Send message"):
            st.session_state.mq.append({"text": msg, "priority": priority})
            st.success("Message placed in the queue.")

    with right:
        st.subheader("📮 Queue")
        if st.session_state.mq:
            for i, item in enumerate(st.session_state.mq, 1):
                st.markdown(
                    f'<div class="step"><b>{i}. [{item["priority"]}]</b> {item["text"]}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Queue is empty.")

        if st.button("📥 Receive oldest message"):
            if st.session_state.mq:
                item = st.session_state.mq.pop(0)
                st.success(f'Received: {item["text"]} ({item["priority"]})')
            else:
                st.warning("Nothing to receive.")

    st.subheader("C programming idea")
    code_block(r'''
    int msgid = msgget(key, IPC_CREAT | 0666);

    // Sender
    msgsnd(msgid, &message, sizeof(message), 0);

    // Receiver
    msgrcv(msgid, &message, sizeof(message), 0, 0);
    ''')

    st.subheader("Challenge")
    st.write("Modify the design so that Emergency messages are processed before Normal messages.")

# -----------------------------
# Sockets
# -----------------------------
elif topic == "📞 Sockets":
    st.header("Sockets: a telephone for processes")

    analogy(
        "📞 Telephone analogy",
        "A socket is like a telephone. A connection-oriented socket establishes a connection first, "
        "then both sides can exchange messages."
    )

    mode = st.radio("Socket style", ["Connection-oriented", "Connection-less"])

    if mode == "Connection-oriented":
        st.subheader("Server lifecycle")
        steps = ["socket()", "bind()", "listen()", "accept()", "recv()/send()"]
        cols = st.columns(len(steps))
        for col, step in zip(cols, steps):
            with col:
                process_box(step, "server", "🔹")

        st.subheader("Client lifecycle")
        steps = ["socket()", "connect()", "send()/recv()"]
        cols = st.columns(len(steps))
        for col, step in zip(cols, steps):
            with col:
                process_box(step, "client", "🔹")

        st.subheader("Interactive client-server demo")
        client_msg = st.text_input("Client message", "Hello Server")
        if st.button("📞 Connect and send"):
            progress = st.progress(0)
            status = st.empty()
            for p, text in [(20, "socket()"), (40, "connect()"), (60, "send()"), (80, "server recv()"), (100, "server send()")]:
                progress.progress(p)
                status.write(f"Executing conceptually: `{text}`")
                time.sleep(0.15)
            st.success(f"Server received: **{client_msg}**")
            st.info("Server response: **Hello Client — message received!**")

        code_block(r'''
        // Server
        int sockfd = socket(AF_INET, SOCK_STREAM, 0);
        bind(sockfd, ...);
        listen(sockfd, 5);
        int newsockfd = accept(sockfd, ...);

        recv(newsockfd, buffer, sizeof(buffer), 0);
        send(newsockfd, response, strlen(response), 0);

        // Client
        int sockfd = socket(AF_INET, SOCK_STREAM, 0);
        connect(sockfd, ...);

        send(sockfd, request, strlen(request), 0);
        recv(sockfd, buffer, sizeof(buffer), 0);
        ''')

    else:
        st.subheader("Connection-less communication")
        st.write("Each message conceptually carries the address of the remote endpoint.")
        code_block(r'''
        int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

        sendto(sockfd, message, ...,
               (struct sockaddr *)&server_addr, ...);

        recvfrom(sockfd, buffer, ...,
                 (struct sockaddr *)&client_addr, ...);
        ''')

# -----------------------------
# Shared memory
# -----------------------------
elif topic == "📝 Shared Memory":
    st.header("Shared Memory: one whiteboard")

    analogy(
        "📝 Whiteboard analogy",
        "Two students can look at the same whiteboard. If one writes `x = 10`, the other can see it. "
        "The benefit is fast shared data, but coordination is still needed when both access the data."
    )

    value = st.number_input("Value in shared memory", value=10, step=1)
    c1, c2, c3 = st.columns(3)
    with c1:
        process_box("Process A", "reads shared value", "🧑‍💻")
    with c2:
        st.markdown(
            f"<div style='text-align:center;padding-top:1.5rem;font-size:2rem'>📝<br><b>{value}</b></div>",
            unsafe_allow_html=True
        )
    with c3:
        process_box("Process B", "reads shared value", "🧑‍💻")

    st.subheader("Experiment: shared counter")
    if "counter" not in st.session_state:
        st.session_state.counter = 0

    a, b = st.columns(2)
    with a:
        if st.button("Process A: counter++"):
            st.session_state.counter += 1
    with b:
        if st.button("Process B: counter++"):
            st.session_state.counter += 1

    st.metric("Shared counter", st.session_state.counter)

    if st.button("Reset counter"):
        st.session_state.counter = 0
        st.rerun()

    st.subheader("C programming idea")
    code_block(r'''
    int shmid = shmget(key, size, IPC_CREAT | 0666);

    char *data = shmat(shmid, NULL, 0);

    // Multiple processes can access *data
    data[0] = 'A';

    shmdt(data);
    ''')

    st.markdown(
        '<div class="warn"><b>Important:</b> Shared memory solves data sharing, but not necessarily '
        'the coordination problem. If two processes modify the same data concurrently, synchronization '
        'may be needed.</div>',
        unsafe_allow_html=True,
    )

# -----------------------------
# Signals
# -----------------------------
elif topic == "🔔 Signals":
    st.header("Signals: the OS doorbell")

    analogy(
        "🔔 Doorbell analogy",
        "A signal is a notification: it tells a process that something happened. It is not intended "
        "to carry a long conversation."
    )

    if "signals" not in st.session_state:
        st.session_state.signals = []

    signal = st.selectbox(
        "Choose a signal",
        ["SIGINT — Ctrl+C", "SIGTERM — request termination", "SIGUSR1 — user-defined event", "SIGKILL — force termination"]
    )

    if st.button("🔔 Send signal"):
        st.session_state.signals.append(signal)
        st.success(f"Signal delivered conceptually: **{signal}**")

    st.subheader("Signal history")
    for s in st.session_state.signals[-8:]:
        st.markdown(f'<div class="step">🔔 {s}</div>', unsafe_allow_html=True)

    st.subheader("C programming example")
    code_block(r'''
    void sigint_handler(int sig) {
        printf("Caught SIGINT\n");
        printf("Cleaning up...\n");
        exit(0);
    }

    int main() {
        signal(SIGINT, sigint_handler);

        while (1) {
            printf("Program running...\n");
            sleep(1);
        }
    }
    ''')

    st.markdown(
        '<div class="good"><b>Try it on Linux:</b> run the program and press Ctrl+C. '
        'The OS can generate SIGINT, and the program can handle it with a signal handler.</div>',
        unsafe_allow_html=True,
    )

    st.warning("SIGKILL cannot be overridden by a user-defined signal handler.")

# -----------------------------
# Blocking
# -----------------------------
elif topic == "⏳ Blocking vs Non-Blocking":
    st.header("Blocking vs Non-Blocking IPC")

    analogy(
        "🚌 Bus-stop analogy",
        "Blocking means: stand at the bus stop until the bus arrives. Non-blocking means: check whether "
        "the bus is there; if not, return and do something else."
    )

    mode = st.radio("Choose mode", ["Blocking", "Non-blocking"])
    buffer_state = st.radio("Temporary buffer", ["Empty", "Has data", "Full"])

    if mode == "Blocking":
        if buffer_state == "Empty":
            st.warning("Receiver calls recv/read → no data → receiver waits.")
        elif buffer_state == "Full":
            st.warning("Sender tries to send → buffer full → sender may wait.")
        else:
            st.success("Data is available → operation can proceed.")
    else:
        if buffer_state == "Empty":
            st.info("Receiver checks → no data → returns instead of waiting.")
        elif buffer_state == "Full":
            st.info("Sender checks → buffer full → returns instead of waiting.")
        else:
            st.success("Data is available → operation proceeds.")

    st.subheader("Core idea")
    st.code(
        '''Blocking:
send()/recv() may wait for the operation to become possible.

Non-blocking:
send()/recv() can return an error/status instead of waiting.''',
        language="text",
    )

# -----------------------------
# Mini project
# -----------------------------
elif topic == "🍽️ Mini Project: Restaurant":
    st.header("Mini Project: Restaurant Ordering System")

    analogy(
        "🍽️ Why a restaurant?",
        "It naturally contains multiple independent roles. The customer talks to the order server, "
        "the server sends jobs to the kitchen, and the kitchen can notify the server when an order is ready."
    )

    st.markdown("""
    **Architecture**

    `Customer → Socket → Order Server → Message Queue → Kitchen`

    `Kitchen → Signal → Order Server`
    """)

    if "orders" not in st.session_state:
        st.session_state.orders = []
    if "ready" not in st.session_state:
        st.session_state.ready = []

    menu = ["Pizza", "Burger", "Pasta", "Sandwich"]
    order = st.selectbox("Customer order", menu)

    if st.button("🧑‍🍳 Place order"):
        st.session_state.orders.append(order)
        st.success(f"Customer sent **{order}** through the socket.")

    st.subheader("📮 Kitchen message queue")
    if st.session_state.orders:
        for i, item in enumerate(st.session_state.orders):
            st.markdown(f'<div class="step">Order {i+1}: 🍽️ {item}</div>', unsafe_allow_html=True)
    else:
        st.info("No orders.")

    if st.button("🔥 Kitchen processes next order"):
        if st.session_state.orders:
            item = st.session_state.orders.pop(0)
            st.session_state.ready.append(item)
            st.success(f"Kitchen cooked **{item}** and sent a completion signal.")
        else:
            st.warning("No pending order.")

    st.subheader("🔔 Completed orders")
    for item in st.session_state.ready:
        st.markdown(f'<div class="good">🔔 {item} is ready!</div>', unsafe_allow_html=True)

    st.subheader("How the three IPC mechanisms fit")
    cols = st.columns(3)
    with cols[0]:
        process_box("Socket", "Customer ↔ Server", "📞")
    with cols[1]:
        process_box("Message Queue", "Server → Kitchen", "📮")
    with cols[2]:
        process_box("Signal", "Kitchen → Server", "🔔")

    st.subheader("Final-project C design")
    code_block(r'''
    /*
       Mini Restaurant IPC

       1. Client -> Server:
          TCP socket

       2. Server -> Kitchen:
          Message queue

       3. Kitchen -> Server:
          SIGUSR1 notification

       Students implement:
       client.c
       server.c
       kitchen.c
    */

    // Client:
    send(sockfd, order, strlen(order), 0);

    // Server:
    recv(newsockfd, order, sizeof(order), 0);
    msgsnd(msgid, &order_msg, sizeof(order_msg), 0);

    // Kitchen:
    msgrcv(msgid, &order_msg, sizeof(order_msg), 0, 0);
    printf("Cooking %s\n", order_msg.text);

    // Notify server:
    kill(server_pid, SIGUSR1);
    ''')

    st.markdown(
        '<div class="good"><b>Student deliverable:</b> implement the three processes, demonstrate '
        'the complete data flow, and explain why each IPC mechanism was selected.</div>',
        unsafe_allow_html=True,
    )

# -----------------------------
# Quiz
# -----------------------------
elif topic == "🧠 Quiz":
    st.header("🧠 IPC Quick Quiz")

    questions = [
        (
            "Two processes need a two-way conversation. Which IPC is most directly represented by the telephone analogy?",
            ["Pipe", "Socket", "Signal", "Shared memory"],
            "Socket",
        ),
        (
            "A message should wait until another process is ready to retrieve it. Which mechanism fits the mailbox analogy?",
            ["Message queue", "Signal", "Pipe", "File descriptor"],
            "Message queue",
        ),
        (
            "What does `cat file.txt | grep OS` use?",
            ["Shared memory", "Signal", "Pipe", "Message queue"],
            "Pipe",
        ),
        (
            "Which IPC provides a shared memory region to multiple processes?",
            ["Socket", "Pipe", "Shared memory", "Signal"],
            "Shared memory",
        ),
        (
            "Ctrl+C is commonly associated with which signal?",
            ["SIGINT", "SIGKILL", "SIGUSR1", "SIGPIPE"],
            "SIGINT",
        ),
        (
            "What is a file descriptor?",
            ["A CPU register", "An integer handle for an open resource", "A process ID", "A memory page"],
            "An integer handle for an open resource",
        ),
        (
            "If a receiver waits because a temporary IPC buffer is empty, this is an example of:",
            ["Non-blocking", "Blocking", "Forking", "Paging"],
            "Blocking",
        ),
    ]

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = set()

    for i, (q, opts, ans) in enumerate(questions):
        st.markdown(f"### {i+1}. {q}")
        selected = st.radio("Answer:", opts, key=f"q{i}")
        if st.button(f"Check Q{i+1}", key=f"check{i}"):
            if i not in st.session_state.answered:
                st.session_state.answered.add(i)
                if selected == ans:
                    st.session_state.score += 1
                    st.success("Correct! 🎉")
                else:
                    st.error(f"Not quite. Correct answer: **{ans}**")

    st.divider()
    st.metric("Score", f"{st.session_state.score} / {len(questions)}")

    if st.button("Reset quiz"):
        st.session_state.score = 0
        st.session_state.answered = set()
        st.rerun()

# -----------------------------
# Footer
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.caption("IPC Playground • UG Operating Systems")
st.caption(
    "Conceptual demonstrations are intentionally interactive/simulated. "
    "The C snippets show the programming model; run the C programs on Linux/WSL to observe real OS behavior."
)

