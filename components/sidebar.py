import streamlit as st
from pathlib import Path

def apply_theme():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root{--navy:#07111F;--panel:#0B192B;--blue:#4F82FF;--violet:#875DFF;--cyan:#28D6EF;--muted:#94A3B8}
    .stApp{background:radial-gradient(ellipse at 75% 0%,#12203a 0%,#07111F 45%);color:#EDF3FF;font-family:'DM Sans',sans-serif}
    h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;letter-spacing:-.025em}
    [data-testid="stSidebar"]{background:#0B192B;border-right:1px solid #1b2d47}
    [data-testid="stMetric"]{background:#0B192B;border:1px solid #20334f;padding:18px;border-radius:14px}
    div[data-testid="stVerticalBlockBorderWrapper"]{border-color:#20334f!important}
    .hero{padding:28px 4px 20px}.hero h1{font-size:2.65rem;line-height:1.1;margin:.35rem 0 1rem}.hero h1 span{color:#72a0ff}.hero p{color:#A9B8CC;font-size:1.05rem;max-width:760px}.eyebrow{font-size:.72rem;font-weight:700;letter-spacing:.16em;color:#28D6EF}
    .metric{background:linear-gradient(145deg,#10223a,#0B192B);border:1px solid #20334f;border-radius:15px;padding:18px 20px;min-height:100px}.metric div{color:#9EB0C8;font-size:.88rem}.metric strong{display:block;font-family:'Space Grotesk';font-size:2rem;margin-top:6px;color:#f3f7ff}
    .source-card{background:#0B192B;border:1px solid #263b58;border-radius:12px;padding:14px 16px;margin:8px 0}.source-meta{color:#91a7c4;font-size:.8rem}.small-muted{color:#91a7c4;font-size:.88rem}
    .stButton>button{border-radius:10px;border:1px solid #36558a;background:linear-gradient(100deg,#315ed8,#6545c7);color:white;font-weight:600}.stButton>button:hover{border-color:#7da0ff;color:white}
    input,textarea,[data-baseweb="select"]{background-color:#0b192b!important}
    </style>""",unsafe_allow_html=True)

def sidebar():
    with st.sidebar:
        st.markdown('## 🧠 DocuMind AI')
        st.caption('Document intelligence workspace')
        st.divider()
        pages=[('01 Dashboard','app.py'),('02 Upload Documents','pages/02_Upload_Documents.py'),('03 Document Library','pages/03_Document_Library.py'),('04 Document Reader','pages/04_Document_Reader.py'),('05 AI Summarizer','pages/05_AI_Summarizer.py'),('06 Ask Your Documents','pages/06_Ask_Your_Documents.py'),('07 Semantic Search','pages/07_Semantic_Search.py'),('08 Document Insights','pages/08_Document_Insights.py'),('09 History & Reports','pages/09_History_Reports.py'),('10 Settings & Status','pages/10_Settings_Status.py')]
        for label,path in pages:
            if st.button(label,use_container_width=True,key='nav_'+path):
                if path=='app.py': st.switch_page('app.py')
                else: st.switch_page(path)
        st.divider(); st.caption('Local-first • SQLite storage • Optional Gemini')
