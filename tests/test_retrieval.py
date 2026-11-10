import numpy as np
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer
from tokenizers import Tokenizer,models,pre_tokenizers
from voc.retrieval import Retriever,chunks

def test_chunk_preserves_end_and_overlap_without_silent_truncation():
    tok=Tokenizer(models.WordLevel({'[UNK]':0,**{f'w{i}':i+1 for i in range(150)}},unk_token='[UNK]'))
    tok.pre_tokenizer=pre_tokenizers.Whitespace()
    text=' '.join(f'w{i}' for i in range(150))
    pieces=list(chunks(text,tok))
    assert len(pieces)==2 and pieces[1].endswith('w149')
    assert pieces[0].endswith('w99') and pieces[1].startswith('w80 ')
    assert all(len(tok.encode(x).ids)<=100 for x in pieces)

@pytest.fixture
def r():
    x=Retriever.__new__(Retriever)
    x.docs={'a':{'doc_id':'a','text':'entrega rápida','review_score':5,'categories':['livros'],'purchase_date':'2018-01-01','late_delivery':False},
            'b':{'doc_id':'b','text':'entrega atrasada','review_score':1,'categories':['moveis'],'purchase_date':'2018-02-01','late_delivery':True},
            'c':{'doc_id':'c','text':'não recebido','review_score':1,'categories':['livros'],'purchase_date':'','late_delivery':None}}
    x.passages=[{'doc_id':i,'chunk_id':i+'_0','text':d['text']} for i,d in x.docs.items()]
    x.vectors=np.array([[1.,0.],[.8,.6],[0.,1.]],dtype=np.float32)
    class Embedder:
        def embed(self,q): return [np.array([1.,0.])]
    x.model=Embedder();x.tfidf=TfidfVectorizer();x.lexical=x.tfidf.fit_transform(p['text'] for p in x.passages)
    return x

def test_filters_before_top_k(r):
    result=r.search('entrega',k=1,scores=[1],mode='dense')
    assert result[0]['doc_id']=='b'

def test_unknown_delivery_excluded_from_false_filter(r):
    result=r.search('entrega',late=False,mode='dense',threshold=-1)
    assert [x['doc_id'] for x in result]==['a']

def test_empty_metadata_recorte(r):
    assert r.search('entrega',category='inexistente')==[]

def test_missing_purchase_date_not_in_date_filter(r):
    result=r.search('entrega',start='2017-01-01',threshold=-1,mode='dense')
    assert 'c' not in [x['doc_id'] for x in result]

def test_semantic_floor_rejects_irrelevant_vector(r):
    assert r.search('entrega',category='livros',scores=[1],mode='dense')==[]
