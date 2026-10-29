import re, math
from collections import Counter
from services.repository import get_chunks
TOKEN=re.compile(r"[A-Za-z0-9][A-Za-z0-9'-]{1,}")
STOP=set('the a an and or but if then is are was were be been being to of in on for with as by at from it its this that these those we they their you your can could should would may might not no do does did have has had into about than also such'.split())
def tokens(text): return [x.lower() for x in TOKEN.findall(text) if x.lower() not in STOP]
def search_chunks(query,doc_ids=None,limit=8):
    chunks=get_chunks(); terms=tokens(query)
    if doc_ids: chunks=[c for c in chunks if c['document_id'] in doc_ids]
    if not chunks or not terms: return []
    qset=set(terms); scored=[]
    for ch in chunks:
        ts=tokens(ch['content']); counts=Counter(ts)
        overlap=sum(counts[t] for t in qset)
        if not overlap: continue
        coverage=len(qset.intersection(counts))/max(1,len(qset))
        density=overlap/max(1,len(ts))
        score=0.75*coverage+0.25*min(1,density*8)
        scored.append({**ch,'score':round(score,3)})
    scored.sort(key=lambda x:(x['score'],len(x['content'])),reverse=True)
    return scored[:limit]
def evidence_answer(question,results):
    if not results or results[0]['score']<0.12:
        return 'I could not find enough supporting evidence in the selected documents to answer that question. Try different wording or upload a relevant document.'
    # Conservative fallback: report retrieved excerpts instead of inventing a generative answer.
    lines=['I found the following potentially relevant evidence. This local fallback retrieves passages; it does not generate a verified natural-language conclusion:']
    for i,r in enumerate(results[:3],1): lines.append(f"\n[{i}] {r['display_name']} — {r.get('source_ref') or 'Section'}\n{r['content'][:650]}")
    return '\n'.join(lines)
