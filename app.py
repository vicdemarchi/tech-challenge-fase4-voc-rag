import json
from pathlib import Path
import streamlit as st
from voc.retrieval import Retriever
from voc.rag import Pipeline,Generator

st.set_page_config(page_title='Escuta | Olist VoC',page_icon='◉',layout='wide')
st.markdown('### ESCUTA / VOICE OF CUSTOMER')
st.title('O que os clientes estão contando?')
st.caption('Avaliações históricas Olist · 2016–2018 · Tech Challenge Fase 4 · Viviane Demarchi')
if not Path('artifacts/index_manifest.json').exists():
    st.info('Prepare a base antes de começar: voc download → voc prepare → voc index. Consulte o guia de instalação.')
    st.stop()

@st.cache_resource
def load(): return Retriever(),Generator()
try:
    retriever,generator=load()
except Exception as exc:
    st.error(f'Não foi possível carregar o modelo ou o índice: {type(exc).__name__}. Consulte o README.')
    st.stop()

with st.sidebar:
    st.header('Recorte da pesquisa')
    scores=st.multiselect('Notas das avaliações',[1,2,3,4,5],default=[1,2,3,4,5])
    categories=sorted({c for d in retriever.docs.values() for c in d['categories']})
    category=st.selectbox('Categoria do pedido',['Todas']+categories)
    st.caption('Pedidos com vários produtos podem pertencer a mais de uma categoria; o comentário é do pedido.')
    period=st.checkbox('Filtrar período da compra')
    start=st.date_input('De',value=__import__('datetime').date(2016,9,1),disabled=not period)
    end=st.date_input('Até',value=__import__('datetime').date(2018,10,31),disabled=not period)
    delivery=st.selectbox('Prazo registrado',['Todos','Entregue com atraso','Entregue sem atraso'])
    st.caption('Prazo compara datas de entrega e estimativa. Ausentes não contam como entrega no prazo.')

c1,c2,c3=st.columns(3)
c1.metric('Avaliações com texto',f'{len(retriever.docs):,}'.replace(',','.'))
c2.metric('Busca','Semântica + lexical')
c3.metric('Geração','Modelo local')
st.info('As respostas resumem evidências recuperadas. Elas não medem a frequência de problemas em toda a base.')
examples=['O que os clientes relatam sobre atrasos na entrega?', 'Quais problemas de qualidade dos produtos são relatados?',
          'Quais aspectos da compra os clientes elogiam?', 'Qual o percentual de clientes insatisfeitos?',
          'Como foi a entrega em 2026?']
example=st.selectbox('Perguntas para explorar',examples)
with st.form('question'):
    question=st.text_area('Sua pergunta',value=example,max_chars=1000)
    submit=st.form_submit_button('Investigar avaliações',type='primary')
if submit:
    if not scores: st.warning('Selecione pelo menos uma nota.')
    elif period and start>end: st.warning('A data inicial deve ser anterior à final.')
    elif not question.strip(): st.warning('Digite uma pergunta.')
    else:
        with st.spinner('Buscando evidências e verificando citações…'):
            result=Pipeline(retriever,generator).answer(question,scores=scores,category=None if category=='Todas' else category,
                start=start.isoformat() if period else None,end=end.isoformat() if period else None,
                late={'Todos':None,'Entregue com atraso':True,'Entregue sem atraso':False}[delivery])
        st.session_state['result']=result
if 'result' in st.session_state:
    result=st.session_state['result']
    st.subheader('Resultado da investigação')
    st.write(result['question'])
    if result['reason']: st.warning(result['reason'])
    for finding in result['findings']:
        st.write(finding['claim'])
        st.info(f'“{finding["quote"]}”')
        st.caption(f'Fonte: {finding["doc_id"]}')
    st.caption(f'Tempo total: {result["latency_seconds"]} s · Status: {result["status"]}')
    st.subheader('Evidências recuperadas')
    for e in result['evidence']:
        with st.expander(f'{e["doc_id"]} · Nota {e["review_score"]} · {e["purchase_date"]}'):
            st.write(e['text'])
            st.json({k:e[k] for k in ('review_id','order_id','source_row','categories','late_delivery','semantic_score','lexical_score','chunk_id')})
    st.download_button('Baixar investigação em JSON',json.dumps(result,ensure_ascii=False,indent=2),'investigacao.json','application/json')
    st.caption('Citações literais e IDs são verificados automaticamente. A sustentação semântica das sínteses ainda requer revisão crítica.')
