# Roteiro de apresentação — até 7 minutos

**Aluna:** Viviane Demarchi. **Duração alvo:** 6min20s.  
Use a aplicação real e o README como apoio. Não é obrigatório apresentar slides. Ensaiar e cronometrar antes de enviar.

## 0:00–0:40 | Problema e proposta

**Na tela:** início da aplicação.

“Olá, eu sou Viviane Demarchi. Este projeto é o Escuta, uma solução de Voice of Customer Intelligence baseada em RAG. O problema é investigar experiências de compra em milhares de comentários sem perder a ligação entre uma conclusão e a avaliação que a sustenta. A solução usa a base pública de e-commerce da Olist, com dados históricos de 2016 a 2018.”

## 0:40–1:30 | Preparação dos dados

**Na tela:** `evidence/data_audit.json` ou a seção da base no README.

“A base de origem tem 99.224 registros de avaliação. Para o RAG, selecionei os 42.687 registros que possuem título ou comentário. Textos ausentes não foram inventados. A limpeza preserva acentos e negações, porque remover a palavra ‘não’ pode inverter o sentido de uma reclamação. Os dados de pedido e categorias foram integrados sem multiplicar uma avaliação pelos itens do pedido. A auditoria também encontrou identificadores de avaliação repetidos, tratados com uma chave adicional de documento.”

## 1:30–2:30 | Arquitetura e escolhas

**Na tela:** diagrama do README.

“A pergunta passa por uma verificação de escopo. A recuperação combina embeddings multilíngues com uma busca lexical TF-IDF. Os resultados são combinados por RRF, que soma contribuições baseadas na posição de cada resultado. Os filtros de nota, período, categoria e atraso são aplicados antes do ranking. Comentários longos são divididos em trechos de até cem tokens, com sobreposição. As evidências selecionadas seguem para um modelo Qwen local. A saída é validada: os identificadores precisam pertencer ao contexto e as citações precisam existir literalmente nos trechos.”

## 2:30–3:45 | Demonstração de reclamações

**Na tela:** notas 1 e 2; pergunta “O que os clientes relatam sobre atrasos na entrega?”.

“Vou investigar atrasos nas avaliações de notas baixas. O sistema recupera comentários relacionados à pergunta e gera achados acompanhados de citações. Aqui posso expandir a avaliação, conferir o texto original, a nota, a data e os identificadores. Essa ligação permite verificar de onde veio cada afirmação.”

**Ação:** leia um achado curto efetivamente exibido e abra sua evidência. Não use uma frase decorada se a execução retornar outra resposta. Se houver abstenção, explique-a e use uma das consultas bem-sucedidas registradas, mostrando uma nova execução real.

## 3:45–4:35 | Demonstração de elogios e contexto

**Na tela:** notas 4 e 5; pergunta “Quais elogios se referem à entrega antes do prazo?”.

“Agora mudo o recorte para notas altas e procuro elogios. Os filtros permitem comparar experiências diferentes. A categoria é do pedido e pode conter vários produtos, então não atribuo automaticamente o comentário a um produto específico.”

**Ação:** mostre um achado e uma fonte correspondente.

## 4:35–5:20 | Limitações e abstenção

**Na tela:** pergunta “Como foi a entrega em 2026?”; depois “Qual o percentual de clientes com atrasos?”.

“Como a base é histórica, o sistema não responde sobre 2026. Ele também não transforma os resultados da busca em percentuais de toda a base. Para medir frequência de temas, seria necessário classificar e agregar o conjunto completo. Reconhecer essas limitações evita respostas convincentes, mas sem fundamento.”

## 5:20–6:05 | Avaliação

**Na tela:** `docs/AVALIACAO.md` e arquivos de evidências.

“A avaliação separa testes de integridade, comparação de recuperação e execuções do modelo. Comparei busca lexical, semântica e híbrida em um conjunto pequeno de perguntas. Os resultados e os julgamentos estão no repositório para permitir reprodução. Os julgamentos são assistidos por IA e não substituem avaliadores independentes. Também há testes para impedir citações inexistentes, verificar integrações e distinguir falha do modelo de ausência de evidência.”

**Ação:** cite apenas os números da versão final de `docs/AVALIACAO.md`. Não diga que busca híbrida foi superior se os resultados não mostrarem isso.

## 6:05–6:25 | Encerramento

“O principal resultado é uma investigação rastreável das avaliações, com filtros e tratamento explícito de limitações. O repositório reúne código, instruções, decisões técnicas e evidências. Como evolução, eu ampliaria a avaliação humana, calibraria melhor a abstenção e adicionaria classificação temática para responder perguntas estatísticas.”

## Antes de gravar

- Abrir a aplicação e carregar os modelos antes de começar.
- Deixar o diagrama e a avaliação acessíveis.
- Confirmar que o vídeo mostra uma execução real e fontes legíveis.
- Conferir áudio, duração inferior a 7 minutos e acesso ao vídeo.
- Usar seu nome e explicar as escolhas com suas palavras; reler o guia de conceitos.
