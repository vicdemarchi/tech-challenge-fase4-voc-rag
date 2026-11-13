# Avaliação: protocolo, resultados e limites

## 1. Base e índice executados

- Fonte: download oficial Kaggle/Olist, com hashes SHA-256 preservados.
- 99.224 registros de origem; 56.537 sem título e sem comentário; 42.687 documentos elegíveis.
- 42.692 chunks, embeddings de 384 dimensões; revisão do MiniLM registrada no manifesto.
- Base completa de textos elegíveis; não houve amostragem para diminuir a indexação.
- Código e testes: Python 3.12 em CPU/Linux. Versões exatas: `evidence/environment.json`.

## 2. Comparação de recuperação

Oito perguntas foram definidas em `evaluation/queries.json`: três de desenvolvimento e cinco de teste. A unidade de avaliação é a pergunta, com top-3 de documentos distintos. A seleção de perguntas e a amostra pequena limitam a validade externa.

Foi formado um pool com 60 pares únicos de pergunta/documento, provenientes dos três métodos. Os julgamentos assistidos por IA estão em `evaluation/qrels.json`, com texto, identificador e justificativa. Não houve anotador humano independente nem cálculo de concordância interanotador.

Escala de relevância:

- **0:** não sustenta o tema solicitado;
- **1:** relação parcial ou evidência ambígua;
- **2:** comentário diretamente relacionado ao tema.

`Precision@3 = número de resultados com relevância >= 1 / 3`.
`Totalmente relevantes@3 = número de resultados com relevância = 2 / 3`.
A média por método é calculada entre as perguntas de cada split. Resultados ausentes contam como não relevantes no denominador fixo 3. Não foi medido recall global: não existe julgamento de todas as avaliações para cada pergunta.

### Resultados nas cinco perguntas de teste

| Método | Precision@3 | Totalmente relevantes@3 | Tempo médio da busca |
|---|---:|---:|---:|
| TF-IDF lexical | 100,0% | 73,3% | 0,081 s |
| Semântica | 86,7% | 66,7% | 0,061 s |
| Híbrida RRF | 93,3% | 80,0% | 0,074 s |

Nas três perguntas de desenvolvimento, os três métodos obtiveram 100% nas duas métricas. São perguntas simples e a quantidade de exemplos é pequena; esses números não devem ser interpretados como desempenho geral do sistema.

A busca híbrida teve a maior proporção de evidências **diretamente** relevantes nesse recorte; a lexical teve a maior precisão ao incluir evidências parciais. Portanto, não se afirma superioridade universal da recuperação híbrida. A escolha de RRF também se apoia na complementaridade de sinais e na simplicidade da combinação.

Os tempos incluem o embedding da pergunta mesmo no modo lexical, porque a implementação calcula os dois sinais para padronizar o registro; não representam uma implementação lexical otimizada. Os modelos estavam carregados. Tempos variam por hardware e não constituem SLA.

## 3. Abstenção e geração

O desenvolvimento identificou dois problemas na configuração inicial com Qwen 1.5B: síntese inadequada apesar de citação válida e confusão entre um drone comprado e entrega feita por drones. As execuções iniciais são preservadas em `evidence/development_v1.json`.

Isso motivou uma verificação adicional da relação entre a pergunta e os achados, instruções mais específicas e avaliação de um modelo maior. A verificação é feita pelo mesmo LLM, sem independência de erros. A versão final julga cada achado separadamente, preservando os sustentados mesmo se outro for rejeitado. Ela pode falhar ou rejeitar uma resposta válida; não prova ausência de alucinações. As configurações intermediárias estão em `evidence/development_v2.json` e `evidence/development_v3.json`. Uma recusa indevida em elogios também motivou a retirada de textos de exemplo genéricos do prompt e o uso de schema dinâmico: cada ID e sua citação são escolhidos entre pares efetivamente recuperados.

As perguntas de desenvolvimento usadas para ajustar o comportamento não contam como teste independente. As seis consultas adicionais de `evaluation/generation_holdout.json` incluem três respondíveis e três sobre informações não disponíveis nos comentários. Apesar do nome histórico do arquivo, o conjunto foi reutilizado após ajustes na verificação; NÃO é um holdout intocado e NÃO demonstra generalização. Há também sobreposição temática com o teste de recuperação. A medição final é uma verificação de regressão exploratória, não uma avaliação externa.

Consulte o resumo de geração ao fim deste documento, produzido após a execução final. Todos os JSONs preservam a pergunta, os filtros, fontes, resposta estruturada, decisão de verificação e tempo total. Erros de infraestrutura são distintos de abstenção por falta de evidências.

## 4. Testes automatizados

`evidence/tests.txt` registra **29 testes aprovados**. Eles cobrem limpeza com preservação de negações, mascaramento de identificadores, dados ausentes, chaves repetidas, integração sem multiplicação, atrasos por data, filtros antes do top-k, chunks com fim preservado, limiar semântico, escopo, citações inválidas e verificação de resposta.

Os testes usam pequenas fixtures sintéticas explicitamente separadas dos dados Olist. A comparação de recuperação e as demonstrações usam a base real. Não se apresenta um teste com gerador simulado como evidência de qualidade de um LLM.

## 5. Interface e reprodução

Quatro verificações passaram via Streamlit AppTest com a base real e a configuração local (sem inferência generativa nessa verificação): carregamento, contagem de documentos, recusa fora de escopo e validação de seleção vazia de notas. O arquivo `evidence/interface_test.json` registra o método.

Em 13/11/2026, a interface foi inspecionada manualmente no Windows com Ollama e Qwen2.5:3b. Foram observadas respostas com fontes para atrasos (notas 1 e 2) e elogios à entrega antecipada (notas 4 e 5), além da abstenção para uma pergunta sobre 2026. Houve um HTTPError inicial; após execução direta do modelo no terminal, a nova tentativa na interface respondeu. Essa verificação pontual não equivale a um benchmark do backend Ollama. As métricas e os JSONs de geração versionados permanecem referentes ao backend llama.cpp.

Os 29 testes automatizados também passaram no GitHub Actions: [execução de referência](https://github.com/vicdemarchi/tech-challenge-fase4-voc-rag/actions/runs/42726554639).

## 6. Ameaças à validade e próximos passos

- Julgamento assistido por IA e número pequeno de perguntas; necessidade de anotadores independentes.
- Perguntas selecionadas podem favorecer vocabulário frequente ou exemplos simples.
- Cosseno mínimo 0,30 é heurístico e não foi calibrado com um grande conjunto de perguntas sem resposta.
- Filtros explícitos no formulário não são extraídos automaticamente da linguagem natural.
- Ausência de um tópico entre os resultados não prova ausência em toda a base.
- Citações literais não garantem suporte de toda a inferência; verificação pelo mesmo LLM também é falível.
- Regra de escopo pode recusar perguntas válidas ou aceitar perguntas irrelevantes que mencionem produtos.
- Não foram executados teste de carga, avaliação de produção, auditoria completa de anonimização ou benchmark amplo de ataques de prompt injection.

Próxima etapa: ampliar e revisar humanamente o conjunto de avaliação, calibrar recuperação/abstenção, avaliar reranking e acrescentar classificação com agregação para responder perguntas de frequência.

## 7. Resultado final de geração

- Demonstração: **8/8** decisões de resposta/abstenção conforme o esperado; três perguntas respondíveis foram respondidas e cinco casos de recusa foram recusados.
- Consultas adicionais reutilizadas: **4/6** decisões conforme o esperado. Houve **duas recusas indevidas** em perguntas respondíveis (produto diferente e pedido parcial). A consulta de qualidade recebeu resposta; os três casos sem informação disponível foram recusados.
- Citações retornadas: **10/10** passaram na conferência de ID e literalidade. Esse é um contrato do validador, não uma medição independente de veracidade da síntese.
- Erros de infraestrutura na execução final registrada: **0**. O isolamento do LLM em subprocessos permitiu concluir as consultas sequenciais no ambiente limitado.

Os casos foram reutilizados durante o desenvolvimento; não se infere desempenho fora dessa amostra. A recusa excessiva é uma limitação material ainda presente. Os resultados das versões anteriores permanecem disponíveis, e a melhoria na demonstração não apaga as falhas do conjunto adicional. A solução é um protótipo acadêmico reproduzível, com rastreabilidade e limites explícitos.
