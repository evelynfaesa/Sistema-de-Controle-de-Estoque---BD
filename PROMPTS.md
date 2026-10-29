# Registro de uso de Inteligência Artificial

Conforme o edital (Observação 5), este arquivo registra os prompts utilizados com
ferramentas de IA, a fonte e o que o grupo fez com cada resposta.
Cada integrante adiciona abaixo os prompts que utilizou, seguindo o mesmo modelo.

---

## 1. Script SQL, dados de exemplo e diagrama relacional

- **Integrante:** Gracielly
- **Fonte:** Claude (Anthropic), via claude.ai
- **Data:** 23/10/2026
- **Prompt (resumo):** envio do edital e do modelo de 4 tabelas do grupo, com pedido de ajuda
  para criar o script das tabelas, os dados de exemplo e o diagrama relacional.
- **O que a IA gerou:** `SQL/criar_tabelas.sql`, `SQL/inserir_dados_exemplo.sql` e
  `Diagram/diagrama_relacional.png`.
- **O que o grupo fez com a resposta:** conferiu com o modelo do grupo, testou os scripts
  no Oracle, enviou ao repositório e estudou o conteúdo com o material da Unidade 5.

---

## 2. Relatórios

- **Integrante:** Gracielly
- **Fonte:** Claude (Anthropic), via claude.ai
- **Data:** 23/10/2026
- **Prompt (resumo):** pedido de explicação de consultas com JOIN e GROUP BY usando as
  tabelas do trabalho, e pedido de montagem da parte de relatórios no padrão do projeto.
- **O que a IA gerou:** consultas da pasta `src/sql` e a classe `src/reports/relatorios.py`.
- **O que o grupo fez com a resposta:** executou as consultas no Oracle, comparou com os
  exemplos das Fases 1 a 3 da aula de SQL e integrou a classe ao menu do sistema.

---

## 3. (Modelo Relacional Inicial)

- **Integrante:** Evelyn Constantino
- **Fonte:** Claude IA
- **Data:** 23/10/2026
- **Prompt (resumo):** Sistema de Controle de Estoque | Controle de produtos e fornecedores, com relatórios de estoque baixo e quantidade comprada. Nos ajude a desenvolver explicando detalhadamente qual será a melhor forma para criar um  diagrama relacional especificando os atributos, chaves, obrigatoriedades e relacionamentos

- **O que a IA gerou:** modelo com 6 tabelas (fornecedor, categoria, produto, produto_fornecedor, compra e item_compra), com atributos, tipos, chaves, relacionamentos, consultas de relatório e regras de integridade.Explicando o que é cada atributo, chave e funcionalidade.

- **O que o grupo fez com a resposta:** usou como ponto de partida e simplificou na etapa seguinte.

- 
## 4. (Conferência do diagrama e do tema)

- **Integrante:** Evelyn Constantino
- **Fonte:** Claude IA
- **Data:** 23/10/2026
- **Prompt (resumo):** Com base no diagrama em que criamos conforme as orientações do professor, está tudo nos conformes? 

- **O que a IA gerou:** confirmou que o diagrama cumpre o item 3 do edital e que o modelo cobre o tema (produtos, fornecedores, estoque baixo e quantidade comprada). Sugeriu, como opção, uma FK id_fornecedor em produtos.

- **O que o grupo fez com a resposta:** conferiu o diagrama contra o edital e o tema.

- 
---

## 5. Classes model e controllers de fornecedores e produtos

- **Integrante:** Micaellen Reis Fagundes
- **Fonte:** Claude (Anthropic), usado como apoio
- **Data:** 23/10/2026
- **Prompt (resumo):** pedido de apoio para estruturar as classes model e os controllers de
  fornecedores e produtos, seguindo o modelo relacional do grupo e o edital.
- **O que fiz com a resposta:** revisei o código com base no material da disciplina, conferi
  os itens 6.b, 6.c e 6.d do edital (incluindo a verificação de chave estrangeira na remoção),
  testei as operações de fornecedores e produtos na VM e corrigi o que foi necessário.


