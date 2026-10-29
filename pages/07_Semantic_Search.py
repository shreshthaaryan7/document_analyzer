import streamlit as st
from components.sidebar import apply_theme,sidebar
from services.repository import get_documents,save_search
from services.retrieval import search_chunks
st.set_page_config(page_title='Semantic Search • DocuMind AI',layout='wide'); apply_theme(); sidebar(); st.title('Search your knowledge'); st.caption('Current default: local lexical retrieval using token overlap and term density. Scores are ranking signals, not confidence percentages.')
docs=get_documents()
if not docs: st.info('Upload documents to make them searchable.'); st.stop()
selected=st.multiselect('Limit to documents',[d['id'] for d in docs],default=[d['id'] for d in docs],format_func=lambda x:next(d['display_name'] for d in docs if d['id']==x))
with st.form('search_form'):
    query=st.text_input('Search by question, phrase, or topic',placeholder='e.g. What are the main project objectives?'); go=st.form_submit_button('Search',type='primary')
if go:
    results=search_chunks(query,selected,limit=12) if query.strip() else []; save_search(query,len(results)); st.session_state['search_results']=results
if 'search_results' in st.session_state:
    results=st.session_state['search_results']
    if not results: st.info('No matching passages found. Try alternate wording or add more documents.')
    for r in results:
        with st.container(border=True): st.markdown(f"**{r['display_name']}** · {r.get('source_ref') or 'Section'} · similarity/ranking score `{r['score']:.3f}`"); st.write(r['content'])
