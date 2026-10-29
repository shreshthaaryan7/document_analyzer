import re

def chunk_pages(pages, max_chars=1100, overlap=160):
    if max_chars<200 or overlap<0 or overlap>=max_chars: raise ValueError('Use max_chars >= 200 and overlap smaller than max_chars.')
    out=[]
    for page in pages:
        text=re.sub(r'[ \t]+',' ',page['text']).strip()
        if not text: continue
        start=0
        while start<len(text):
            end=min(start+max_chars,len(text))
            if end<len(text):
                boundary=max(text.rfind('. ',start,end),text.rfind('\n',start,end),text.rfind(' ',start,end))
                if boundary>start+max_chars//2: end=boundary+1
            part=text[start:end].strip()
            if part: out.append({'content':part,'source_ref':page.get('source_ref','Section')})
            if end>=len(text): break
            start=max(end-overlap,start+1)
    return out
