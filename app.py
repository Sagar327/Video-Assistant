import streamlit as st
import time
from dotenv import load_dotenv
from utils.audio_processor import process_input
from Core.transcriber import transcribe_all
from Core.summarize import summarize, generate_title
from Core.extractor import extract_all_insights
from Core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Root Variables ── */
:root {
    --bg-dark: #09090d;
    --surface-glass: rgba(18, 18, 26, 0.75);
    --surface-card: #12121a;
    --surface-border: #242436;
    --accent-purple: #8b5cf6;
    --accent-cyan: #06b6d4;
    --accent-glow: rgba(139, 92, 246, 0.25);
    --text-primary: #f3f4f6;
    --text-secondary: #9ca3af;
    --success: #10b981;
    --warning: #f59e0b;
}

/* ── Global Styles ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: var(--bg-dark) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: radial-gradient(circle at 50% 0%, #17102b 0%, #09090d 70%) !important;
}

/* Grid overlay background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image: 
        linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar Styling ── */
[data-testid="stSidebar"] {
    background: rgba(12, 12, 18, 0.95) !important;
    border-right: 1px solid var(--surface-border) !important;
    backdrop-filter: blur(12px);
}

/* ── Typography & Cards ── */
.hero-title {
    font-size: clamp(2.2rem, 4vw, 3.2rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 30%, #a78bfa 70%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-secondary);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

.glass-card {
    background: var(--surface-glass);
    border: 1px solid var(--surface-border);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.glass-card:hover {
    border-color: rgba(139, 92, 246, 0.4);
}

.card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.725rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent-cyan);
    margin-bottom: 0.5rem;
}

/* ── UI Badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-purple { background: rgba(139, 92, 246, 0.15); color: #c4b5fd; border: 1px solid rgba(139, 92, 246, 0.3); }
.badge-cyan   { background: rgba(6, 182, 212, 0.15); color: #67e8f9; border: 1px solid rgba(6, 182, 212, 0.3); }
.badge-green  { background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.3); }

/* ── Status Indicators ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0.85rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 8px;
    margin: 0.35rem 0;
    border: 1px solid rgba(255, 255, 255, 0.05);
    font-size: 0.8rem;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}
.dot-active { background: var(--accent-purple); box-shadow: 0 0 10px var(--accent-purple); animation: pulse 1.2s infinite; }
.dot-done   { background: var(--success); box-shadow: 0 0 6px rgba(16, 185, 129, 0.4); }
.dot-pending { background: #374151; }

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
}

/* ── Inputs & Native Overrides ── */
[data-testid="InputInstructions"] {
    display: none !important;
}

[data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: var(--surface-card) !important;
    border: 1px solid var(--surface-border) !important;
    border-radius: 10px !important;
}

[data-testid="stTextInput"] input {
    background-color: transparent !important;
    color: var(--text-primary) !important;
    border: none !important;
    box-shadow: none !important;
}

.stSelectbox > div > div {
    background-color: var(--surface-card) !important;
    border: 1px solid var(--surface-border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent-purple), #6d28d9) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    padding: 0.65rem 1.2rem !important;
    box-shadow: 0 4px 20px var(--accent-glow) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(139, 92, 246, 0.4) !important;
}

/* Streamlit Tabs Customization */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
    border-bottom: 1px solid var(--surface-border);
}

.stTabs [data-baseweb="tab"] {
    height: 42px;
    border-radius: 8px 8px 0px 0px;
    padding: 0 16px;
    background-color: transparent;
    color: var(--text-secondary);
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background-color: var(--surface-card) !important;
    color: var(--accent-cyan) !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
}

/* Scrollbars */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: var(--surface-border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-purple); }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Helpers ────────────────────────────────────────────────────────────────────
def step_status(steps: dict, key: str) -> str:
    s = steps.get(key, "pending")
    if s == "active":  return "dot-active"
    if s == "done":    return "dot-done"
    return "dot-pending"

def render_step_bar(label: str, key: str, icon: str):
    css = step_status(st.session_state.pipeline_steps, key)
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot {css}"></div>
        <span style="font-weight: 500;">{icon} {label}</span>
    </div>""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:1.6rem">🎬 AI Video</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Video Intelligence</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<span class="badge badge-purple">Configuration</span>', unsafe_allow_html=True)

    with st.form("pipeline_form", clear_on_submit=False):
        source = st.text_input("Source URL or File Path", placeholder="YouTube Link or /path/to/file.mp4")
        language = st.selectbox("Language", ["english", "hinglish"], index=0)
        run_btn = st.form_submit_button("⚡ Start Analysis", use_container_width=True)

    if st.session_state.pipeline_done:
        st.markdown("---")
        st.markdown('<span class="badge badge-green">Pipeline Status</span>', unsafe_allow_html=True)
        for step, icon, label in [
            ("audio",      "🔊", "Audio Extraction"),
            ("transcript", "📝", "Transcription"),
            ("title",      "🏷️", "Title Generation"),
            ("summary",    "📋", "Summarization"),
            ("extract",    "🔍", "Insight Extraction"),
            ("rag",        "🧠", "RAG Indexing"),
        ]:
            render_step_bar(label, step, icon)

# ─── Main Header ────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">AI Video Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Transcribe · Summarise · Chat with your videos</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── Run Pipeline ────────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("Please provide a valid YouTube URL or local file path.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_steps = {}

        progress_placeholder = st.empty()

        def update_step(key, state):
            st.session_state.pipeline_steps[key] = state

        try:
            with progress_placeholder.container():
                st.info("⚡ Executing pipeline steps... Monitor live progress in the sidebar.")

            update_step("audio", "active")
            chunks = process_input(source)
            update_step("audio", "done")

            update_step("transcript", "active")
            transcript = transcribe_all(chunks, language)
            update_step("transcript", "done")

            update_step("title", "active")
            title = generate_title(transcript)
            update_step("title", "done")

            update_step("summary", "active")
            summary = summarize(transcript)
            update_step("summary", "done")

            update_step("extract", "active")
            # Called extract_all_insights directly to match imports
            insights = extract_all_insights(transcript)
            update_step("extract", "done")

            update_step("rag", "active")
            rag_chain = build_rag_chain(transcript)
            update_step("rag", "done")

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": insights.get("action_items", "None found"),
                "key_decisions": insights.get("key_decisions", "None found"),
                "open_questions": insights.get("open_questions", "None found"),
                "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            progress_placeholder.success("✅ Analysis Complete!")
            time.sleep(0.5)
            progress_placeholder.empty()
            st.rerun()

        except Exception as e:
            for k in ["audio", "transcript", "title", "summary", "extract", "rag"]:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            progress_placeholder.error(f"❌ Error during execution: {e}")

# ── Render Results ──────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Video Title Banner
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-label">Video Overview</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">
            {r['title']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Multi-tab workspace view
    tab_summary, tab_insights, tab_transcript = st.tabs(["📋 Summary", "💡 Insights & Key Highlights", "📝 Transcript & Exports"])

    with tab_summary:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-label">Key Takeaways & Summary</div>
            <div style="line-height: 1.7; font-size: 0.95rem;">{r['summary']}</div>
        </div>
        """, unsafe_allow_html=True)

    with tab_insights:
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            st.markdown(f"""
            <div class="glass-card" style="height: 100%;">
                <div class="card-label">✅ Action Items</div>
                <div style="font-size: 0.875rem; line-height: 1.6;">{r['action_items']}</div>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="glass-card" style="height: 100%;">
                <div class="card-label">🔑 Key Takeaways</div>
                <div style="font-size: 0.875rem; line-height: 1.6;">{r['key_decisions']}</div>
            </div>""", unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="glass-card" style="height: 100%;">
                <div class="card-label">❓ Open Questions</div>
                <div style="font-size: 0.875rem; line-height: 1.6;">{r['open_questions']}</div>
            </div>""", unsafe_allow_html=True)

    with tab_transcript:
        exp_col1, exp_col2 = st.columns([3, 1])
        with exp_col1:
            st.download_button(
                label="📥 Export Full Transcript (.txt)",
                data=r['transcript'],
                file_name=f"{r['title']}_transcript.txt",
                mime="text/plain",
            )
        with exp_col2:
            notes_content = f"# {r['title']}\n\n## Summary\n{r['summary']}\n\n## Key Takeaways\n{r['action_items']}"
            st.download_button(
                label="📥 Export Video Notes",
                data=notes_content,
                file_name=f"{r['title']}_notes.md",
                mime="text/markdown",
            )

        st.text_area("Full Transcript", value=r["transcript"], height=300, disabled=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Interactive RAG Chat ──────────────────────────────────────────────────
    st.markdown('<div style="font-size:1.3rem; font-weight:700; margin-bottom: 0.5rem;">💬 Chat with your Video</div>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.info("💡 Ask questions directly to query anything discussed in the video.")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask anything about this video..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing video content..."):
                answer = ask_question(r["rag_chain"], prompt)
                st.write(answer)

        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

else:
    # Empty Initial State Screen
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding: 4rem 2rem; margin-top: 2rem;">
        <div style="font-size: 3.5rem; margin-bottom: 1rem;">🎬</div>
        <div style="font-size: 1.4rem; font-weight: 700; margin-bottom: 0.5rem;">
            Ready to Analyze Your Video
        </div>
        <div style="color: var(--text-secondary); font-size: 0.9rem; max-width: 440px; margin: 0 auto 1.5rem auto; line-height: 1.6;">
            Paste a YouTube URL or a path to a local audio/video file in the sidebar to extract takeaways and chat with the video's content.
        </div>
        <div style="display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap;">
            <span class="badge badge-purple">Transcription</span>
            <span class="badge badge-cyan">Summarisation</span>
            <span class="badge badge-green">RAG Q&A</span>
        </div>
    </div>
    """, unsafe_allow_html=True)