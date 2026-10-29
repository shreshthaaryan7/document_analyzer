from collections import Counter
from services.retrieval import tokens
import re

def analyze(text):
    words=re.findall(r'\b\w+\b',text); sentences=[s for s in re.split(r'[.!?]+',text) if s.strip()]
    return {'words':len(words),'characters':len(text),'sentences':len(sentences),'paragraphs':len([p for p in text.splitlines() if p.strip()]),'terms':Counter(tokens(text)).most_common(12)}
