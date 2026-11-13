"""Relatório técnico complementar; dados de avaliação lidos das execuções reais."""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/Relatorio-Tecnico-Fase4-Viviane-Demarchi.pdf'
for name,file in [('DejaVu','DejaVuSans.ttf'),('DejaVu-Bold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
INK=colors.HexColor('#1E3038'); TEAL=colors.HexColor('#187F80'); LIGHT=colors.HexColor('#EAF1F1'); GRAY=colors.HexColor('#586B74')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body',fontName='DejaVu',fontSize=9.3,leading=14,textColor=INK,spaceAfter=9))
styles.add(ParagraphStyle(name='SmallX',fontName='DejaVu',fontSize=7.8,leading=11,textColor=GRAY,spaceAfter=7))
styles.add(ParagraphStyle(name='TitleX',fontName='DejaVu-Bold',fontSize=28,leading=33,textColor=INK,spaceAfter=16))
styles.add(ParagraphStyle(name='H1X',fontName='DejaVu-Bold',fontSize=20,leading=25,textColor=INK,spaceAfter=15))
styles.add(ParagraphStyle(name='H2X',fontName='DejaVu-Bold',fontSize=12,leading=16,textColor=TEAL,spaceBefore=12,spaceAfter=7))
styles.add(ParagraphStyle(name='Cell',fontName='DejaVu',fontSize=8,leading=11,textColor=INK))

def p(text,style='Body'): return Paragraph(escape(str(text)).replace('\n','<br/>'),styles[style])
def table(rows,widths):
    t=Table([[p(c,'Cell') for c in row] for row in rows],colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#DAE2E5'))]))
    return t

def footer(c,doc):
    c.setFillColor(TEAL);c.rect(42,805,511,4,fill=1,stroke=0)
    c.setFont('DejaVu',7);c.setFillColor(GRAY)
    c.drawString(42,28,'ESCUTA  /  TECH CHALLENGE FASE 4  /  VIVIANE DEMARCHI')
    c.drawRightString(553,28,str(doc.page))

class Architecture(Flowable):
    def __init__(self): Flowable.__init__(self);self.width=511;self.height=215
    def draw(self):
        c=self.canv
        boxes=[(0,150,235,48,'Pergunta + filtros','Escopo e universo elegível'),
               (276,150,235,48,'Base de avaliações','Chunks + metadados'),
               (0,77,235,48,'Busca híbrida','Semântica + TF-IDF → RRF'),
               (276,77,235,48,'Contexto rastreável','Trechos selecionados + IDs'),
               (0,4,235,48,'LLM local','Síntese em JSON estruturado'),
               (276,4,235,48,'Validação e resposta','Citações válidas ou abstenção')]
        for x,y,w,h,title,sub in boxes:
            c.setFillColor(LIGHT);c.roundRect(x,y,w,h,5,fill=1,stroke=0)
            c.setFillColor(TEAL);c.setFont('DejaVu-Bold',10);c.drawString(x+12,y+29,title)
            c.setFillColor(INK);c.setFont('DejaVu',8);c.drawString(x+12,y+12,sub)
        c.setStrokeColor(TEAL);c.setLineWidth(1)
        for x1,y1,x2,y2 in [(118,150,118,125),(394,150,394,138),(394,138,118,138),(235,101,276,101),(394,77,394,64),(394,64,118,64),(118,64,118,52),(235,28,276,28)]:
            c.line(x1,y1,x2,y2)

audit=json.loads((ROOT/'evidence/data_audit.json').read_text())
metrics=json.loads((ROOT/'evidence/retrieval_metrics.json').read_text())
demos=json.loads((ROOT/'evidence/demo_runs.json').read_text())
index=json.loads((ROOT/'artifacts/index_manifest.json').read_text())
story=[]
story += [Spacer(1,22),p('IAST / PÓS TECH / FASE 4','SmallX'),p('Escuta\nVoice of Customer\nIntelligence','TitleX'),
    p('RAG com avaliações reais, recuperação híbrida e evidências verificáveis.','H2X'),Spacer(1,14),
    table([['BASE ORIGINAL','DOCUMENTOS COM TEXTO','PERÍODO'],['99.224 avaliações','42.687 documentos','2016–2018']],[170,171,170]),
    Spacer(1,20),p('Viviane Demarchi','H2X'),p('Relatório técnico complementar · 09 de novembro de 2026'),
    p('Objetivo','H2X'),p('Permitir que gestores investiguem reclamações e elogios em linguagem natural, com acesso aos comentários que sustentam cada achado. O sistema reconhece limitações de escopo e não apresenta a amostra recuperada como uma estatística de toda a base.'),
    p('Entregas e situação','H2X'),p('Código, documentação, auditoria, testes e execuções reais compõem o pacote. Publicação no GitHub e gravação do vídeo dependem da finalização na conta e no computador da aluna. Este PDF não substitui os dois entregáveis exigidos no briefing.'),
    p('O resultado de avaliação é exploratório. Os resultados não representam uma medição de desempenho geral em produção.','SmallX'),PageBreak()]

story += [p('01 / Base de conhecimento','SmallX'),p('Preservar o sentido e a origem','H1X'),
    p('Foram usados os quatro arquivos oficiais de avaliações, pedidos, itens e produtos. A seleção mantém registros com título ou comentário; a falta de texto não é preenchida artificialmente.'),
    table([['ETAPA / VERIFICAÇÃO','RESULTADO'],['Registros de avaliação recebidos','99.224'],['Sem título e sem comentário','56.537'],['Documentos elegíveis','42.687'],['Pedidos associados aos documentos','42.540'],['Ocorrências repetidas de review_id','317'],['Textos repetidos na base elegível','5.576'],['Avaliações sem correspondência em pedidos','0']],[340,171]),
    p('Limpeza conservadora','H2X'),p('Remoção de HTML e espaços redundantes; preservação de acentos, pontuação e negações. Email, telefone e CPF identificáveis por padrões são mascarados. Não se alega anonimização completa.'),
    p('Integração sem inflar a base','H2X'),p('Categorias dos itens são agregadas por pedido antes do join. Relações many-to-one são verificadas. O documento preserva review_id, order_id e posição lógica no CSV; uma chave derivada adicional evita tratar review_id como único.'),
    p('Metadados e interpretação','H2X'),p('Nota, data da compra, lista de categorias e atraso registrado permitem recortes. Pedidos com várias categorias não atribuem o comentário a um produto específico. Ausência de data de entrega permanece desconhecida; atraso compara datas de calendário.'),
    p('Rastreabilidade: evidence/data_audit.json e evidence/source_sha256.json registram contagens e hashes dos arquivos de origem.','SmallX'),PageBreak()]

story += [p('02 / Arquitetura','SmallX'),p('Da pergunta à evidência','H1X'),Architecture(),Spacer(1,10),
    table([['DECISÃO','JUSTIFICATIVA'],['MiniLM multilíngue · 384 dimensões','Representação semântica com suporte a português e execução em CPU.'],['Chunks: 100 tokens; overlap: 20','Janela de 128 tokens do modelo; evita perder o fim de comentários longos.'],['Matriz NumPy + busca exata','Escala do protótipo permite simplicidade sem índice aproximado ou serviço externo.'],['TF-IDF + RRF (constante 60)','Complementa sentidos próximos com termos específicos sem misturar escalas de score.'],['Qwen2.5 3B Instruct Q4_K_M','Geração local, sem API paga, com limite de capacidade explicitado.']],[200,311]),
    p(f'Índice executado: {index["passages"]:,} trechos para {index["documents"]:,} documentos. Até seis avaliações entram no contexto, sem repetir documento ou texto.'.replace(',','.'),'SmallX'),
    p('Filtros são aplicados antes do ranking. Similaridade mínima de 0,30 é uma heurística, não uma probabilidade calibrada. IDs e citações literais são verificados após a geração; falhas resultam em abstenção.'),PageBreak()]

rows=[['MÉTODO','PRECISION@3','TOTALMENTE RELEVANTES@3']]
for mode,label in [('lexical','Lexical TF-IDF'),('dense','Semântica'),('hybrid','Híbrida RRF')]:
    m=metrics['summary']['test'][mode];rows.append([label,f'{m["precision_at_3"]:.1%}',f'{m["fully_relevant_at_3"]:.1%}'])
story += [p('03 / Avaliação','SmallX'),p('Evidências de execução','H1X'),
    p('Comparação de recuperação','H2X'),p('O protocolo contém oito perguntas: três de desenvolvimento e cinco de teste. Para cada método, os três primeiros documentos foram reunidos em um pool e julgados com escala 0 (irrelevante), 1 (parcial) e 2 (direto). Precision@3 considera notas 1 e 2 como relevantes.'),table(rows,[191,140,180]),
    p('Limite da medição','H2X'),p('Os julgamentos foram produzidos com assistência de IA, sem anotador humano independente. O conjunto é pequeno e representa perguntas selecionadas, não a distribuição real de uso. Não foi calculado recall global porque não há julgamento de toda a base.'),
    p('Testes e geração','H2X'),p('29 testes automatizados aprovados verificam integridade de joins, preservação de negações, dados ausentes, recusas, IDs e citações inválidas, erro de infraestrutura. Quatro verificações adicionais via AppTest cobrem a interface. As respostas do modelo local são registradas integralmente com seus documentos e tempo total.'),
    p('Geração: resultado final','H2X'),p('Na demonstração, 8 de 8 decisões corresponderam ao esperado. Nas seis consultas adicionais reutilizadas, foram 4 de 6: duas perguntas respondíveis foram recusadas indevidamente. Não é um teste independente nem uma estimativa de acurácia geral.'),
    p('Leitura crítica','H2X'),p('Uma citação existente pode acompanhar uma síntese equivocada. A validação automática garante pertencimento e literalidade, mas não demonstra entailment semântico. O pequeno LLM pode omitir informação ou formular uma inferência inadequada. Revisão humana é necessária antes de decisões de negócio.'),
    p('Arquivos: evaluation/queries.json, evaluation/qrels.json, evidence/retrieval_metrics.json, evidence/tests.txt e evidence/demo_runs.json.','SmallX'),PageBreak()]

story += [p('04 / Demonstração','SmallX'),p('Respostas com fontes visíveis','H1X')]
for result in demos[:3]:
    story += [p(result['question'],'H2X')]
    if result['findings']:
        f=result['findings'][0]
        story += [p(f['claim']),p('“'+f['quote']+'”','SmallX'),p('Fonte: '+f['doc_id']+' · '+str(result['latency_seconds'])+' s','SmallX')]
    else: story += [p(result['reason'])]
story += [p('Recusas e ausências de evidência','H2X')]
for result in demos[3:]:
    story += [p(result['question']+(' (categoria inexistente)' if result['filters'].get('category')=='categoria_inexistente' else '')+' — '+{'answered':'respondida','abstained':'abstenção','error':'erro'}[result['status']],'SmallX')]
story += [p('Os exemplos acima foram obtidos na execução, não redigidos como se fossem respostas do sistema. As evidências completas, filtros e tempos estão no JSON da demonstração.','SmallX'),PageBreak()]

story += [p('05 / Reprodução','SmallX'),p('Uma solução que pode ser conferida','H1X'),
    table([['PASSO','ONDE CONFERIR'],['Instalar e preparar','README.md'],['Reproduzir a recuperação','scripts/evaluate_retrieval.py e evaluation/qrels.json'],['Reproduzir respostas','scripts/run_demo.py; LLM local deve estar disponível'],['Verificar requisitos','docs/MATRIZ_REQUISITOS.md']],[200,311]),
    p('Escopo da validação','H2X'),p('A execução de referência usa Linux, CPU e backend llama.cpp. A interface com Ollama foi verificada manualmente no Windows em três consultas: atrasos, elogios à entrega antecipada e pergunta fora do período da base. Versões, hashes e resultados estão em evidence/. Downloads iniciais exigem internet. Essa verificação pontual não substitui a avaliação quantitativa de referência.'),
    p('Próximos passos técnicos','H2X'),p('Ampliar perguntas e anotadores independentes; calibrar limiares de abstenção; testar reranker multilíngue; acrescentar classificação temática e agregação para frequências. Aplicações públicas exigiriam autenticação, controles de acesso e revisão de privacidade.'),
    p('Fontes principais','H2X'),p('Dados: Olist / Kaggle, Brazilian E-Commerce Public Dataset, licença CC BY-NC-SA 4.0. Modelos: Sentence Transformers / MiniLM multilíngue e Qwen2.5-3B-Instruct-GGUF, conforme model cards. Bibliografia e URLs completas: docs/REFERENCIAS.md. Requisitos acadêmicos: briefing [IAST] Tech Challenge Fase 4, pp. 6–10.'),
    p('O bônus opcional Databricks não integra o escopo implementado; não há reivindicação de bonificação.','SmallX')]
SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),rightMargin=42,leftMargin=42,topMargin=55,bottomMargin=48,
                  title='Escuta - Relatório Técnico - Tech Challenge Fase 4',author='Viviane Demarchi').build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
