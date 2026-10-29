import streamlit as st
from components.sidebar import apply_theme, sidebar
from database.db import init_db

st.set_page_config(page_title="DocuMind AI", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")
init_db(); apply_theme(); sidebar()
st.markdown('<div class="hero"><div class="eyebrow">DOCUMENT INTELLIGENCE WORKSPACE</div><h1>Understand your documents.<br><span>Find answers with evidence.</span></h1><p>Upload files, explore source passages, summarize content, and search your knowledge base.</p></div>', unsafe_allow_html=True)
from services.repository import dashboard_stats, recent_documents, recent_activities
stats=dashboard_stats()
cols=st.columns(4)
for c,(label,value) in zip(cols,[('Documents',stats['documents']),('Processed',stats['processed']),('PDF pages',stats['pages']),('Text chunks',stats['chunks'])]):
    c.markdown(f'<div class="metric"><div>{label}</div><strong>{value}</strong></div>',unsafe_allow_html=True)
st.subheader('Quick actions')
a,b,c=st.columns(3)
with a:
    st.markdown('**⬆️ Upload documents**\n\nAdd PDF, DOCX, or TXT files to your workspace.')
    if st.button('Open uploader', use_container_width=True): st.switch_page('pages/02_Upload_Documents.py')
with b:
    st.markdown('**💬 Ask your documents**\n\nAsk evidence-based questions across your files.')
    if st.button('Ask a question', use_container_width=True): st.switch_page('pages/06_Ask_Your_Documents.py')
with c:
    st.markdown('**⌕ Search knowledge**\n\nFind passages using lexical relevance scoring.')
    if st.button('Search documents', use_container_width=True): st.switch_page('pages/07_Semantic_Search.py')
st.subheader('Recent documents')
docs=recent_documents(6)
if docs:
    st.dataframe([{'Name':d['display_name'],'Type':d['file_type'].upper(),'Status':d['status'],'Pages':d['page_count'] or '—','Uploaded':d['created_at']} for d in docs],use_container_width=True,hide_index=True)
else: st.info('Your workspace is empty. Upload a document to start building your searchable library.')
st.subheader('Recent activity')
acts=recent_activities(6)
if acts: st.dataframe(acts,use_container_width=True,hide_index=True)
else: st.caption('Activity will appear here as you upload, search, summarize, and ask questions.')
