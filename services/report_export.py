import csv,io,json
from services.repository import get_documents,recent_activities,get_chunks

def documents_csv():
    rows=get_documents(); out=io.StringIO(); fields=['id','display_name','file_type','file_size','page_count','status','created_at']
    w=csv.DictWriter(out,fieldnames=fields); w.writeheader()
    for r in rows: w.writerow({k:r.get(k) for k in fields})
    return out.getvalue()
def activity_json(): return json.dumps(recent_activities(500),indent=2,ensure_ascii=False)
def chunks_markdown():
    chunks=get_chunks(); return '\n\n'.join(f"## {x['display_name']} — {x.get('source_ref') or 'Section'}\n\n{x['content']}" for x in chunks)
