# Evidências de execução

## Versão final

| Arquivo | Conteúdo |
|---|---|
| `data_audit.json` | Contagens, elegibilidade, integração e hashes dos CSVs |
| `index_manifest.json` | Modelo, revisão, dimensões, chunks e hashes do índice |
| `environment.json` | Versões e configuração do modelo local |
| `tests.txt` | Resultado dos testes automatizados |
| `interface_test.json` | Verificações da interface via AppTest |
| `retrieval_runs.json` | Rankings dos três métodos de busca |
| `retrieval_metrics.json` | Métricas e resultados por pergunta |
| `demo_runs.json` | Oito consultas da demonstração com fontes e decisões |
| `generation_holdout_runs.json` | Seis consultas adicionais; conjunto reutilizado após ajustes, sem independência de teste |
| `generation_summary.json` | Resumo das verificações de geração, escopo e citações |

## Histórico de diagnóstico

`development_v1.json`, `development_v2.json` e `development_v3.json` registram configurações intermediárias, incluindo falhas identificadas. `baseline_conservative_demo.json` e `baseline_conservative_additional.json` registram a configuração com verificação global, anterior à decisão individual por achado. A versão final está nos arquivos indicados na tabela acima.

As avaliações e os julgamentos são assistidos por IA. A interpretação e os limites estão em `docs/AVALIACAO.md`. Os resultados não constituem uma medição de acurácia geral.
