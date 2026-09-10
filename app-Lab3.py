
import streamlit as st
import pandas as pd
import random
from collections import deque

st.set_page_config(
    page_title="CPU Scheduling Playground",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 3rem;}
.hero {
    padding: 1.6rem 1.8rem;
    border-radius: 18px;
    border: 1px solid rgba(120,120,120,.25);
    background: linear-gradient(135deg, rgba(240,244,255,.95), rgba(250,250,250,.98));
    margin-bottom: 1rem;
}
.badge {
    display:inline-block; padding:4px 10px; border-radius:999px;
    background:#e8eefc; margin-right:5px; font-size:.82rem;
}
.metric-card {
    border:1px solid rgba(120,120,120,.25); border-radius:14px;
    padding:14px; text-align:center; height:100%;
}
.small {font-size:.9rem; color:#666;}
</style>
""", unsafe_allow_html=True)

# ---------- Scheduling engines ----------
def fcfs(procs):
    t = 0
    rows = []
    for p in sorted(procs, key=lambda x: (x["arrival"], x["id"])):
        t = max(t, p["arrival"])
        start = t
        finish = t + p["burst"]
        rows.append((p["id"], start, finish))
        t = finish
    return rows

def sjf(procs):
    t, done, rows = 0, set(), []
    while len(done) < len(procs):
        avail = [p for p in procs if p["id"] not in done and p["arrival"] <= t]
        if not avail:
            t = min(p["arrival"] for p in procs if p["id"] not in done)
            continue
        p = min(avail, key=lambda x: (x["burst"], x["arrival"], x["id"]))
        rows.append((p["id"], t, t+p["burst"]))
        t += p["burst"]
        done.add(p["id"])
    return rows

def srtf(procs):
    rem = {p["id"]: p["burst"] for p in procs}
    finish = {}
    first = {}
    timeline = []
    t = 0
    while len(finish) < len(procs):
        avail = [p for p in procs if p["arrival"] <= t and rem[p["id"]] > 0]
        if not avail:
            t += 1
            timeline.append(("IDLE", t-1, t))
            continue
        p = min(avail, key=lambda x: (rem[x["id"]], x["arrival"], x["id"]))
        pid = p["id"]
        if pid not in first: first[pid] = t
        timeline.append((pid, t, t+1))
        rem[pid] -= 1
        t += 1
        if rem[pid] == 0:
            finish[pid] = t
    # Merge adjacent identical slices
    merged=[]
    for x in timeline:
        if merged and merged[-1][0] == x[0] and merged[-1][2] == x[1]:
            merged[-1]=(merged[-1][0], merged[-1][1], x[2])
        else: merged.append(x)
    return merged

def round_robin(procs, quantum):
    procs = sorted(procs, key=lambda x: (x["arrival"], x["id"]))
    rem = {p["id"]: p["burst"] for p in procs}
    i, t = 0, 0
    q = deque()
    rows = []
    while i < len(procs) or q:
        if not q and i < len(procs) and t < procs[i]["arrival"]:
            rows.append(("IDLE", t, procs[i]["arrival"]))
            t = procs[i]["arrival"]
        while i < len(procs) and procs[i]["arrival"] <= t:
            q.append(procs[i]); i += 1
        if not q: continue
        p = q.popleft()
        run = min(quantum, rem[p["id"]])
        rows.append((p["id"], t, t+run))
        t += run
        rem[p["id"]] -= run
        while i < len(procs) and procs[i]["arrival"] <= t:
            q.append(procs[i]); i += 1
        if rem[p["id"]] > 0:
            q.append(p)
    return rows

def metrics(procs, rows):
    finish = {}
    first = {}
    for pid,s,e in rows:
        if pid == "IDLE": continue
        first.setdefault(pid, s)
        finish[pid] = e
    data=[]
    for p in procs:
        f=finish[p["id"]]
        tat=f-p["arrival"]
        wait=tat-p["burst"]
        resp=first[p["id"]]-p["arrival"]
        data.append({**p, "Finish":f, "Turnaround":tat, "Waiting":wait, "Response":resp})
    df=pd.DataFrame(data)
    return df, {
        "avg_wait":df["Waiting"].mean(),
        "avg_turn":df["Turnaround"].mean(),
        "avg_resp":df["Response"].mean(),
    }

def gantt(rows):
    if not rows: return
    max_t=max(x[2] for x in rows)
    cols=st.columns(max(1, min(max_t, 20)))
    # A compact textual Gantt is more robust than complex charting.
    parts=[]
    for pid,s,e in rows:
        parts.append(f"`{s}` **{pid}** `{e}`")
    st.markdown(" → ".join(parts))

def random_processes(n=5, seed=7):
    rng=random.Random(seed)
    return [
        {"id":f"P{i+1}", "arrival":rng.randint(0,5), "burst":rng.randint(2,9)}
        for i in range(n)
    ]

# ---------- State ----------
if "score" not in st.session_state: st.session_state.score = 0
if "attempts" not in st.session_state: st.session_state.attempts = 0
if "challenge" not in st.session_state: st.session_state.challenge = None

# ---------- Hero ----------
st.markdown("""
<div class="hero">
<h1>🧠 CPU Scheduling Playground</h1>
<p style="font-size:1.12rem">
Learn scheduling by <b>playing</b>: build a workload, run different policies,
predict what happens, and challenge yourself with OS problems.
</p>
<span class="badge">FCFS</span><span class="badge">SJF</span>
<span class="badge">SRTF</span><span class="badge">Round Robin</span>
<span class="badge">MLFQ concepts</span><span class="badge">Fairness</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🎮 Your progress")
    st.metric("Challenge score", st.session_state.score)
    st.metric("Attempts", st.session_state.attempts)
    st.divider()
    page=st.radio("Choose a mode", [
        "🏠 Start Here",
        "🧪 Scheduling Lab",
        "🎯 Challenge Mode",
        "🧩 Problem Set",
        "📚 Concept Check",
    ])

# ---------- Start ----------
if page=="🏠 Start Here":
    st.subheader("Why scheduling?")
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown("### ⚙️ Mechanism")
        st.write("A context switch changes the running process by saving and restoring execution state.")
    with c2:
        st.markdown("### 🧭 Policy")
        st.write("The scheduler decides which ready process should run next.")
    with c3:
        st.markdown("### ⏱️ Time sharing")
        st.write("A timer interrupt lets a preemptive OS regain control even when a program keeps running.")
    st.info("Core idea from the lecture: **policy decides; mechanism executes.**")
    st.markdown("### The algorithms in this playground")
    st.dataframe(pd.DataFrame([
        ["FCFS", "Non-preemptive", "Oldest ready job first", "Convoy effect"],
        ["SJF", "Non-preemptive", "Shortest burst first", "Need burst estimate"],
        ["SRTF", "Preemptive", "Shortest remaining time", "More switching"],
        ["Round Robin", "Preemptive", "Fixed time quantum", "Quantum trade-off"],
        ["MLFQ", "Dynamic", "Priority changes with behavior", "Needs anti-starvation policy"],
    ], columns=["Policy","Type","Idea","Teaching point"]), hide_index=True, use_container_width=True)
    st.markdown("### 🎓 Suggested classroom flow")
    st.write("1. Predict → 2. Run the scheduler → 3. Inspect the Gantt chart → 4. Compare waiting/turnaround/response → 5. Explain why.")

# ---------- Lab ----------
elif page=="🧪 Scheduling Lab":
    st.subheader("🧪 Interactive Scheduling Lab")
    st.caption("Try to predict the schedule before pressing Run. This makes the activity useful for in-class discussion or homework.")

    if "workload" not in st.session_state:
        st.session_state.workload=random_processes()

    if st.button("🎲 Generate a new workload"):
        st.session_state.workload=random_processes(seed=random.randint(1,10000))

    df_in=pd.DataFrame(st.session_state.workload)
    edited=st.data_editor(df_in, num_rows="dynamic", use_container_width=True,
                          column_config={
                              "id":st.column_config.TextColumn("Process"),
                              "arrival":st.column_config.NumberColumn("Arrival", min_value=0, step=1),
                              "burst":st.column_config.NumberColumn("CPU Burst", min_value=1, step=1),
                          }, hide_index=True)
    procs=edited.to_dict("records")
    policy=st.selectbox("Choose scheduling policy", ["FCFS","SJF","SRTF","Round Robin"])
    quantum=2
    if policy=="Round Robin":
        quantum=st.slider("Time quantum",1,6,2)

    if st.button("▶ Run scheduler", type="primary"):
        if policy=="FCFS": rows=fcfs(procs)
        elif policy=="SJF": rows=sjf(procs)
        elif policy=="SRTF": rows=srtf(procs)
        else: rows=round_robin(procs, quantum)
        st.markdown("### Gantt chart")
        gantt(rows)
        mdf, av=metrics(procs, rows)
        a,b,c=st.columns(3)
        a.metric("Avg. waiting time", f"{av['avg_wait']:.2f}")
        b.metric("Avg. turnaround", f"{av['avg_turn']:.2f}")
        c.metric("Avg. response", f"{av['avg_resp']:.2f}")
        st.dataframe(mdf, hide_index=True, use_container_width=True)
        st.success("Now change one variable—arrival time, burst time, or quantum—and predict how the result changes.")

# ---------- Challenge ----------
elif page=="🎯 Challenge Mode":
    st.subheader("🎯 Beat the Scheduler")
    st.write("You get a workload and must answer one scheduling question. Correct answers earn points.")

    if st.session_state.challenge is None:
        st.session_state.challenge=random_processes(4, random.randint(1,100000))

    p=st.session_state.challenge
    st.dataframe(pd.DataFrame(p), hide_index=True, use_container_width=True)
    qtype=st.selectbox("Question", [
        "Under FCFS, what is the average waiting time?",
        "Under SJF, which process runs first?",
        "Under Round Robin (q=2), which process runs second?",
        "Under SRTF, which process is running at time 1?",
    ])
    # Compute answer
    if "average waiting" in qtype:
        _,av=metrics(p,fcfs(p)); answer=round(av["avg_wait"],2)
        options=[answer, round(answer+1,2), round(max(0,answer-1),2), round(answer+2,2)]
    elif "SJF" in qtype:
        answer=min(p,key=lambda x:(x["burst"],x["arrival"],x["id"]))["id"]
        options=[answer]+[x["id"] for x in p if x["id"]!=answer]
    elif "Round Robin" in qtype:
        rr=round_robin(p,2)
        nonidle=[x for x in rr if x[0]!="IDLE"]
        answer=nonidle[1][0] if len(nonidle)>1 else nonidle[0][0]
        options=[answer]+[x["id"] for x in p if x["id"]!=answer]
    else:
        sr=srtf(p)
        answer=next((pid for pid,s,e in sr if s<=1<e), "IDLE")
        options=[answer]+[x["id"] for x in p if x["id"]!=answer]
    options=list(dict.fromkeys(options))
    random.Random(sum(ord(c) for c in qtype)+len(p)).shuffle(options)
    choice=st.radio(qtype, options)
    if st.button("Check answer", type="primary"):
        st.session_state.attempts+=1
        if choice==answer:
            st.session_state.score+=10
            st.success(f"✅ Correct! +10 points. Answer: {answer}")
        else:
            st.error(f"❌ Not quite. Correct answer: {answer}")
        st.info("Generate another challenge for a fresh workload.")
    if st.button("🔄 New challenge"):
        st.session_state.challenge=random_processes(4, random.randint(1,100000))
        st.rerun()

# ---------- Problem set ----------
elif page=="🧩 Problem Set":
    st.subheader("🧩 Scheduling Problems")
    st.caption("These are designed as short, US-classroom-friendly practice problems. Students can solve by hand and then verify with the lab.")

    problems=[
        ("1. FCFS waiting time",
         "Processes arrive as follows: P1(0,5), P2(1,2), P3(2,1). Under FCFS, what is the average waiting time?",
         "P1 waits 0, P2 waits 4, P3 waits 5 → average = 3.0 time units."),
        ("2. Convoy effect",
         "A 12-unit CPU-bound job arrives before three 1-unit jobs. Why can FCFS produce poor response time?",
         "The short jobs form a convoy behind the long job, so interactive/short work waits even though it could finish quickly."),
        ("3. SJF",
         "At time 0, P1 needs 8 units, P2 needs 3, and P3 needs 5. Which process does non-preemptive SJF choose?",
         "P2, because it has the shortest CPU burst."),
        ("4. SRTF",
         "P1 starts with 8 units remaining. At time 2, P2 arrives needing 2 units. What does SRTF do?",
         "Preempt P1 and run P2 because 2 < P1's remaining time."),
        ("5. Round Robin",
         "Three jobs have bursts 5, 3, and 1. With quantum=2, what is the key effect of making the quantum much smaller?",
         "Better responsiveness but more context switches and scheduling overhead."),
        ("6. Response vs turnaround",
         "A process arrives at time 4, first runs at time 7, and finishes at time 12. Its CPU burst is 3. Find response time and turnaround time.",
         "Response = 7−4 = 3. Turnaround = 12−4 = 8."),
        ("7. Starvation",
         "A low-priority job waits while high-priority jobs repeatedly arrive. What technique can help?",
         "Aging or periodic priority reset can gradually raise the waiting job's priority."),
        ("8. Fairness",
         "Two jobs have weights 1 and 2 in a weighted fair scheduler. Roughly what CPU-share ratio should they receive?",
         "Approximately 1:2, assuming the scheduler can enforce the intended shares."),
    ]
    for title,question,answer in problems:
        with st.expander(title):
            st.write(question)
            if st.checkbox("Show solution", key=title):
                st.success(answer)

# ---------- Concept check ----------
else:
    st.subheader("📚 Concept Check")
    questions=[
        ("What is the difference between a trap and a context switch?",
         ["Trap enters the kernel; context switch changes the running process.",
          "They are exactly the same.",
          "Trap only happens on multicore CPUs."],0),
        ("Which policy is non-preemptive?",
         ["SRTF","Round Robin","SJF"],2),
        ("What lets a preemptive OS regain control when a program does not make a system call?",
         ["Timer interrupt","printf()","A normal function call"],0),
        ("What is the main trade-off controlled by Round Robin's quantum?",
         ["Responsiveness vs. context-switch overhead","Disk size vs. RAM size","Security vs. encryption"],0),
        ("What is a major weakness of SJF?",
         ["It requires knowledge/estimation of future CPU burst length.",
          "It cannot run on a CPU.",
          "It always causes starvation."],0),
        ("What is the central MLFQ idea?",
         ["Dynamic priority levels based on observed behavior.",
          "Only one process may ever run.",
          "Always choose the longest job first."],0),
    ]
    for i,(q,opts,ans) in enumerate(questions):
        st.markdown(f"**{i+1}. {q}**")
        pick=st.radio("",opts,key=f"cq{i}",index=None)
        if st.button("Check",key=f"cb{i}"):
            if pick==opts[ans]: st.success("Correct! 🎉")
            else: st.error(f"Try again. Correct: {opts[ans]}")
        st.divider()

st.caption("Built as an interactive teaching companion for the scheduling material: mechanism vs. policy, preemption, timer interrupts, FCFS, SJF, SRTF, Round Robin, weighted fairness, MLFQ, starvation, and multicore load balancing.")

