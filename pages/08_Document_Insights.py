import streamlit as st
import pandas as pd
from components.sidebar import apply_theme,sidebar
from services.repository import get_documents,get_chunks
from services.insights import analyze
st.set_page_config(page_title='Document Insights • DocuMind AI',layout='wide'); apply_theme(); sidebar(); st.title('Document insights')
docs=get_documents()
if not docs: st.info('Upload a document to analyze it.'); st.stop()
sel=st.selectbox('Document',[d['id'] for d in docs],format_func=lambda x:next(d['display_name'] for d in docs if d['id']==x)); text='\n'.join(c['content'] for c in get_chunks(sel))
if not text.strip(): st.warning('This document has no usable extracted text.'); st.stop()
a=analyze(text); cols=st.columns(4)
for col,(label,val) in zip(cols,[('Words',a['words']),('Characters',a['characters']),('Sentences',a['sentences']),('Paragraphs',a['paragraphs'])]): col.metric(label,val)
st.subheader('Frequent meaningful terms'); terms=pd.DataFrame(a['terms'],columns=['Term','Frequency'])
if not terms.empty: st.bar_chart(terms.set_index('Term'))
st.caption('Method: simple token-frequency analysis with a small stop-word list. This is descriptive text analysis, not a trained topic model or named-entity model.')
st.dataframe(terms,use_container_width=True,hide_index=True)
