import streamlit as st
from components.sidebar import apply_theme,sidebar
from services.repository import get_documents,get_chunks
st.set_page_config(page_title='Document Reader • DocuMind AI',layout='wide'); apply_theme(); sidebar(); st.title('Document reader')
docs=get_documents()
if not docs: st.info('Upload a document first.'); st.stop()
ids=[d['id'] for d in docs]; default=ids.index(st.session_state['selected_doc_id']) if st.session_state.get('selected_doc_id') in ids else 0
sel=st.selectbox('Choose document',ids,index=default,format_func=lambda x:next(d['display_name'] for d in docs if d['id']==x)); chunks=get_chunks(sel); term=st.text_input('Find in document')
if not chunks: st.warning('No extracted text is available for this document.'); st.stop()
for ch in chunks:
    text=ch['content']; found=not term or term.lower() in text.lower()
    if found:
        with st.container(border=True): st.caption(f"{ch.get('source_ref') or 'Section'} · Chunk {ch['chunk_index']+1}"); st.write(text)
