import streamlit as st
from components.sidebar import apply_theme,sidebar
from services.repository import get_documents,get_chunks,save_summary
from services.summarizer import summarize
st.set_page_config(page_title='AI Summarizer • DocuMind AI',layout='wide'); apply_theme(); sidebar(); st.title('Document summarizer')
docs=get_documents()
if not docs: st.info('Upload a document to generate a summary.'); st.stop()
sel=st.selectbox('Document',[d['id'] for d in docs],format_func=lambda x:next(d['display_name'] for d in docs if d['id']==x)); style=st.radio('Summary style',['Concise','Detailed','Executive'],horizontal=True)
if st.button('Generate summary',type='primary'):
    text='\n'.join(c['content'] for c in get_chunks(sel)); result,method=summarize(text,style); st.session_state['summary_result']=result; st.session_state['summary_method']=method; st.session_state['summary_doc']=sel; save_summary(sel,style,result,method)
if st.session_state.get('summary_result') and st.session_state.get('summary_doc')==sel:
    st.caption('Method: '+st.session_state['summary_method']); st.markdown(st.session_state['summary_result']); st.download_button('Download Markdown',st.session_state['summary_result'],file_name='documind-summary.md',mime='text/markdown')
    st.info('This offline version uses extractive sentence ranking. It is not a generative AI model. Optional Gemini integration is documented for future configuration.')
