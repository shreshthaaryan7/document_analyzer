from collections import Counter
from services.retrieval import tokens
import re

def summarize(text,style='Concise'):
    sentences=[s.strip() for s in re.split(r'(?<=[.!?])\s+',text) if len(s.strip())>25]
    if not sentences: return 'Not enough readable text to summarize.', 'rule-based extractive'
    words=tokens(text); freq=Counter(words)
    ranked=[]
    for i,s in enumerate(sentences):
        ts=tokens(s); score=sum(freq[t] for t in ts)/max(1,len(ts))
        ranked.append((score,i,s))
    count={'Concise':3,'Detailed':7,'Executive':4}.get(style,3)
    chosen=sorted(sorted(ranked,reverse=True)[:count],key=lambda x:x[1])
    prefix={'Executive':'Executive summary (locally extracted key sentences):\n','Detailed':'Detailed extractive summary:\n','Concise':'Concise extractive summary:\n'}.get(style,'Extractive summary:\n')
    return prefix+'\n'.join('• '+x[2] for x in chosen), 'rule-based extractive (not generative AI)'
