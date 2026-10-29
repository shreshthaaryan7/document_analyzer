from database.db import connect, log_activity
from datetime import datetime,timezone

def dashboard_stats():
    with connect() as c:
        docs=c.execute('SELECT COUNT(*) n FROM documents').fetchone()['n']
        processed=c.execute("SELECT COUNT(*) n FROM documents WHERE status='processed'").fetchone()['n']
        pages=c.execute('SELECT COALESCE(SUM(page_count),0) n FROM documents').fetchone()['n']
        chunks=c.execute('SELECT COUNT(*) n FROM chunks').fetchone()['n']
    return {'documents':docs,'processed':processed,'pages':pages,'chunks':chunks}
def recent_documents(limit=10):
    with connect() as c: return [dict(r) for r in c.execute('SELECT * FROM documents ORDER BY created_at DESC LIMIT ?',(limit,)).fetchall()]
def get_documents():
    with connect() as c: return [dict(r) for r in c.execute('SELECT * FROM documents ORDER BY created_at DESC').fetchall()]
def get_document(doc_id):
    with connect() as c:
        r=c.execute('SELECT * FROM documents WHERE id=?',(doc_id,)).fetchone(); return dict(r) if r else None
def get_chunks(doc_id=None):
    with connect() as c:
        if doc_id: rows=c.execute('SELECT c.*,d.display_name FROM chunks c JOIN documents d ON d.id=c.document_id WHERE c.document_id=? ORDER BY c.chunk_index',(doc_id,)).fetchall()
        else: rows=c.execute('SELECT c.*,d.display_name FROM chunks c JOIN documents d ON d.id=c.document_id ORDER BY c.id').fetchall()
        return [dict(r) for r in rows]
def recent_activities(limit=10):
    with connect() as c: return [dict(r) for r in c.execute('SELECT action,detail,created_at FROM activities ORDER BY id DESC LIMIT ?',(limit,)).fetchall()]
def save_summary(doc_id,style,content,method):
    with connect() as c: c.execute('INSERT INTO summaries(document_id,style,content,method,created_at) VALUES(?,?,?,?,?)',(doc_id,style,content,method,datetime.now(timezone.utc).isoformat(timespec='seconds')))
    log_activity('Summary generated',f'{style} summary for {doc_id}')
def save_search(query,count):
    with connect() as c: c.execute('INSERT INTO searches(query,result_count,created_at) VALUES(?,?,?)',(query,count,datetime.now(timezone.utc).isoformat(timespec='seconds')))
    log_activity('Search',f'Query: {query[:100]} ({count} results)')
def delete_document(doc_id):
    with connect() as c:
        r=c.execute('SELECT display_name,stored_name FROM documents WHERE id=?',(doc_id,)).fetchone()
        if not r: return None
        c.execute('DELETE FROM documents WHERE id=?',(doc_id,))
    from database.db import UPLOADS
    (UPLOADS/r['stored_name']).unlink(missing_ok=True)
    log_activity('Document deleted',r['display_name']); return r['display_name']
def rename_document(doc_id,name):
    with connect() as c: c.execute('UPDATE documents SET display_name=?,updated_at=? WHERE id=?',(name,datetime.now(timezone.utc).isoformat(timespec='seconds'),doc_id))
    log_activity('Document renamed',name)
