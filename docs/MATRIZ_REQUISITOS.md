# Matriz de atendimento ao briefing

| Exigência | Implementação | Evidência / demonstração |
|---|---|---|
| Base Brazilian E-Commerce Public Dataset by Olist | Download oficial de quatro CSVs | `src/voc/cli.py`, hashes em `evidence/source_sha256.json` |
| Seleção e limpeza justificadas | Título ou comentário; limpeza conservadora | `src/voc/data.py`, `README.md` |
| Valores ausentes | Sem texto excluído; datas desconhecidas mantidas como desconhecidas | Auditoria e testes em `tests/test_pipeline.py` |
| Organização de documentos | Avaliação com chave adicional; chunks com IDs | `documents.jsonl`, `passages.jsonl`, manifesto |
| Embeddings | MiniLM multilíngue com revisão fixada | `src/voc/retrieval.py`, `evidence/index_manifest.json` |
| Armazenamento e indexação | JSONL + matriz NumPy normalizada + TF-IDF | `retrieval.build`, checksums e dimensões |
| Processamento da pergunta | Normalização de espaços e regras de escopo | `scope_reason`, limite de tamanho |
| Recuperação semântica | Cosseno em embeddings, com filtros prévios | `Retriever.search`, comparação com baseline |
| Seleção relevante | RRF, piso de similaridade e deduplicação | `evaluation/queries.json` e `qrels.json` |
| Construção do contexto | Trechos e IDs serializados como dados | `Generator.generate` |
| Geração por modelo de linguagem | Qwen local com saída JSON | `src/voc/rag.py`, execuções em `evidence/` |
| Respostas fundamentadas | IDs e citações literais validados; verificação semântica adicional | Achados e fontes na interface |
| Perguntas sem evidências | Abstenção por escopo, busca vazia ou validação | Demonstração de período inexistente, filtros vazios e premissa sem suporte |
| Rastreabilidade | review_id, order_id, doc_id, chunk_id, posição do registro | Expandir fonte e baixar investigação em JSON |
| Metadados (opcional) | Nota, período, categoria e atraso | Filtros na barra lateral; testes de aplicação antes do top-k |
| Código e instruções | Pacote Python e README | Instalação, download, preparo, índice, aplicação e testes |
| Arquitetura e tecnologias | Diagrama e contratos dos componentes | `README.md`, `docs/ARQUITETURA.md` |
| Justificativas técnicas | Dados, granularidade, busca, modelo e limites | README, relatório e avaliação |
| Exemplos de perguntas e respostas | Saídas reais, com falhas e recusas documentadas | `evidence/demo_runs.json` |
| Reprodução | Revisão do embedding, hashes e versões | `requirements-validated.txt`, `evidence/environment.json` |
| Repositório público GitHub | Publicado | https://github.com/vicdemarchi/tech-challenge-fase4-voc-rag |
| Vídeo de até 7 minutos | Material complementar de apresentação | Arquivo de vídeo submetido separadamente |
| Bônus Databricks (opcional) | Não executado | Sem reivindicação de bonificação |
