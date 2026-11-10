"""Pool para julgamento e comparação reproduzível; não usa LLM como juiz."""
import json
import math
import time
from pathlib import Path
from voc.retrieval import Retriever
r=Retriever(); queries=json.loads(Path('evaluation/queries.json').read_text(encoding='utf-8'))
rows=[];pool={}
for q in queries:
    for mode in ['lexical','dense','hybrid']:
        start=time.perf_counter(); found=r.search(q['question'],k=3,scores=q['scores'],mode=mode)
        rows.append({'query_id':q['id'],'mode':mode,'ids':[x['doc_id'] for x in found],
                     'latency_seconds':round(time.perf_counter()-start,4)})
        for x in found: pool[(q['id'],x['doc_id'])]={'query_id':q['id'],'doc_id':x['doc_id'], 'text':x['text'], 'relevance':None}
Path('evidence/retrieval_runs.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
path=Path('evaluation/qrels.json')
if not path.exists():
    path.write_text(json.dumps(list(pool.values()),indent=2,ensure_ascii=False),encoding='utf-8')
    print('Pool criado. Julgue relevance 0/1/2 e execute novamente.');raise SystemExit(0)
labels={(x['query_id'],x['doc_id']):x['relevance'] for x in json.loads(path.read_text(encoding='utf-8'))}
metrics=[]
for row in rows:
    grades=[labels.get((row['query_id'],i)) for i in row['ids']]
    if any(g is None for g in grades): raise ValueError('Julgamentos ausentes no pool.')
    q=next(q for q in queries if q['id']==row['query_id'])
    metrics.append({**row,'split':q['split'],'precision_at_3':sum(g>=1 for g in grades)/3,
                    'fully_relevant_at_3':sum(g==2 for g in grades)/3})
summary={}
for split in ['dev','test']:
    summary[split]={}
    for mode in ['lexical','dense','hybrid']:
        selected=[m for m in metrics if m['split']==split and m['mode']==mode]
        summary[split][mode]={k:round(sum(m[k] for m in selected)/len(selected),4)
                              for k in ['precision_at_3','fully_relevant_at_3','latency_seconds']}
Path('evidence/retrieval_metrics.json').write_text(json.dumps({'summary':summary,'per_query':metrics,
 'method':'Pool top-3, julgamento assistido por IA, escala 0/1/2; sem juiz humano independente. Amostra pequena, sem recall global.'},indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
