import os,sys,sqlite3
import streamlit as st
from components.sidebar import apply_theme,sidebar
from database.db import DB_PATH,UPLOADS,connect
st.set_page_config(page_title='Settings & Status • DocuMind AI',layout='wide'); apply_theme(); sidebar(); st.title('Settings & system status')
st.write('Local application diagnostics and privacy controls.')
with connect() as c:
    db_ok=c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'; docs=c.execute('SELECT COUNT(*) FROM documents').fetchone()[0]; chunks=c.execute('SELECT COUNT(*) FROM chunks').fetchone()[0]
for label,value in [('Python',sys.version.split()[0]),('SQLite database','Healthy' if db_ok else 'Integrity check failed'),('Database file',str(DB_PATH)),('Upload directory',str(UPLOADS)),('Documents stored',docs),('Indexed chunks',chunks),('Gemini API key','Configured' if os.getenv('GEMINI_API_KEY') else 'Not configured (local mode)')]:
    with st.container(border=True): st.markdown(f'**{label}**'); st.code(str(value))
st.subheader('Privacy and limitations')
st.markdown('- Uploaded files, extracted chunks, history, and summaries are stored locally in the project data directory.\n- Current default search uses lexical ranking; it is not embedding-based semantic search.\n- Summaries are extractive and local. Generative Gemini features are not active in this build.\n- Do not store sensitive documents on a shared or untrusted computer.\n- Deleting a document removes its stored file and database chunks.')
if st.button('Rebuild chunks from stored files',type='secondary'):
    from services.document_parser import extract_document
    from services.text_chunker import chunk_pages
    with connect() as c:
        rows=[dict(r) for r in c.execute('SELECT * FROM documents')]
    success=0; errors=[]
    for d in rows:
        try:
            data=(UPLOADS/d['stored_name']).read_bytes(); pages,count=extract_document(data,d['file_type']); chunks=chunk_pages(pages)
            with connect() as c:
                c.execute('DELETE FROM chunks WHERE document_id=?',(d['id'],)); c.executemany('INSERT INTO chunks(document_id,chunk_index,content,source_ref) VALUES(?,?,?,?)',[(d['id'],i,ch['content'],ch['source_ref']) for i,ch in enumerate(chunks)])
            success+=1
        except Exception as e: errors.append(f"{d['display_name']}: {e}")
    st.success(f'Rebuilt chunks for {success} document(s).')
    for e in errors: st.error(e)
