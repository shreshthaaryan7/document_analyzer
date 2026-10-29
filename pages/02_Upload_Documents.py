import streamlit as st
from components.sidebar import apply_theme,sidebar
from services.ingestion import ingest
st.set_page_config(page_title='Upload Documents • DocuMind AI',layout='wide'); apply_theme(); sidebar()
st.title('Upload documents'); st.write('Import PDF, DOCX, and TXT files. Extracted text is stored locally in your workspace.')
st.caption('Maximum file size: 20 MB per file. Scanned PDFs without selectable text are not OCR-processed.')
files=st.file_uploader('Choose one or more files',type=['pdf','docx','txt'],accept_multiple_files=True)
if st.button('Process selected files',type='primary',disabled=not files):
    for f in files:
        with st.status(f'Processing {f.name}…',expanded=True) as status:
            try:
                result=ingest(f); status.update(label=f"Processed {f.name}",state='complete'); st.success(f"{result['name']}: {result['chunks']} searchable chunks created.")
            except Exception as e: status.update(label=f'Could not process {f.name}',state='error'); st.error(str(e))
st.info('Privacy: files remain on this computer. The current local retrieval and extractive summary features do not send documents to an external AI provider.')
