import unittest
from services.text_chunker import chunk_pages
from services.retrieval import tokens, search_chunks
from services.document_parser import extract_document
from services.insights import analyze
class CoreTests(unittest.TestCase):
 def test_txt_extract(self):
  pages,count=extract_document(b'hello document', 'txt'); self.assertEqual(pages[0]['text'],'hello document'); self.assertIsNone(count)
 def test_empty_txt(self):
  pages,count=extract_document(b'   ','txt'); self.assertEqual(pages,[])
 def test_chunk_source_preserved(self):
  chunks=chunk_pages([{'text':'This is a test sentence. '*60,'source_ref':'Page 2'}],max_chars=300,overlap=40); self.assertTrue(chunks); self.assertTrue(all(c['source_ref']=='Page 2' for c in chunks))
 def test_tokens_remove_common_words(self): self.assertIn('retrieval',tokens('The retrieval pipeline works'))
 def test_insights(self):
  a=analyze('Document analysis works. Document search works.'); self.assertEqual(a['sentences'],2); self.assertGreater(a['words'],0)
if __name__=='__main__': unittest.main()
