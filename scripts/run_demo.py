import json
from pathlib import Path
from voc.retrieval import Retriever
from voc.rag import Generator,Pipeline
p=Pipeline(Retriever(),Generator())
cases=[
 ('O que os clientes relatam sobre atrasos na entrega?',{'scores':[1,2]}),
 ('Quais relatos mencionam produtos quebrados ou danificados?',{'scores':[1,2]}),
 ('Quais elogios se referem à entrega antes do prazo?',{'scores':[4,5]}),
 ('O que os clientes relatam sobre a entrega por drones?',{}),
 ('Qual é a capital da França?',{}),
 ('Como foi a entrega em 2026?',{}),
 ('Qual o percentual de clientes com atrasos?',{}),
 ('Há reclamações sobre a entrega?',{'category':'categoria_inexistente'}),
]
results=[]
for question,filters in cases:
    result=p.answer(question,**filters);results.append(result)
    print(json.dumps({k:result[k] for k in ['question','status','findings','reason','latency_seconds']},ensure_ascii=False),flush=True)
    Path('evidence/demo_runs.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
