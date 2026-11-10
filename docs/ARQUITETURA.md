# Arquitetura e contrato dos componentes

## Fronteiras

| Componente | Entrada | Saída | Falha observável |
|---|---|---|---|
| data.prepare | Quatro CSVs oficiais | documents.jsonl e auditoria | Schema ausente, chaves de dimensão duplicadas |
| retrieval.build | Documentos íntegros | Chunks, vetores, manifesto | Modelo indisponível, indexação incompleta |
| Retriever.search | Pergunta e filtros explícitos | Até k evidências, scores e metadados | Pergunta vazia/longa, índice divergente |
| Generator.generate | Pergunta e trechos | JSON estruturado | Serviço local indisponível, timeout, JSON inválido |
| validate | JSON e evidências | Achados validados ou lista vazia | ID/quote inventado, schema impróprio |
| Pipeline.answer | Pergunta e filtros | answered/abstained/error, rastreio | Mensagem explícita; sem resposta artificial |
| app.py | Interação local | Resposta, fontes, JSON baixável | Orientação para preparar índice/modelo |

## Por que não um banco vetorial externo?

Uma matriz de aproximadamente 43 mil vetores de 384 dimensões requer cerca de 66 MB antes de overhead e chunks adicionais. A busca exata é suficiente para este protótipo e mantém operação simples e auditável. Em maior escala, concorrência ou atualizações frequentes, seria adequado migrar para FAISS, Qdrant ou outro mecanismo com índices e filtros persistentes.

TF-IDF é reconstruído no carregamento da aplicação para evitar desserializar objetos pickle de origem não confiável. Vetores usam `allow_pickle=False`. Documentos e manifesto permitem inspeção com ferramentas comuns. Não há gravação automática de perguntas em um serviço externo.

## Granularidade e integridade

O documento representa uma avaliação, não um item. Os chunks mantêm `doc_id` e `chunk_id`. A busca pode encontrar um trecho no fim do comentário e retorna o comentário integral na área de evidências. A geração recebe somente o trecho recuperado, portanto a citação deve estar nesse trecho. A tela exibe também o `review_id`, `order_id` e `source_row` (número lógico do registro CSV com cabeçalho; não linha física quando existem quebras internas no campo).

A categoria se refere à lista de categorias do pedido. Um comentário pode abordar logística geral, mesmo que o pedido tenha produto de uma categoria filtrada. Por isso, não se afirma que o comentário diagnostica um produto individual.

## Recuperação e abstenção

O filtro cria o universo elegível antes do cálculo de ranking. As buscas lexical e semântica operam no mesmo universo. A fusão RRF reduz dependência de escalas distintas. Duplicatas textuais e múltiplos chunks do mesmo documento são removidos do contexto. O limiar de cosseno é heurístico; não é evidência suficiente por si só.

Abstenção tem três barreiras: escopo determinístico, ausência de candidatos elegíveis/relevantes e avaliação/validação da resposta pelo gerador. A checagem de IDs e quotes é determinística. Citações com menos de oito caracteres são rejeitadas para evitar tratar elogios genéricos muito curtos como evidência suficiente; isso também pode gerar recusas conservadoras. Uma segunda passagem pelo mesmo LLM verifica relação com a pergunta e suporte, mas a checagem de relevância semântica da conclusão não é completa: deve ser revisada na avaliação humana.

## Custos e reprodutibilidade

Downloads têm custo de banda e armazenamento; inferência local consome CPU, memória e energia, mesmo sem cobrança por token. Cache de modelos e índice evita repetir preparação. Quantização reduz memória do LLM. Temperatura zero e seed 42 diminuem variação, mas versões e hardware podem mudar resultados. `evidence/environment.json` registra o ambiente medido. Não foram enviados segredos ou credenciais ao repositório.

## Memória no backend llama.cpp

O carregamento conjunto do embedding e do LLM 3B excedeu o limite do ambiente de execução. O pipeline passou a liberar o embedding antes de carregar o LLM; cada chamada de geração ou verificação roda em um subprocesso isolado e termina ao devolver o JSON. Isso garante a liberação dos buffers nativos entre chamadas. A busca seguinte recarrega o embedding pelo cache. Contexto llama.cpp de 3.072 tokens, batch de 128 e microbatch de 64 limitam buffers. Essa escolha troca latência de recarga por menor pico de memória. Ollama gerencia seu próprio processo e cache; o teste local não mede a memória desse backend.
