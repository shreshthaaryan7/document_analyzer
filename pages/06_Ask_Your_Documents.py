import streamlit as st
from components.sidebar import apply_theme,sidebar
from services.repository import get_documents,save_search
from services.retrieval import search_chunks,evidence_answer
st.set_page_config(page_title='Ask Your Documents • DocuMind AI',layout='wide'); apply_theme(); sidebar(); st.title('Ask your documents'); st.write('Answers are grounded in retrieved passages. Local mode presents evidence excerpts rather than inventing a generated answer.')
docs=get_documents()
if not docs: st.info('Upload documents before asking a question.'); st.stop()
selected=st.multiselect('Search within documents',[d['id'] for d in docs],default=[d['id'] for d in docs],format_func=lambda x:next(d['display_name'] for d in docs if d['id']==x))
with st.form('ask_form'):
    q=st.text_area('What would you like to know?',placeholder='Ask a question grounded in your uploaded documents…')
    submit=st.form_submit_button('Find evidence',type='primary')
if submit:
    if not q.strip(): st.warning('Enter a question first.')
    else:
        results=search_chunks(q,selected,limit=5); save_search(q,len(results)); st.session_state['last_answer']=evidence_answer(q,results); st.session_state['last_evidence']=results
if st.session_state.get('last_answer'):
    st.subheader('Response'); st.write(st.session_state['last_answer'])
    if st.session_state.get('last_evidence'):
        st.subheader('Retrieved sources')
        for r in st.session_state['last_evidence']:
            with st.container(border=True): st.caption(f"{r['display_name']} · {r.get('source_ref') or 'Section'} · lexical relevance {r['score']:.3f}"); st.write(r['content'])
