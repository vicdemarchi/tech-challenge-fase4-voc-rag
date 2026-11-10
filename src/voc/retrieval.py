"""Vetores normalizados + TF-IDF; fusão por Reciprocal Rank Fusion (RRF)."""
import hashlib
import json
import os
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from sklearn.feature_extraction.text import TfidfVectorizer

MODEL = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
REVISION = 'e8f8c211226b894fcb81acc59f3b34ba3efd5f42'

class Embedder:
    def __init__(self):
        torch.set_num_threads(int(os.getenv('VOC_THREADS','4')))
        self.model=SentenceTransformer(MODEL,revision=REVISION,device='cpu',cache_folder=os.getenv('VOC_EMBED_CACHE','artifacts/model_cache'))
    def embed(self,texts,batch_size=64):
        return self.model.encode(list(texts),batch_size=batch_size,normalize_embeddings=True,show_progress_bar=True)

def embedder():
    return Embedder()

def chunks(text, tokenizer, size=100, overlap=20):
    """Offsets de tokens no texto original, sem perder o fim de avaliações longas."""
    # Use an independent tokenizer with truncation disabled (configured by build).
    encoded = tokenizer.encode(text,add_special_tokens=False)
    offsets = encoded.offsets
    for start in range(0,len(offsets),size-overlap):
        end = min(start+size,len(offsets))
        yield text[offsets[start][0]:offsets[end-1][1]]
        if end == len(offsets):
            break

def build(processed: Path, artifacts: Path):
    from tokenizers import Tokenizer
    model = embedder()
    tokenizer = Tokenizer.from_str(model.model.tokenizer.backend_tokenizer.to_str())
    tokenizer.no_truncation(); tokenizer.no_padding()
    documents = [json.loads(x) for x in (processed/'documents.jsonl').read_text(encoding='utf-8').splitlines()]
    passages=[]
    for d in documents:
        for i,text in enumerate(chunks(d['text'],tokenizer)):
            passages.append({'doc_id':d['doc_id'],'chunk_id':f"{d['doc_id']}_{i}",'text':text})
    vectors = np.array(list(model.embed([p['text'] for p in passages],batch_size=64)),dtype=np.float32)
    vectors /= np.maximum(np.linalg.norm(vectors,axis=1,keepdims=True),1e-12)
    artifacts.mkdir(parents=True,exist_ok=True)
    np.save(artifacts/'vectors.npy',vectors)
    (artifacts/'passages.jsonl').write_text('\n'.join(json.dumps(p,ensure_ascii=False) for p in passages),encoding='utf-8')
    manifest={'model':MODEL,'revision':REVISION,'dimensions':int(vectors.shape[1]),'documents':len(documents),
              'passages':len(passages),'chunk_tokens':100,'overlap_tokens':20,
              'documents_sha256':hashlib.sha256((processed/'documents.jsonl').read_bytes()).hexdigest(),
              'vectors_sha256':hashlib.sha256((artifacts/'vectors.npy').read_bytes()).hexdigest(),
              'passages_sha256':hashlib.sha256((artifacts/'passages.jsonl').read_bytes()).hexdigest()}
    (artifacts/'index_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    return manifest

class Retriever:
    def __init__(self, processed=Path('data/processed'), artifacts=Path('artifacts')):
        self.manifest=json.loads((artifacts/'index_manifest.json').read_text())
        if self.manifest['model']!=MODEL or self.manifest.get('revision')!=REVISION:
            raise ValueError('Modelo ou revisão diferente do índice; reconstrua o índice.')
        for path,key in [(processed/'documents.jsonl','documents_sha256'),(artifacts/'vectors.npy','vectors_sha256'),(artifacts/'passages.jsonl','passages_sha256')]:
            if hashlib.sha256(path.read_bytes()).hexdigest()!=self.manifest[key]:
                raise ValueError('Dados ou índice alterados: reconstrua o índice.')
        self.docs={d['doc_id']:d for d in map(json.loads,(processed/'documents.jsonl').read_text(encoding='utf-8').splitlines())}
        self.passages=list(map(json.loads,(artifacts/'passages.jsonl').read_text(encoding='utf-8').splitlines()))
        self.vectors=np.load(artifacts/'vectors.npy',mmap_mode='r',allow_pickle=False)
        if len(self.passages)!=len(self.vectors): raise ValueError('Índice desalinhado.')
        self.model=embedder()
        self.tfidf=TfidfVectorizer(lowercase=True,strip_accents='unicode',ngram_range=(1,2),sublinear_tf=True)
        self.lexical=self.tfidf.fit_transform(p['text'] for p in self.passages)

    def release_model(self):
        self.model=None
        import gc
        gc.collect()
        # Return freed CPU allocations on glibc; optional optimization, not required on Windows.
        if os.name=='posix':
            import ctypes
            try: ctypes.CDLL(None).malloc_trim(0)
            except AttributeError: pass

    def search(self,question,k=6,scores=None,category=None,start=None,end=None,late=None,mode='hybrid',threshold=0.30):
        if mode not in ('hybrid','dense','lexical'): raise ValueError('Modo desconhecido')
        q=' '.join(question.split())
        if not q or len(q)>1000: raise ValueError('Use uma pergunta entre 1 e 1.000 caracteres.')
        allowed=[]
        for i,p in enumerate(self.passages):
            d=self.docs[p['doc_id']]
            if scores is not None and d['review_score'] not in scores: continue
            if category and category not in d['categories']: continue
            if start and (not d['purchase_date'] or d['purchase_date']<start): continue
            if end and (not d['purchase_date'] or d['purchase_date']>end): continue
            if late is not None and d['late_delivery'] is not late: continue
            allowed.append(i)
        if not allowed: return []
        ids=np.array(allowed)
        if self.model is None: self.model=embedder()
        vector=np.array(list(self.model.embed([q]))[0]); vector/=max(np.linalg.norm(vector),1e-12)
        dense=self.vectors[ids]@vector
        lex=(self.lexical[ids]@self.tfidf.transform([q]).T).toarray().ravel()
        n=min(60,len(ids))
        dr=np.argsort(-dense,kind='stable')[:n]; lr=np.argsort(-lex,kind='stable')[:n]
        fused={}
        for ranking,values in ((dr,dense),(lr,lex)):
            for rank,j in enumerate(ranking,1):
                if values[j]>0: fused[int(j)]=fused.get(int(j),0)+1/(60+rank)
        ranked=sorted(fused,key=lambda j:(-fused[j],int(ids[j]))) if mode=='hybrid' else (dr if mode=='dense' else lr)
        seen=set(); seen_text=set(); results=[]
        for j in ranked:
            if mode=='lexical':
                if lex[j]<=0: continue
            elif dense[j]<threshold: continue
            p=self.passages[int(ids[j])]; d=self.docs[p['doc_id']]
            fingerprint=d['text'].casefold()
            if d['doc_id'] in seen or fingerprint in seen_text: continue
            seen.add(d['doc_id']); seen_text.add(fingerprint)
            results.append({**d,'passage':p['text'],'chunk_id':p['chunk_id'],'semantic_score':round(float(dense[j]),5),
                            'lexical_score':round(float(lex[j]),5),'rrf_score':round(fused.get(int(j),0),6)})
            if len(results)>=k: break
        return results
