import hashlib, uuid
from datetime import datetime,timezone
from database.db import connect,UPLOADS
from services.document_parser import extract_document
from services.text_chunker import chunk_pages
from services.repository import log_activity
MAX_BYTES=20*1024*1024

def ingest(uploaded_file):
    name=uploaded_file.name; ext=name.rsplit('.',1)[-1].lower() if '.' in name else ''
    if ext not in {'pdf','docx','txt'}: raise ValueError('Unsupported file type. Choose PDF, DOCX, or TXT.')
    data=uploaded_file.getvalue()
    if not data: raise ValueError('The uploaded file is empty.')
    if len(data)>MAX_BYTES: raise ValueError('File exceeds the 20 MB upload limit.')
    digest=hashlib.sha256(data).hexdigest()
    with connect() as c:
        if c.execute('SELECT 1 FROM documents WHERE sha256=?',(digest,)).fetchone(): raise ValueError('This exact file is already in your library.')
    pages,page_count=extract_document(data,ext); chunks=chunk_pages(pages)
    if not chunks: raise ValueError('No searchable text could be extracted.')
    doc_id=uuid.uuid4().hex; stored=f'{doc_id}.{ext}'; now=datetime.now(timezone.utc).isoformat(timespec='seconds')
    (UPLOADS/stored).write_bytes(data)
    try:
        with connect() as c:
            c.execute('INSERT INTO documents(id,display_name,stored_name,file_type,file_size,sha256,page_count,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)',(doc_id,name,stored,ext,len(data),digest,page_count,'processed',now,now))
            c.executemany('INSERT INTO chunks(document_id,chunk_index,content,source_ref) VALUES(?,?,?,?)',[(doc_id,i,ch['content'],ch['source_ref']) for i,ch in enumerate(chunks)])
    except Exception:
        (UPLOADS/stored).unlink(missing_ok=True); raise
    log_activity('Document uploaded',f'{name} • {len(chunks)} chunks')
    return {'id':doc_id,'name':name,'pages':page_count,'chunks':len(chunks)}
