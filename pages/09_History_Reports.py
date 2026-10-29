import streamlit as st
from components.sidebar import apply_theme,sidebar
from services.repository import recent_activities
from services.report_export import documents_csv,activity_json,chunks_markdown
from database.db import connect
st.set_page_config(page_title='History & Reports • DocuMind AI',layout='wide'); apply_theme(); sidebar(); st.title('History & reports')
st.subheader('Activity'); acts=recent_activities(200)
if acts: st.dataframe(acts,use_container_width=True,hide_index=True)
else: st.info('No activity recorded yet.')
a,b,c=st.columns(3)
with a: st.download_button('Export document inventory CSV',documents_csv(),file_name='documind-documents.csv',mime='text/csv',use_container_width=True)
with b: st.download_button('Export activity JSON',activity_json(),file_name='documind-activity.json',mime='application/json',use_container_width=True)
with c: st.download_button('Export extracted text Markdown',chunks_markdown(),file_name='documind-extracted-text.md',mime='text/markdown',use_container_width=True)
with connect() as conn:
    summaries=[dict(r) for r in conn.execute('SELECT s.style,s.method,s.created_at,d.display_name,s.content FROM summaries s JOIN documents d ON d.id=s.document_id ORDER BY s.id DESC LIMIT 50')]
st.subheader('Saved summaries')
if summaries: st.dataframe([{'Document':s['display_name'],'Style':s['style'],'Method':s['method'],'Created':s['created_at']} for s in summaries],use_container_width=True,hide_index=True)
else: st.caption('Generated summaries will be recorded here.')
