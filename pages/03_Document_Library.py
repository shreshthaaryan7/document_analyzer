import streamlit as st
from components.sidebar import apply_theme,sidebar
from services.repository import get_documents,rename_document,delete_document
from database.db import UPLOADS
st.set_page_config(page_title='Document Library • DocuMind AI',layout='wide'); apply_theme(); sidebar(); st.title('Document library')
docs=get_documents(); q=st.text_input('Search document names'); typ=st.selectbox('File type',['All','PDF','DOCX','TXT']); status=st.selectbox('Status',['All','processed','error'])
docs=[d for d in docs if q.lower() in d['display_name'].lower() and (typ=='All' or d['file_type'].upper()==typ) and (status=='All' or d['status']==status)]
sort=st.selectbox('Sort by',['Newest','Name A–Z','Largest file','Most pages'])
if sort=='Name A–Z': docs.sort(key=lambda d:d['display_name'].lower())
elif sort=='Largest file': docs.sort(key=lambda d:d['file_size'],reverse=True)
elif sort=='Most pages': docs.sort(key=lambda d:d['page_count'] or 0,reverse=True)
if not docs: st.info('No documents match your filters. Upload a file or change the filters.')
for d in docs:
    with st.container(border=True):
        a,b,c=st.columns([4,2,2]); a.markdown(f"**{d['display_name']}**  ·  `{d['file_type'].upper()}`"); a.caption(f"{d['file_size']:,} bytes • {d['page_count'] or 'N/A'} pages • {d['created_at'][:19]}"); b.write(f"Status: **{d['status']}**")
        with c:
            with st.popover('Manage'):
                new=st.text_input('Display name',value=d['display_name'],key='rename_'+d['id'])
                if st.button('Save name',key='save_'+d['id']):
                    if new.strip(): rename_document(d['id'],new.strip()); st.success('Name updated.'); st.rerun()
                path=UPLOADS/d['stored_name']
                if path.exists(): st.download_button('Download original',path.read_bytes(),file_name=d['display_name'],key='dl_'+d['id'])
                if st.checkbox('Confirm deletion',key='confirm_'+d['id']):
                    if st.button('Delete document and indexed text',key='delete_'+d['id']): delete_document(d['id']); st.success('Document deleted.'); st.rerun()
        if st.button('Read extracted text',key='read_'+d['id']): st.session_state['selected_doc_id']=d['id']; st.switch_page('pages/04_Document_Reader.py')
