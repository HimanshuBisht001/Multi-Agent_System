import streamlit as st
import time
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
from langchain_core.messages import ToolMessage


# ─────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Research AI · Multi-Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  Custom CSS  (dark editorial theme)
# ─────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=DM+Mono:wght@400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:       #0c0c0f;
    --surface:  #13131a;
    --border:   #22222e;
    --accent:   #e8ff47;
    --accent2:  #47ffe8;
    --muted:    #5a5a72;
    --text:     #dcdcf0;
    --text-dim: #8888a8;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--surface) !important; }
footer { visibility: hidden; }

/* ── Hero heading ── */
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 8vw, 6.5rem);
    letter-spacing: 0.04em;
    line-height: 0.92;
    color: var(--text);
    margin: 0;
}
.hero-title span { color: var(--accent); }

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: var(--text-dim);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.75rem;
}

/* ── Input area ── */
[data-testid="stTextInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
    padding: 0.85rem 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(232,255,71,0.12) !important;
}
[data-testid="stTextInput"] label {
    color: var(--text-dim) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}

/* ── Primary button ── */
[data-testid="stButton"] > button {
    background: var(--accent) !important;
    color: #0c0c0f !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.15rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.65rem 2.2rem !important;
    cursor: pointer !important;
    transition: opacity 0.15s, transform 0.1s !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── Pipeline step cards ── */
.step-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 2px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
}
.step-card.active { border-left-color: var(--accent2); }
.step-card.done   { border-left-color: #47ff8a; }

.step-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}
.step-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    color: var(--text);
}

/* ── Output panels ── */
.output-block {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
}
.output-block h4 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: 0.08em;
    color: var(--accent);
    margin: 0 0 0.9rem 0;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
}
.output-block p, .output-block li {
    font-size: 0.93rem;
    line-height: 1.75;
    color: var(--text);
}

/* ── Tag pills ── */
.tag {
    display: inline-block;
    background: rgba(232,255,71,0.10);
    color: var(--accent);
    border: 1px solid rgba(232,255,71,0.25);
    border-radius: 100px;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    padding: 0.15rem 0.65rem;
    margin-right: 0.4rem;
    text-transform: uppercase;
}

/* ── Divider ── */
hr.fancy {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, var(--accent) 0%, transparent 100%);
    margin: 2rem 0;
}

/* ── Spinner text override ── */
[data-testid="stSpinner"] p { color: var(--text-dim) !important; font-family: 'DM Mono', monospace !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-dim) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
#  Pipeline runner (mirrors pipeline.py logic)
# ─────────────────────────────────────────────
def run_research_pipeline(topic: str, status_placeholders: dict) -> dict:
    state = {}

    # ── Step 1: Search Agent ──────────────────
    status_placeholders["search"].markdown(
        '<div class="step-card active"><div class="step-label">Step 01 / 04</div>'
        '<div class="step-title">🔍 Search Agent — finding information…</div></div>',
        unsafe_allow_html=True,
    )

    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {"messages": [("user", f"Find the reliable and detailed information about: {topic}.")]}
    )

    raw_search_results = ""
    for msg in search_result["messages"]:
        if isinstance(msg, ToolMessage):
            raw_search_results = msg.content

    state["search_summary"] = search_result["messages"][-1].content
    state["raw_search_results"] = raw_search_results

    status_placeholders["search"].markdown(
        '<div class="step-card done"><div class="step-label">Step 01 / 04</div>'
        '<div class="step-title">✅ Search Agent — complete</div></div>',
        unsafe_allow_html=True,
    )

    # ── Step 2: Reader Agent ──────────────────
    status_placeholders["reader"].markdown(
        '<div class="step-card active"><div class="step-label">Step 02 / 04</div>'
        '<div class="step-title">📄 Reader Agent — scraping top resource…</div></div>',
        unsafe_allow_html=True,
    )

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""
Based on the following search results about: {topic}

Choose the MOST relevant NEWS ARTICLE URL.

Avoid:
- Twitter/X
- Facebook
- social media pages

Then scrape the webpage using the scraping tool.
Return the RAW scraped text only. Do not summarize.

Search Results:
{state['raw_search_results']}
""",
                )
            ]
        }
    )

    state["scraped_content"] = reader_result["messages"][-1].content

    status_placeholders["reader"].markdown(
        '<div class="step-card done"><div class="step-label">Step 02 / 04</div>'
        '<div class="step-title">✅ Reader Agent — complete</div></div>',
        unsafe_allow_html=True,
    )

    # ── Step 3: Writer ────────────────────────
    status_placeholders["writer"].markdown(
        '<div class="step-card active"><div class="step-label">Step 03 / 04</div>'
        '<div class="step-title">✍️  Writer — drafting the report…</div></div>',
        unsafe_allow_html=True,
    )

    agent_research = (
        f"Search Summary:\n{state['search_summary']}\n\n"
        f"Scraped Content: {state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({"topic": topic, "research": agent_research})

    status_placeholders["writer"].markdown(
        '<div class="step-card done"><div class="step-label">Step 03 / 04</div>'
        '<div class="step-title">✅ Writer — report drafted</div></div>',
        unsafe_allow_html=True,
    )

    # ── Step 4: Critic ────────────────────────
    status_placeholders["critic"].markdown(
        '<div class="step-card active"><div class="step-label">Step 04 / 04</div>'
        '<div class="step-title">🧐 Critic — reviewing the report…</div></div>',
        unsafe_allow_html=True,
    )

    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    status_placeholders["critic"].markdown(
        '<div class="step-card done"><div class="step-label">Step 04 / 04</div>'
        '<div class="step-title">✅ Critic — feedback ready</div></div>',
        unsafe_allow_html=True,
    )

    return state


# ─────────────────────────────────────────────
#  Layout
# ─────────────────────────────────────────────

# ── Hero ─────────────────────────────────────
st.markdown(
    """
<div style="padding: 2.5rem 0 1.5rem 0;">
    <p class="hero-sub">Multi-Agent · AI Research System</p>
    <h1 class="hero-title">DEEP<br><span>RESEARCH</span></h1>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown('<hr class="fancy">', unsafe_allow_html=True)

# ── Input row ─────────────────────────────────
col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")

with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum Computing breakthroughs 2025",
        key="topic_input",
        label_visibility="visible",
    )

with col_btn:
    run_btn = st.button("RUN →", use_container_width=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── Agent pills ───────────────────────────────
st.markdown(
    """
<div style="margin-bottom:1.8rem">
    <span class="tag">Search Agent</span>
    <span style="color:#5a5a72; font-size:0.8rem; margin:0 0.3rem">→</span>
    <span class="tag">Reader Agent</span>
    <span style="color:#5a5a72; font-size:0.8rem; margin:0 0.3rem">→</span>
    <span class="tag">Writer Chain</span>
    <span style="color:#5a5a72; font-size:0.8rem; margin:0 0.3rem">→</span>
    <span class="tag">Critic Chain</span>
</div>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  Run pipeline
# ─────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic before running.")
    else:
        # ── Status cards placeholders ─────────
        st.markdown("#### Pipeline Progress")
        ph_search = st.empty()
        ph_reader = st.empty()
        ph_writer = st.empty()
        ph_critic = st.empty()

        # Initial idle state
        for ph, num, label in [
            (ph_search, "01", "Search Agent"),
            (ph_reader, "02", "Reader Agent"),
            (ph_writer, "03", "Writer"),
            (ph_critic, "04", "Critic"),
        ]:
            ph.markdown(
                f'<div class="step-card"><div class="step-label">Step {num} / 04</div>'
                f'<div class="step-title" style="color:var(--muted)">{label} — waiting…</div></div>',
                unsafe_allow_html=True,
            )

        status_phs = {
            "search": ph_search,
            "reader": ph_reader,
            "writer": ph_writer,
            "critic": ph_critic,
        }

        # ── Execute ───────────────────────────
        with st.spinner("Running research pipeline…"):
            try:
                result = run_research_pipeline(topic.strip(), status_phs)
            except Exception as e:
                st.error(f"Pipeline error: {e}")
                st.stop()

        st.markdown('<hr class="fancy">', unsafe_allow_html=True)

        # ─────────────────────────────────────
        #  Results
        # ─────────────────────────────────────
        st.markdown(
            f"""
<div style="margin-bottom:1.2rem">
    <p class="hero-sub" style="margin-bottom:0.3rem">Research complete for</p>
    <h2 style="font-family:'Bebas Neue',sans-serif; font-size:2.4rem;
               letter-spacing:0.06em; color:var(--accent); margin:0">{topic}</h2>
</div>
""",
            unsafe_allow_html=True,
        )

        # ── Two-column layout: Report | Feedback ──
        col_report, col_feedback = st.columns([3, 2], gap="large")

        with col_report:
            st.markdown(
                '<div class="output-block"><h4>📋 Final Report</h4>',
                unsafe_allow_html=True,
            )
            st.markdown(result["report"])
            st.markdown("</div>", unsafe_allow_html=True)

        with col_feedback:
            st.markdown(
                '<div class="output-block"><h4>🧐 Critic Feedback</h4>',
                unsafe_allow_html=True,
            )
            st.markdown(result["feedback"])
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Raw data expanders ─────────────────
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        with st.expander("🔎 View Search Summary"):
            st.text(result["search_summary"])

        with st.expander("📑 View Raw Search Results"):
            st.text(result["raw_search_results"])

        with st.expander("🌐 View Scraped Content"):
            st.text(result["scraped_content"])

        # ── Download button ───────────────────
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        download_text = (
            f"RESEARCH REPORT: {topic}\n"
            f"{'='*60}\n\n"
            f"{result['report']}\n\n"
            f"{'='*60}\n"
            f"CRITIC FEEDBACK\n"
            f"{'='*60}\n\n"
            f"{result['feedback']}"
        )
        st.download_button(
            label="⬇ Download Report",
            data=download_text,
            file_name=f"research_{topic[:40].replace(' ', '_')}.txt",
            mime="text/plain",
        )