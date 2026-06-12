import streamlit as st
from utils import build_index, get_relevant_chunks, ask_gemini, chat_with_gemini
import os

st.set_page_config(
    page_title="DocMind AI",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; }
    section[data-testid="stSidebar"] { background: rgba(255,255,255,0.05) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255,255,255,0.1); }
    .hero { text-align: center; padding: 60px 20px 40px; }
    .hero-icon { font-size: 64px; margin-bottom: 16px; }
    .hero-title { font-size: 48px; font-weight: 700; background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; }
    .hero-sub { font-size: 18px; color: rgba(255,255,255,0.5); margin-bottom: 40px; }
    .info-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 20px 28px; text-align: center; color: rgba(255,255,255,0.7); font-size: 15px; backdrop-filter: blur(10px); }
    .user-bubble { background: linear-gradient(135deg, #6d28d9, #4f46e5); color: white; padding: 14px 20px; border-radius: 18px 18px 4px 18px; margin: 8px 0; max-width: 75%; margin-left: auto; font-size: 15px; line-height: 1.5; box-shadow: 0 4px 15px rgba(109,40,217,0.3); }
    .ai-bubble { background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.9); padding: 14px 20px; border-radius: 18px 18px 18px 4px; margin: 8px 0; max-width: 75%; font-size: 15px; line-height: 1.5; }
    .mode-active { background: linear-gradient(135deg, #6d28d9, #4f46e5) !important; color: white !important; border: none !important; border-radius: 10px !important; }
    .stat-box { background: linear-gradient(135deg, rgba(109,40,217,0.3), rgba(79,70,229,0.3)); border: 1px solid rgba(109,40,217,0.4); border-radius: 12px; padding: 14px; text-align: center; margin-top: 16px; }
    .stat-number { font-size: 28px; font-weight: 700; color: #a78bfa; }
    .stat-label { font-size: 12px; color: rgba(255,255,255,0.4); }
    .label { font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: rgba(255,255,255,0.35); margin-bottom: 6px; }
    div[data-testid="stTextInput"] input { background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 10px !important; color: white !important; }
    div[data-testid="stFileUploader"] { background: rgba(255,255,255,0.04) !important; border: 1.5px dashed rgba(167,139,250,0.4) !important; border-radius: 12px !important; }
    div[data-testid="stChatInput"] textarea { background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 14px !important; color: white !important; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div style="font-size:22px;font-weight:700;color:white;margin-bottom:4px">🧠 DocMind AI</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:rgba(255,255,255,0.4);margin-bottom:24px">Your intelligent AI assistant</div>', unsafe_allow_html=True)

    st.markdown('<div class="label">Gemini API Key</div>', unsafe_allow_html=True)
    api_key = st.text_input("", placeholder="Paste your API key...", type="password", label_visibility="collapsed")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.success("✅ API key saved!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Mode selector
    st.markdown('<div class="label">Mode</div>', unsafe_allow_html=True)
    mode = st.radio("", ["💬 Chat", "📄 PDF Chat"], label_visibility="collapsed")

    if mode == "📄 PDF Chat":
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="label">Upload PDF</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
        if uploaded_file and api_key:
            with st.spinner("Indexing..."):
                num_chunks = build_index(uploaded_file)
            st.markdown(f'<div class="stat-box"><div class="stat-number">{num_chunks}</div><div class="stat-label">chunks indexed</div></div>', unsafe_allow_html=True)
            st.markdown(f"<br>📄 **{uploaded_file.name}**")
    else:
        uploaded_file = None

    st.markdown("---")
    st.markdown('<div style="color:rgba(255,255,255,0.3);font-size:12px;">Built with Gemini · LangChain · HNSWlib</div>', unsafe_allow_html=True)

# Main area
if not api_key:
    st.markdown("""
    <div class="hero">
        <div class="hero-icon">🧠</div>
        <div class="hero-title">DocMind AI</div>
        <div class="hero-sub">Your all-in-one AI assistant — chat freely or talk to your PDFs</div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="info-card"><div style="font-size:32px;margin-bottom:10px">💬</div><div style="color:white;font-weight:600;margin-bottom:6px">AI Chat</div><div>Chat freely like ChatGPT — ask anything</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-card"><div style="font-size:32px;margin-bottom:10px">📄</div><div style="color:white;font-weight:600;margin-bottom:6px">PDF Chat</div><div>Upload any PDF and ask questions about it</div></div>', unsafe_allow_html=True)

else:
    # Initialize separate chat histories
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = []

    if mode == "💬 Chat":
        st.markdown('<div style="max-width:800px;margin:0 auto;padding:20px">', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;padding:20px 0;background:linear-gradient(90deg,#a78bfa,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:28px;font-weight:700">💬 AI Chat</div>', unsafe_allow_html=True)

        if not st.session_state.chat_messages:
            st.markdown('<div style="text-align:center;color:rgba(255,255,255,0.4);padding:40px 0">Ask me anything — I\'m your AI assistant!</div>', unsafe_allow_html=True)

        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-bubble">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-bubble">🧠 {msg["content"]}</div>', unsafe_allow_html=True)

        if prompt := st.chat_input("Ask me anything..."):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            st.markdown(f'<div class="user-bubble">👤 {prompt}</div>', unsafe_allow_html=True)
            with st.spinner("Thinking..."):
                response = chat_with_gemini(st.session_state.chat_messages)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.markdown(f'<div class="ai-bubble">🧠 {response}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    else:  # PDF Chat mode
        st.markdown('<div style="max-width:800px;margin:0 auto;padding:20px">', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;padding:20px 0;background:linear-gradient(90deg,#a78bfa,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:28px;font-weight:700">📄 PDF Chat</div>', unsafe_allow_html=True)

        if not uploaded_file:
            st.markdown('<div style="text-align:center;color:rgba(255,255,255,0.4);padding:40px 0">👈 Upload a PDF from the sidebar to get started</div>', unsafe_allow_html=True)
        else:
            if not st.session_state.pdf_messages:
                st.markdown('<div style="text-align:center;color:rgba(255,255,255,0.4);padding:20px 0">Document ready! Ask me anything about it.</div>', unsafe_allow_html=True)

            for msg in st.session_state.pdf_messages:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-bubble">👤 {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-bubble">🧠 {msg["content"]}</div>', unsafe_allow_html=True)

            if prompt := st.chat_input("Ask about your PDF..."):
                st.session_state.pdf_messages.append({"role": "user", "content": prompt})
                st.markdown(f'<div class="user-bubble">👤 {prompt}</div>', unsafe_allow_html=True)
                with st.spinner("Thinking..."):
                    context = get_relevant_chunks(prompt)
                    response = ask_gemini(prompt, context)
                st.session_state.pdf_messages.append({"role": "assistant", "content": response})
                st.markdown(f'<div class="ai-bubble">🧠 {response}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)