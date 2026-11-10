# Comece aqui — Viviane Demarchi

## O que este trabalho faz?

Você pergunta sobre experiências de compra. O programa procura comentários reais da Olist, entrega os trechos a um modelo de linguagem e apresenta uma resposta com as fontes. Esse processo se chama RAG: geração apoiada em recuperação de informações.

Uma analogia: antes de redigir uma conclusão, o analista separa os depoimentos que vai usar. A resposta vem acompanhada desses depoimentos para permitir conferência.

## O que já está nos arquivos?

Código, documentação, auditoria dos dados, testes, avaliação e roteiro. Consulte `docs/AVALIACAO.md` para saber exatamente quais etapas foram executadas e quais precisam de validação no seu computador. Não apresente como concluído algo marcado como pendente.

## O que falta para entregar à faculdade?

1. Abrir e testar a aplicação no computador que será usado na gravação.
2. Publicar os arquivos em um repositório **público** no GitHub.
3. Gravar um vídeo de até **7 minutos**, com uma demonstração real.
4. Enviar o link do repositório e o vídeo conforme o formato solicitado no portal da faculdade. O briefing não determina se o portal exige ZIP: conferir na página da atividade.

O bônus Databricks depende da conclusão real da trilha Generative AI Engineering Pathway pela aluna e de comprovante identificável. Ele não foi realizado nem está incluído no pacote. O briefing menciona +10 pontos, mas não fornece a fórmula completa de composição da nota. A nota máxima não pode ser garantida.

## Passo a passo no Windows

### A. Abrir o projeto

1. Baixe e extraia o ZIP. Não execute os arquivos de dentro do ZIP.
2. Abra o VS Code.
3. Clique em **Arquivo → Abrir Pasta**.
4. Selecione a pasta `fase4-voz-do-cliente`, que contém `README.md`, `app.py` e `pyproject.toml`.
5. Clique em **Terminal → Novo Terminal**. Os comandos devem ser executados nessa pasta.
6. Siga os comandos de instalação do README, um de cada vez. Eles usam o Python da pasta `.venv`; assim, não é necessário alterar a política de execução do PowerShell.

Se `py -3.12` não funcionar, instale Python 3.12 pelo site oficial https://www.python.org/downloads/ e reabra o terminal. Se já houver outra versão instalada, não a remova.

### B. Instalar o modelo de resposta

O caminho mais simples no Windows é instalar Ollama, abrir a aplicação e executar `ollama pull qwen2.5:3b`. Isso baixa um modelo para seu computador. A primeira instalação precisa de internet. A geração posterior acontece localmente.

A instalação Python de llama.cpp é alternativa para reproduzir exatamente o backend testado. Pode exigir compilador no Windows; não é necessária se você escolher Ollama.

Depois da instalação e da criação do índice, você também pode abrir `INICIAR_WINDOWS.bat` com dois cliques. Ele inicia a interface; o Ollama precisa estar aberto.

### C. Conferir a demonstração

Na interface, filtre notas **1 e 2** e pergunte sobre atrasos. Confira uma citação na avaliação expandida. Depois filtre notas **4 e 5** e pergunte sobre elogios. Finalmente, faça uma pergunta sobre 2026 e mostre a recusa justificada.

Não use apenas as respostas gravadas nos arquivos como se fossem uma execução ao vivo. Elas servem para comparação e auditoria.

### D. Publicar no GitHub

Sugestão de nome: `tech-challenge-fase4-voc-rag`.

Se usar GitHub Desktop: adicione a pasta como repositório local (ou crie um repositório nela), confira os arquivos exibidos, faça o primeiro commit e clique em **Publish repository**. Desmarque **Keep this code private**, pois o briefing exige repositório público.

Confira se o `.gitignore` está presente. Não inclua `.venv`, dados brutos, `artifacts`, modelos, `.env` ou credenciais. Os arquivos pequenos de `evidence` e `evaluation` devem entrar: eles demonstram o trabalho executado.

Abra a página do repositório sem login ou em janela anônima e confirme que o README pode ser lido. Não há necessidade de criar branch ou pull request para uma entrega individual simples.

### E. Gravar o vídeo

Use `docs/ROTEIRO_VIDEO.md`. Mire aproximadamente 6 minutos para ter margem até 7. Se o modelo estiver lento, grave a consulta e corte parte da espera, indicando que o tempo foi abreviado. Não afirme um tempo de resposta menor do que o real.

## Termos que você precisa entender

| Termo | Significado neste projeto |
|---|---|
| RAG | Buscar comentários e usá-los como contexto para a resposta |
| Embedding | Lista de números que representa características semânticas do texto |
| Busca semântica | Encontrar textos de sentido próximo à pergunta |
| TF-IDF | Dar peso a palavras e combinações de palavras para uma busca lexical |
| Chunk | Trecho pequeno de um comentário longo |
| Metadado | Nota, data, categoria e outros dados associados ao comentário |
| RRF | Combinar as posições de duas listas de resultados |
| LLM | Modelo de linguagem que redige a síntese |
| Alucinação | Informação gerada sem sustentação nas evidências |
| Abstenção | Reconhecer que não há suporte suficiente para responder |
| Top-k | Os k resultados selecionados pela busca, não toda a população |

## Perguntas que podem fazer na avaliação

**Por que não usar somente a nota?** A nota indica satisfação de forma aproximada, mas o texto pode explicar o motivo e até contradizer essa nota.

**Por que não remover “não” na limpeza?** Porque isso pode inverter o sentido, por exemplo transformar “não recebi” em “recebi”.

**Por que não usar `review_id` como chave única?** A auditoria encontrou repetições. O projeto preserva os registros e cria uma chave de documento adicional.

**Por que a busca não prova o problema mais frequente?** Ela seleciona os exemplos mais próximos da pergunta. Isso não equivale a contar o tema em todas as avaliações.

**Uma citação válida garante uma conclusão correta?** Não. O código verifica se a citação existe e se pertence à fonte, mas ainda é necessário avaliar se ela sustenta a síntese.

**Por que escolher um modelo pequeno?** Para viabilizar execução local e sem cobrança por API. A contrapartida é capacidade limitada, explicitada na avaliação.
