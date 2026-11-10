import json
from pathlib import Path
from voc.rag import Generator,Pipeline
from voc.retrieval import Retriever
cases=json.loads(Path('evaluation/generation_holdout.json').read_text(encoding='utf-8'))
p=Pipeline(Retriever(),Generator());results=[]
for case in cases:
    result=p.answer(case['question'],**case['filters']);result['expected_status']=case['expected']
    result['status_match']=result['status']==case['expected'];results.append(result)
    print(result['question'],result['status'],result['status_match'],flush=True)
    Path('evidence/generation_holdout_runs.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('Correspondência de status:',sum(r['status_match'] for r in results),'/',len(results))
