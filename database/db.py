import sqlite3
from pathlib import Path
from contextlib import contextmanager
BASE=Path(__file__).resolve().parents[1]
DATA=BASE/'data'; UPLOADS=DATA/'uploads'; DB_PATH=DATA/'documind.sqlite3'
UPLOADS.mkdir(parents=True,exist_ok=True)
SCHEMA="""
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY, display_name TEXT NOT NULL, stored_name TEXT NOT NULL, file_type TEXT NOT NULL, file_size INTEGER NOT NULL, sha256 TEXT NOT NULL UNIQUE, page_count INTEGER, status TEXT NOT NULL, error TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS chunks(id INTEGER PRIMARY KEY AUTOINCREMENT, document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE, chunk_index INTEGER NOT NULL, content TEXT NOT NULL, source_ref TEXT, UNIQUE(document_id,chunk_index));
CREATE INDEX IF NOT EXISTS idx_chunks_document ON chunks(document_id);
CREATE TABLE IF NOT EXISTS conversations(id TEXT PRIMARY KEY, title TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS messages(id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT REFERENCES conversations(id) ON DELETE CASCADE, role TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS citations(id INTEGER PRIMARY KEY AUTOINCREMENT, message_id INTEGER REFERENCES messages(id) ON DELETE CASCADE, chunk_id INTEGER REFERENCES chunks(id) ON DELETE SET NULL, quote TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS activities(id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT NOT NULL, detail TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS summaries(id INTEGER PRIMARY KEY AUTOINCREMENT, document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE, style TEXT NOT NULL, content TEXT NOT NULL, method TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS searches(id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT NOT NULL, result_count INTEGER NOT NULL, created_at TEXT NOT NULL);
"""
@contextmanager
def connect():
    conn=sqlite3.connect(DB_PATH,timeout=15); conn.row_factory=sqlite3.Row; conn.execute('PRAGMA foreign_keys=ON')
    try: yield conn; conn.commit()
    finally: conn.close()
def init_db():
    with connect() as c: c.executescript(SCHEMA)
def log_activity(action,detail):
    from datetime import datetime,timezone
    with connect() as c: c.execute('INSERT INTO activities(action,detail,created_at) VALUES(?,?,?)',(action,detail,datetime.now(timezone.utc).isoformat(timespec='seconds')))
