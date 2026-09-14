# Classificação Técnica — Vulnerabilidades Confirmadas (VULN-001 a VULN-010)

| Item | Valor |
|---|---|
| Data | 2026-09-14 |
| Fontes | `docs/00-contexto/escopo.md` e `docs/01-inventario/inventario-vulnerabilidades.md` (nenhum outro arquivo foi lido nesta etapa) |
| Itens classificados | VULN-001 a VULN-010, marcados como "vulnerabilidade confirmada" (VC) no inventário |
| Itens fora desta etapa | VULN-011 a VULN-021 (riscos de configuração e pontos de validação manual) |
| Revisão de código de referência | commit `598e025`, conforme o inventário |
| Natureza | Classificação baseada em análise estática. Nenhum teste dinâmico foi executado |
| Sanitização | Sem segredos, IPs, e-mails, tokens, senhas ou payloads. Trechos de código aparecem só como referência estrutural, com valores sensíveis redigidos |

---

## 1. Método

### 1.1 CVSS v3.1

- Foram calculadas apenas as **métricas base**. As métricas temporais e ambientais dependem do ambiente implantado e ficam para a matriz de risco (`03-matriz-risco`).
- A fórmula e os pesos são os da especificação FIRST CVSS v3.1, com a função *Roundup* oficial. Os scores foram recalculados por script e conferidos com valores de referência conhecidos.
- **Pontuação individual:** cada vulnerabilidade foi pontuada isoladamente, como exige a especificação. Encadeamentos (ex.: VULN-001 + VULN-009) são descritos nas justificativas, mas não inflam o score base.
- **Pior caso razoável:** quando mais de um perfil consegue explorar o item, o vetor usa o perfil de **menor privilégio** que o código comprovadamente aceita.
- **Escala de severidade:** 0,0 Nenhuma · 0,1–3,9 Baixa · 4,0–6,9 Média · 7,0–8,9 Alta · 9,0–10,0 Crítica.

### 1.2 OWASP Top 10 2021 e CWE

- A categoria OWASP segue a **lista oficial de CWEs mapeadas** de cada categoria de 2021 sempre que a CWE principal consta nela. Quando não consta, o mapeamento é feito **por afinidade**, e isso está indicado no item.
- A CWE principal é a entrada mais específica compatível com a evidência. A secundária só aparece quando descreve um aspecto que a principal não cobre.

### 1.3 CVE/NVD e MITRE ATT&CK

- **CVE:** VULN-001 a VULN-010 estão todos em **código próprio** da aplicação. Nenhum decorre de defeito em dependência de terceiros, então CVE/NVD é "não aplicável" em todos.
- **ATT&CK:** foi usada a matriz Enterprise. Técnicas só foram indicadas quando existe cenário realista coerente com os pré-requisitos do item.

### 1.4 Ajustes em relação ao inventário preliminar

| ID | Inventário (preliminar) | Classificação técnica | Motivo |
|---|---|---|---|
| VULN-002 | CWE-602 (principal) | CWE-472 (principal), CWE-602 (secundária) | O preço é um parâmetro que se supõe imutável, mas é controlado externamente. CWE-472 descreve isso de forma mais específica |
| VULN-003 | Severidade "Alta" | 9,8 **Crítica** | Resultado do vetor CVSS: sem autenticação, com impacto total |
| VULN-004 | A07:2021 | **A01:2021** | CWE-540 consta na lista oficial de A01:2021 |
| VULN-007 | CWE-840 / CWE-863 / CWE-20 | CWE-863 (principal), CWE-841 (secundária) | CWE-840 é categoria, não fraqueza. CWE-841 cobre a falta de fluxo de estados. CWE-20 (nota) segue pendente de validação |
| VULN-009 | A02 / A09; CWE-532 | **A01:2021**; CWE-215 (secundária) | CWE-922 consta na lista oficial de A01:2021. O dado sensível vai para código de depuração (console do navegador), não para arquivo de log |
| VULN-010 | Severidade "Baixa" | 0,0 **Nenhuma** | Nenhum impacto em confidencialidade, integridade ou disponibilidade é demonstrável estaticamente. É uma fraqueza de robustez |

---

## 2. Resumo

| ID | Título | CWE principal / secundária | OWASP 2021 | Vetor CVSS v3.1 | Score | Severidade | CVE | ATT&CK |
|---|---|---|---|---|---|---|---|---|
| VULN-003 | Credencial padrão de administrador fixa no código | CWE-798 / CWE-1392 | A07 | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | 9,8 | Crítica | Não aplicável | T1078.001 |
| VULN-005 | Login sem limite de tentativas | CWE-307 / — | A07 | `AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` | 7,4 | Alta | Não aplicável | T1110.001, T1110.003, T1110.004 |
| VULN-006 | Política de senha fraca | CWE-521 / — | A07 | `AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` | 7,4 | Alta | Não aplicável | T1110.001, T1110.003 |
| VULN-002 | Preço do item definido pelo cliente | CWE-472 / CWE-602 | A04 | `AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N` | 6,5 | Média | Não aplicável | T1565.001 |
| VULN-001 | XSS armazenado | CWE-79 / — | A03 | `AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N` | 5,4 | Média | Não aplicável | T1059.007, T1528 |
| VULN-009 | Token em `localStorage` e no console | CWE-922 / CWE-215 | A01 | `AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N` | 4,4 | Média | Não aplicável | T1528, T1550.001 |
| VULN-004 | Token JWT versionado no git | CWE-540 / CWE-359 | A01 | `AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` | 4,3 | Média | Não aplicável | T1552.001 |
| VULN-007 | Atualização de pedido sem autorização por campo nem fluxo | CWE-863 / CWE-841 | A01 | `AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N` | 4,3 | Média | Não aplicável | T1565.001 |
| VULN-008 | Paginação sem limites e divisão por zero | CWE-770 / CWE-369 | A04 (afinidade) | `AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L` | 4,3 | Média | Não aplicável | T1499.003 |
| VULN-010 | Exceções de banco não tratadas | CWE-755 / CWE-20 | A04 (afinidade) | `AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:N` | 0,0 | Nenhuma | Não aplicável | Não aplicável |

Todos os vetores têm o prefixo `CVSS:3.1/`, omitido na tabela por espaço. A ordem é por score, do maior para o menor.

**Distribuição:** 1 Crítica · 2 Altas · 6 Médias · 1 Nenhuma.

---

## 3. Classificação detalhada

### VULN-001 — XSS armazenado via observações do pedido e dados de produto

**1. Identificação e escopo afetado**
- **Componente vulnerável:** frontend. Telas `atendente/acompanhar_pedidos`, `chapeiro/preparar_pedidos`, `atendente/menu`, `admin/gerenciar_produtos` e `atendente/registrar_avaliacao`.
- **Origem dos dados:** API backend, campos `notes` (pedido) e `name`/`description` (produto).
- **Usuários afetados:** qualquer operador que abra essas telas, inclusive administradores.

**2. Evidência sanitizada**

| Arquivo | Linhas | Observação |
|---|---|---|
| `projeto_aplicado_foodtruck_frontend-main/public/atendente/acompanhar_pedidos.js` | 269–276 | `innerHTML` com interpolação de `notes` sem escape |
| `projeto_aplicado_foodtruck_frontend-main/public/chapeiro/preparar_pedidos.js` | 269–277 | Mesmo padrão com `notes` |
| `projeto_aplicado_foodtruck_frontend-main/public/atendente/menu.js` | 122–123, 192–197 | `innerHTML` com `name` e `description` de produto |
| `projeto_aplicado_foodtruck_frontend-main/public/admin/gerenciar_produtos.js` | 170–175 | `innerHTML` com `name` e `description` |
| `projeto_aplicado_foodtruck_frontend-main/public/atendente/acompanhar_pedidos.js` | 119–122 | Nome de produto vindo do cache, interpolado em HTML |
| `projeto_aplicado_foodtruck_frontend-main/public/atendente/registrar_avaliacao.js` | 151–152 | Idem |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/order/schemas.py` | 28, 37 | `notes: Optional[str]`, sem restrição de conteúdo |

**3. CWE**
- **Principal:** CWE-79 — Improper Neutralization of Input During Web Page Generation (Cross-site Scripting).
- **Secundária:** não necessária.

**4. OWASP Top 10 2021:** A03:2021 – Injection. CWE-79 consta na lista oficial da categoria.

**5. CVSS v3.1**
- **Vetor:** `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N`
- **Score:** 5,4 · **Severidade:** Média

| Métrica | Valor | Justificativa |
|---|---|---|
| AV (Attack Vector) | N | O conteúdo é gravado pela API HTTP e entregue remotamente ao navegador da vítima |
| AC (Attack Complexity) | L | Não há sanitização, escape nem CSP no fluxo evidenciado. Nenhuma condição fora do controle do atacante |
| PR (Privileges Required) | L | O campo `notes` é gravável por perfis operacionais (`attendant`/`kitchen`). Um perfil `admin` também grava produtos, mas o vetor usa o menor privilégio suficiente |
| UI (User Interaction) | R | A vítima precisa abrir uma das telas que renderizam o conteúdo |
| S (Scope) | C | O componente vulnerável (renderização no frontend) afeta um componente distinto: a sessão no navegador de outro usuário |
| C (Confidentiality) | L | O script acessa dados disponíveis na sessão da vítima. O acesso amplo depende do perfil da vítima e do encadeamento com VULN-009, que não entram no score base |
| I (Integrity) | L | O script pode executar ações da vítima pela API dentro das permissões dela. Pelo mesmo motivo, fica em L no score base |
| A (Availability) | N | Nenhuma perda de disponibilidade demonstrada |

**6. CVE/NVD:** não aplicável (código próprio).

**7. MITRE ATT&CK**

| Tática | Técnica | Justificativa |
|---|---|---|
| Execution | T1059.007 — Command and Scripting Interpreter: JavaScript | O conteúdo gravado é interpretado como JavaScript no navegador da vítima |
| Credential Access | T1528 — Steal Application Access Token | Cenário realista só em cadeia com VULN-009: o token Bearer fica em `localStorage`, legível por script da mesma origem |

**8. Pré-requisitos, impacto e limitações**
- **Pré-requisitos:** conta autenticada com perfil que grave `notes` (ou `admin`, para produtos), e uma vítima que abra a tela afetada.
- **Impacto técnico:** execução de script arbitrário no contexto da vítima. Em cadeia com VULN-009, o token de sessão pode ser roubado e usado para ações com os privilégios da vítima.
- **Limitações de validação:**
  - A execução efetiva no navegador **necessita validação manual** em ambiente autorizado, com teste de injeção de HTML inofensivo (sem script).
  - Se administradores de fato usam as telas afetadas no dia a dia **necessita validação manual**. Isso muda o impacto contextual na matriz de risco, não o score base.
  - Se existe algum cabeçalho CSP aplicado pela infraestrutura implantada **necessita validação manual**. O inventário não encontrou CSP no código nem na configuração versionada.

---

### VULN-002 — Preço do item do pedido definido pelo cliente

**1. Identificação e escopo afetado**
- **Componente:** backend, endpoint `POST /api/v1/orders/`, módulo `resources/order`.
- **Perfis capazes de explorar:** `attendant` e `admin`.
- **Dados afetados:** valores de itens e totais de pedidos, que alimentam faturamento, relatórios e ranking.

**2. Evidência sanitizada**

| Arquivo | Linhas | Observação |
|---|---|---|
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/order/schemas.py` | 11–18 | `CreateOrderItemDTO` aceita `price` enviado pelo cliente |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/order/controller.py` | 381–395 | O produto é buscado só para checar se existe. O item é criado a partir do DTO e o total é somado com o preço recebido |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/order/model.py` | 54–55 | `calculate_total` usa `quantity × price` do item |
| `projeto_aplicado_foodtruck-main/tests/test_api_order.py` | 328–350 | O teste `test_order_total_with_small_price` aceita um preço arbitrário e confirma que o total reflete esse valor |
| `projeto_aplicado_foodtruck_frontend-main/public/atendente/menu.js` | 338–339 | O frontend envia o preço a partir do carrinho no navegador |

**3. CWE**
- **Principal:** CWE-472 — External Control of Assumed-Immutable Web Parameter.
- **Secundária:** CWE-602 — Client-Side Enforcement of Server-Side Security. A regra de preço, que deveria ser do servidor, depende do valor montado no cliente.

**4. OWASP Top 10 2021:** A04:2021 – Insecure Design. CWE-472 e CWE-602 constam na lista oficial da categoria.

**5. CVSS v3.1**
- **Vetor:** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N`
- **Score:** 6,5 · **Severidade:** Média

| Métrica | Valor | Justificativa |
|---|---|---|
| AV | N | Explorável pela API HTTP |
| AC | L | Basta alterar um campo da requisição. A suíte de testes demonstra que o servidor aceita o valor |
| PR | L | Exige conta autenticada com perfil operacional (`attendant`) |
| UI | N | Nenhuma ação de outro usuário é necessária |
| S | U | O impacto fica restrito aos dados do próprio backend |
| C | N | Nenhuma leitura indevida de dados |
| I | H | O atacante controla **integralmente** o valor financeiro gravado em cada pedido que registra. É modificação de dado com consequência direta e séria |
| A | N | Nenhum efeito sobre disponibilidade |

**6. CVE/NVD:** não aplicável (código próprio).

**7. MITRE ATT&CK**

| Tática | Técnica | Justificativa |
|---|---|---|
| Impact | T1565.001 — Data Manipulation: Stored Data Manipulation | Cenário realista de ameaça interna: um operador registra pedidos com valores adulterados, afetando registros financeiros persistidos |

**8. Pré-requisitos, impacto e limitações**
- **Pré-requisitos:** conta `attendant` ou `admin` e acesso à API, direto ou por ferramenta que modifique a requisição.
- **Impacto técnico:** perda de integridade de valores de pedidos e totais, e distorção de relatórios e do ranking de vendas.
- **Limitações de validação:**
  - Se existe conciliação fora do sistema (caixa, PDV) que detecte divergências **necessita validação manual**. Isso afeta o risco de negócio, não o score base.
  - O comportamento no banco PostgreSQL implantado **necessita validação manual**. A evidência vem do código e da suíte de testes; os testes não foram executados nesta etapa.

---

### VULN-003 — Credencial padrão de administrador fixa no código e na documentação

**1. Identificação e escopo afetado**
- **Componente:** backend. Script de inicialização `create_admin.py`, modelo de variáveis `.env.template` e documentação (`docs/` do backend).
- **Endpoint de exploração:** `POST /api/v1/token/`.
- **Conta afetada:** usuário administrador criado pelo script, em qualquer instalação que o tenha executado sem trocar a senha.

**2. Evidência sanitizada**

| Arquivo | Linhas | Observação |
|---|---|---|
| `projeto_aplicado_foodtruck-main/create_admin.py` | 13–19 | Cria o usuário `admin` com perfil `ADMIN` e senha literal no código (valor redigido) |
| `projeto_aplicado_foodtruck-main/.env.template` | 14–16 | Senha padrão do administrador como valor de exemplo (valor redigido) |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/` | — | O inventário registra que a variável `DEFAULT_ADMIN_PASSWORD` não é referenciada pelo código |
| `projeto_aplicado_foodtruck-main/docs/` e `README.md` | — | O inventário registra 9 arquivos com a mesma senha padrão em exemplos. As linhas não foram reproduzidas para não expor o valor |

**3. CWE**
- **Principal:** CWE-798 — Use of Hard-coded Credentials.
- **Secundária:** CWE-1392 — Use of Default Credentials.

**4. OWASP Top 10 2021:** A07:2021 – Identification and Authentication Failures. CWE-798 consta na lista oficial da categoria.

**5. CVSS v3.1**
- **Vetor:** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`
- **Score:** 9,8 · **Severidade:** Crítica

| Métrica | Valor | Justificativa |
|---|---|---|
| AV | N | O login é feito pela API HTTP |
| AC | L | A credencial é pública no repositório e na documentação. Não há condição especial nem limite de tentativas (VULN-005) |
| PR | N | Nenhuma autenticação prévia é necessária |
| UI | N | Nenhuma interação de outro usuário |
| S | U | O impacto fica dentro da aplicação backend e de seus dados |
| C | H | O perfil `admin` lê todos os usuários, produtos e pedidos |
| I | H | O perfil `admin` cria, altera e exclui usuários (inclusive perfis) e produtos |
| A | H | O perfil `admin` pode excluir usuários e produtos, o que torna a operação inviável para os demais operadores |

**6. CVE/NVD:** não aplicável (código próprio).

**7. MITRE ATT&CK**

| Tática | Técnica | Justificativa |
|---|---|---|
| Initial Access / Persistence / Privilege Escalation | T1078.001 — Valid Accounts: Default Accounts | Uso de conta administrativa padrão, com credencial conhecida publicamente, para obter acesso legítimo à aplicação |

**8. Pré-requisitos, impacto e limitações**
- **Pré-requisitos:** acesso de rede ao endpoint de login, e uma instalação onde a conta criada pelo script mantém a senha padrão.
- **Impacto técnico:** comprometimento administrativo completo da aplicação.
- **Limitações de validação:**
  - Se cada ambiente implantado usou o script e se a senha foi trocada depois **necessita validação manual**, feita pelo responsável do ambiente, sem tentativa de login com a credencial.
  - O score assume o cenário em que a conta padrão existe. Em ambientes onde ela não existe ou foi alterada, o item não é explorável, mas o defeito de código continua.

---

### VULN-004 — Token JWT de administrador versionado no git (`token.json`)

**1. Identificação e escopo afetado**
- **Componente:** repositório git (raiz), arquivo `token.json` introduzido no commit `598e025`.
- **Dados expostos:** resposta de login de conta administrativa (token de acesso, identificador, nome de usuário, e-mail e perfil).
- **Afetados:** a conta administrativa exposta e, indiretamente, o segredo de assinatura JWT da aplicação.

**2. Evidência sanitizada**

| Artefato | Referência | Observação |
|---|---|---|
| Histórico git | commit `598e025` | Adição de `token.json` (registrada no inventário via `git log -- token.json`) |
| `.gitignore` da raiz | — | Inexistente. `git check-ignore` não retorna regra para o arquivo |
| Estrutura do arquivo | chaves de primeiro nível | `access_token`, `token_type`, `user` (valores não reproduzidos) |
| Metadados do token | cabeçalho e claims | Algoritmo HS256, claims `sub` e `exp`, expiração em 2026-05-16 01:04 UTC (expirado) |
| `docs/00-contexto/escopo.md` | linha 20 | O escopo determina que `token.json` não seja versionado, e isso foi descumprido |

O arquivo não tem "linhas" de código relevantes. A referência verificável é o commit e a estrutura de chaves.

**3. CWE**
- **Principal:** CWE-540 — Inclusion of Sensitive Information in Source Code (artefato sensível dentro do repositório de código).
- **Secundária:** CWE-359 — Exposure of Private Personal Information to an Unauthorized Actor (identificadores e e-mail da conta administrativa).

**4. OWASP Top 10 2021:** A01:2021 – Broken Access Control. CWE-540 e CWE-359 constam na lista oficial da categoria.

**5. CVSS v3.1**
- **Vetor:** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N`
- **Score:** 4,3 · **Severidade:** Média

| Métrica | Valor | Justificativa |
|---|---|---|
| AV | N | Repositório acessível pela rede (hospedagem git remota) |
| AC | L | Basta ler o arquivo no histórico |
| PR | L | Exige permissão de leitura no repositório. A visibilidade (público ou privado) **necessita validação manual**. Se o repositório for público, PR passa a N e o score fica 5,3 (Média) |
| UI | N | Nenhuma interação necessária |
| S | U | A exposição fica restrita ao ativo repositório e aos dados da conta |
| C | L | Confirmados: exposição de identificadores e e-mail da conta administrativa e de um token já expirado. O acesso amplo exigiria forjar tokens, o que depende da entropia do segredo e não é demonstrável |
| I | N | Com token expirado, nenhuma modificação é demonstrável |
| A | N | Nenhum efeito sobre disponibilidade |

**6. CVE/NVD:** não aplicável (código e artefato próprios).

**7. MITRE ATT&CK**

| Tática | Técnica | Justificativa |
|---|---|---|
| Credential Access | T1552.001 — Unsecured Credentials: Credentials In Files | Material de autenticação (token) armazenado em arquivo versionado |

Técnicas de reconhecimento em repositórios públicos só se aplicariam se a visibilidade pública fosse confirmada, que **necessita validação manual**. Por isso não foram atribuídas.

**8. Pré-requisitos, impacto e limitações**
- **Pré-requisitos:** acesso de leitura ao repositório ou a qualquer clone.
- **Impacto técnico:**
  - Exposição de dados pessoais da conta administrativa (relevante para a LGPD).
  - Um par mensagem/assinatura HS256 disponível para tentativa offline de descobrir o segredo de assinatura.
  - Persistência da exposição no histórico, mesmo que o arquivo seja removido.
- **Limitações de validação:**
  - Visibilidade do repositório e lista de pessoas com acesso: **necessita validação manual**.
  - Entropia real de `JWT_SECRET_KEY` em cada ambiente: **necessita validação manual**, sem expor o valor. Se ela for baixa, a forja de tokens elevaria C e I, mas isso não entra no score por não ser demonstrável.
  - Se o token foi usado indevidamente enquanto estava válido: **necessita validação manual**, por análise de logs de acesso, se existirem.

---

### VULN-005 — Endpoint de login sem limite de tentativas

**1. Identificação e escopo afetado**
- **Componente:** backend, endpoint `POST /api/v1/token/` (`auth/token.py`). Também o roteamento Traefik definido em `docker-compose.yaml`.
- **Contas afetadas:** todas as contas da aplicação, de qualquer perfil.

**2. Evidência sanitizada**

| Arquivo | Linhas | Observação |
|---|---|---|
| `projeto_aplicado_foodtruck-main/projeto_aplicado/auth/token.py` | 81–96 | A resposta HTTP 429 existe só como documentação OpenAPI |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/auth/token.py` | 152–186 | O fluxo de autenticação não tem contagem de tentativas, atraso nem bloqueio |
| `projeto_aplicado_foodtruck-main/docs/pt-br/API.md` | 722 | A documentação promete limite de taxa |
| `projeto_aplicado_foodtruck-main/docker-compose.yaml` | 24–27 | Labels do Traefik sem middleware de limitação |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/` | — | Busca por bibliotecas ou middlewares de limitação sem ocorrências (registrado no inventário) |

**3. CWE**
- **Principal:** CWE-307 — Improper Restriction of Excessive Authentication Attempts.
- **Secundária:** não necessária.

**4. OWASP Top 10 2021:** A07:2021 – Identification and Authentication Failures. CWE-307 consta na lista oficial da categoria.

**5. CVSS v3.1**
- **Vetor:** `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`
- **Score:** 7,4 · **Severidade:** Alta

| Métrica | Valor | Justificativa |
|---|---|---|
| AV | N | O endpoint é acessível pela rede |
| AC | H | O sucesso depende de condição fora do controle do atacante: existir ao menos uma conta com senha adivinhável dentro do volume de tentativas viável |
| PR | N | Nenhuma autenticação prévia |
| UI | N | Nenhuma interação |
| S | U | O impacto fica dentro da aplicação |
| C | H | Uma conta obtida pode ser administrativa. A API permite criar contas `admin` (ver VULN-006), então o pior caso é leitura total |
| I | H | Mesmo raciocínio: modificação total com perfil `admin` |
| A | N | Consumo de CPU por verificações Argon2 em massa é plausível, mas a magnitude **necessita validação manual**. Por isso não foi pontuado |

**6. CVE/NVD:** não aplicável (código próprio; ausência de controle, não defeito de dependência).

**7. MITRE ATT&CK**

| Tática | Técnica | Justificativa |
|---|---|---|
| Credential Access | T1110.001 — Brute Force: Password Guessing | Tentativas repetidas contra uma conta, sem bloqueio |
| Credential Access | T1110.003 — Brute Force: Password Spraying | Poucas senhas comuns contra muitas contas, sem limitação por origem |
| Credential Access | T1110.004 — Brute Force: Credential Stuffing | Reuso de credenciais vazadas de terceiros, sem limitação |

**8. Pré-requisitos, impacto e limitações**
- **Pré-requisitos:** acesso de rede ao endpoint e existência de contas com senha fraca ou reutilizada.
- **Impacto técnico:** tomada de contas, inclusive administrativas, e potencial degradação por carga de hashing.
- **Limitações de validação:**
  - Se existe WAF, proxy ou limitação de rede à frente do backend em produção: **necessita validação manual**.
  - O efeito de negação de serviço por carga Argon2: **necessita validação manual**, por teste de carga controlado em ambiente autorizado.
  - O score é independente de VULN-003 e VULN-006. A combinação é tratada na matriz de risco.

---

### VULN-006 — Política de senha fraca (mínimo de 6 caracteres)

**1. Identificação e escopo afetado**
- **Componente:** backend, esquemas de criação e atualização de usuário (`resources/user/schemas.py`), usados por `POST /api/v1/users/` e `PATCH /api/v1/users/{id}`.
- **Contas afetadas:** todas as contas criadas ou alteradas pela API, de qualquer perfil, inclusive `admin`.

**2. Evidência sanitizada**

| Arquivo | Linhas | Observação |
|---|---|---|
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/user/schemas.py` | 25 | Senha na criação com restrição única de comprimento mínimo 6 |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/user/schemas.py` | 33 | Mesma regra na atualização |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/user/controller.py` | 235–238 | Exemplo de erro "senha fraca" só documental, sem regra correspondente |

**3. CWE**
- **Principal:** CWE-521 — Weak Password Requirements.
- **Secundária:** não necessária.

**4. OWASP Top 10 2021:** A07:2021 – Identification and Authentication Failures. CWE-521 consta na lista oficial da categoria.

**5. CVSS v3.1**
- **Vetor:** `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`
- **Score:** 7,4 · **Severidade:** Alta

| Métrica | Valor | Justificativa |
|---|---|---|
| AV | N | A senha fraca é explorada pelo login via rede |
| AC | H | Depende de condição fora do controle do atacante: um usuário ou administrador precisa ter escolhido uma senha fraca, o que a regra permite mas não obriga |
| PR | N | O atacante não precisa de conta |
| UI | N | Não é necessária interação da vítima no momento do ataque |
| S | U | O impacto fica dentro da aplicação |
| C | H | A regra se aplica também a contas `admin` criadas pela API, então o pior caso é leitura total |
| I | H | Idem, com modificação total |
| A | N | Nenhum efeito direto sobre disponibilidade |

O vetor é igual ao de VULN-005 porque ambos levam ao mesmo resultado (tomada de conta via adivinhação). As fraquezas, porém, são distintas e corrigidas de forma independente: uma é a política de senha, a outra é o controle de tentativas.

**6. CVE/NVD:** não aplicável (código próprio).

**7. MITRE ATT&CK**

| Tática | Técnica | Justificativa |
|---|---|---|
| Credential Access | T1110.001 — Brute Force: Password Guessing | Senhas curtas e sem verificação contra listas comuns ampliam a chance de acerto |
| Credential Access | T1110.003 — Brute Force: Password Spraying | Senhas comuns aceitas pela política são alvo típico de spraying |

**8. Pré-requisitos, impacto e limitações**
- **Pré-requisitos:** existência de conta cadastrada com senha fraca e acesso ao endpoint de login.
- **Impacto técnico:** tomada de contas operacionais ou administrativas.
- **Limitações de validação:**
  - A composição real das senhas cadastradas **não pode e não deve** ser verificada por análise estática. Se há contas com senhas fracas **necessita validação manual**, preferencialmente por auditoria de política no cadastro, sem quebra de hashes.
  - Os perfis efetivamente criados pela API em cada ambiente: **necessita validação manual**.

---

### VULN-007 — Atualização de pedido sem autorização por campo, sem regra de transição e sem limites para a nota

**1. Identificação e escopo afetado**
- **Componente:** backend, endpoint `PATCH /api/v1/orders/{order_id}` (`resources/order/controller.py`, `resources/order/schemas.py`, `resources/shared/repository.py`).
- **Perfis capazes de explorar:** `admin`, `attendant` e `kitchen`.
- **Dados afetados:** `status`, `rating` e `notes` de qualquer pedido.

**2. Evidência sanitizada**

| Arquivo | Linhas | Observação |
|---|---|---|
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/order/controller.py` | 414–432 | A autorização verifica só se o perfil pertence ao conjunto permitido, depois aplica o DTO inteiro |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/order/schemas.py` | 21–28 | `UpdateOrderDTO` com `status`, `rating` (inteiro sem faixa) e `notes` |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/shared/repository.py` | 37–40 | Atribuição direta dos campos, sem validação de negócio |
| `projeto_aplicado_foodtruck-main/migrations/versions/ca713c51cd3c_add_rating_to_order_table.py` | 24 | Coluna `rating` inteira, sem restrição `CHECK` |
| `projeto_aplicado_foodtruck-main/tests/test_api_order.py` | 354, 513 | Testes confirmam retorno a `PENDING` e atualização por perfil `kitchen` |
| `projeto_aplicado_foodtruck_frontend-main/public/chapeiro/preparar_pedidos.js` | 250–255 | As transições permitidas existem só no cliente |

**3. CWE**
- **Principal:** CWE-863 — Incorrect Authorization. Não há autorização por campo: qualquer perfil operacional altera `rating`, `notes` e `status`.
- **Secundária:** CWE-841 — Improper Enforcement of Behavioral Workflow. Não há máquina de estados no servidor.
- **Observação:** o aspecto "nota fora da faixa 1–5" corresponderia a CWE-20. Ele **necessita validação manual** e não foi usado como CWE do item.

**4. OWASP Top 10 2021:** A01:2021 – Broken Access Control. CWE-863 consta na lista oficial da categoria. CWE-841 consta em A04:2021.

**5. CVSS v3.1**
- **Vetor:** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N`
- **Score:** 4,3 · **Severidade:** Média

| Métrica | Valor | Justificativa |
|---|---|---|
| AV | N | Explorável pela API HTTP |
| AC | L | Uma requisição direta ao endpoint basta. Os testes confirmam o comportamento |
| PR | L | Exige conta autenticada, e o menor perfil suficiente é `kitchen` |
| UI | N | Nenhuma interação necessária |
| S | U | O impacto fica restrito aos dados de pedidos do backend |
| C | N | O endpoint não expõe dados adicionais |
| I | L | A modificação é limitada a três campos de pedidos. Não permite alterar usuários, produtos ou valores financeiros |
| A | N | Cancelar ou reabrir pedidos afeta o fluxo operacional, mas não a disponibilidade do componente. Fica registrado como impacto de negócio para a matriz de risco |

**6. CVE/NVD:** não aplicável (código próprio).

**7. MITRE ATT&CK**

| Tática | Técnica | Justificativa |
|---|---|---|
| Impact | T1565.001 — Data Manipulation: Stored Data Manipulation | Cenário realista de ameaça interna: alteração de status e avaliações persistidas para ocultar falhas operacionais ou manipular indicadores |

**8. Pré-requisitos, impacto e limitações**
- **Pré-requisitos:** conta autenticada com perfil `kitchen`, `attendant` ou `admin`.
- **Impacto técnico:** alteração indevida de estado e avaliação de pedidos, distorção de indicadores de satisfação e do ranking, e vetor de entrada para VULN-001 via `notes`.
- **Limitações de validação:**
  - Se valores de `rating` fora de 1–5 (ex.: zero ou negativos) são efetivamente persistidos **necessita validação manual**. A conclusão depende do comportamento do SQLModel em atualização de modelo de tabela.
  - Se existem regras de negócio formais definindo quais perfis alteram cada campo **necessita validação manual** com os responsáveis pelo produto. A classificação assume a separação de funções sugerida pela própria interface.

---

### VULN-008 — Paginação sem limites e divisão por zero

**1. Identificação e escopo afetado**
- **Componente:** backend, rotas de listagem `GET /api/v1/products/`, `GET /api/v1/orders/{id}/items`, `GET /api/v1/users/` e `GET /api/v1/orders/`.
- **Perfis capazes de explorar:** qualquer usuário autenticado (`/users/` exige `admin`).

**2. Evidência sanitizada**

| Arquivo | Linhas | Observação |
|---|---|---|
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/shared/schemas.py` | 27–28 | Cálculo de páginas com divisão inteira por `limit`, sem proteção contra zero |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/product/repository.py` | 29–32 | Listagem de produtos chama o cálculo de paginação acima |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/product/controller.py` | 98–150 | Parâmetros `offset`/`limit` sem faixa |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/order/controller.py` | 239–247 | Divisão por `limit` na listagem de itens de pedido |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/shared/repository.py` | 27–29 | `offset`/`limit` repassados à consulta sem validação |

**3. CWE**
- **Principal:** CWE-770 — Allocation of Resources Without Limits or Throttling (`limit` sem teto).
- **Secundária:** CWE-369 — Divide By Zero (`limit=0` gera exceção).

**4. OWASP Top 10 2021:** A04:2021 – Insecure Design, **por afinidade**. CWE-770 e CWE-369 não foram identificadas nas listas oficiais de CWEs mapeadas de 2021. A categoria foi escolhida porque o defeito é ausência de limite de recurso no desenho da API.

**5. CVSS v3.1**
- **Vetor:** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L`
- **Score:** 4,3 · **Severidade:** Média

| Métrica | Valor | Justificativa |
|---|---|---|
| AV | N | Explorável pela API HTTP |
| AC | L | Basta informar valores extremos nos parâmetros de consulta |
| PR | L | Exige conta autenticada de qualquer perfil nas rotas de produtos e pedidos |
| UI | N | Nenhuma interação necessária |
| S | U | O impacto fica restrito ao backend e ao banco da aplicação |
| C | N | Os registros retornados já são acessíveis ao mesmo usuário por paginação normal. Nenhuma exposição adicional |
| I | N | Nenhuma modificação de dados |
| A | L | Erros 500 repetíveis e consultas sem teto degradam o serviço. Negação total (A:H) não é demonstrável estaticamente |

**6. CVE/NVD:** não aplicável (código próprio).

**7. MITRE ATT&CK**

| Tática | Técnica | Justificativa |
|---|---|---|
| Impact | T1499.003 — Endpoint Denial of Service: Application Exhaustion Flood | Requisições repetidas com `limit` elevado, que força consultas e respostas volumosas, podem esgotar recursos da aplicação. A magnitude real **necessita validação manual** |

**8. Pré-requisitos, impacto e limitações**
- **Pré-requisitos:** conta autenticada e acesso à API.
- **Impacto técnico:** respostas 500 sob demanda e degradação de desempenho por consultas sem limite.
- **Limitações de validação:**
  - O volume de dados necessário para degradação perceptível e o comportamento sob carga: **necessita validação manual**, por teste de carga controlado em ambiente autorizado.
  - O efeito de `offset`/`limit` negativos no PostgreSQL implantado: **necessita validação manual**.
  - Existência de limites de tamanho de resposta ou timeouts na infraestrutura: **necessita validação manual**.

---

### VULN-009 — Token de acesso em `localStorage` e resposta de login registrada no console

**1. Identificação e escopo afetado**
- **Componente:** frontend, tela de login (`public/index.js`) e telas que leem o token armazenado.
- **Dados afetados:** token de acesso Bearer e dados do usuário devolvidos no login.
- **Contexto:** navegadores dos terminais de operação (atendente, chapeiro, administrador).

**2. Evidência sanitizada**

| Arquivo | Linhas | Observação |
|---|---|---|
| `projeto_aplicado_foodtruck_frontend-main/public/index.js` | 34 | A resposta completa da API de login é enviada ao console do navegador |
| `projeto_aplicado_foodtruck_frontend-main/public/index.js` | 37, 40 | Token de acesso e perfil gravados em `localStorage` |
| `projeto_aplicado_foodtruck_frontend-main/public/atendente/menu.js` | 431–436 | Perfil lido do `localStorage` só para exibir ou ocultar menu (a autorização efetiva é do backend) |
| `projeto_aplicado_foodtruck_frontend-main/public/` | — | O inventário registra 7 ocorrências de `console.log` no frontend |

**3. CWE**
- **Principal:** CWE-922 — Insecure Storage of Sensitive Information (token persistente em armazenamento legível por script).
- **Secundária:** CWE-215 — Insertion of Sensitive Information Into Debugging Code (`console.log` com o token).

**4. OWASP Top 10 2021:** A01:2021 – Broken Access Control. CWE-922 consta na lista oficial da categoria. CWE-215 não foi identificada nas listas oficiais de 2021.

**5. CVSS v3.1**
- **Vetor:** `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N`
- **Score:** 4,4 · **Severidade:** Média

| Métrica | Valor | Justificativa |
|---|---|---|
| AV | L | Cenário pontuado de forma isolada: leitura do token por quem tem acesso local ao navegador ou terminal (console, `localStorage`). O vetor remoto via script depende de VULN-001 e não entra no score base deste item |
| AC | L | O token fica em texto claro no armazenamento e no console, sem barreira adicional |
| PR | L | Exige acesso a uma sessão local do dispositivo (sistema operacional ou navegador) |
| UI | N | Não depende de ação da vítima no momento da leitura |
| S | U | O impacto fica dentro da aplicação |
| C | L | O token dá acesso aos dados permitidos ao perfil da vítima. Acesso total só ocorre se a vítima for `admin`, o que depende do contexto |
| I | L | O token permite ações dentro das permissões da vítima. Mesma ressalva |
| A | N | Nenhum efeito sobre disponibilidade |

**6. CVE/NVD:** não aplicável (código próprio).

**7. MITRE ATT&CK**

| Tática | Técnica | Justificativa |
|---|---|---|
| Credential Access | T1528 — Steal Application Access Token | Obtenção do token Bearer armazenado ou impresso no console do navegador |
| Defense Evasion / Lateral Movement | T1550.001 — Use Alternate Authentication Material: Application Access Token | Uso do token obtido para chamar a API sem conhecer a senha da vítima |

**8. Pré-requisitos, impacto e limitações**
- **Pré-requisitos:** acesso local ao navegador ou terminal onde houve login, ou execução de script na origem da aplicação (VULN-001).
- **Impacto técnico:** sequestro de sessão até o token expirar, com privilégios do usuário vítima.
- **Limitações de validação:**
  - Se os terminais de operação são compartilhados, e se há bloqueio de sessão do sistema operacional: **necessita validação manual**.
  - O tempo de expiração do token em cada ambiente: **necessita validação manual**. Ele define a janela de uso do token obtido.
  - Se o frontend implantado é um *build* diferente, sem `console.log`: **necessita validação manual**.

---

### VULN-010 — Exceções de banco não tratadas geram HTTP 500

**1. Identificação e escopo afetado**
- **Componente:** backend. Criação e atualização de usuários (`POST/PATCH /api/v1/users/`) e de pedidos (`POST/PATCH /api/v1/orders/`).
- **Camada comum:** `BaseRepository`, que relança exceções de banco.

**2. Evidência sanitizada**

| Arquivo | Linhas | Observação |
|---|---|---|
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/user/controller.py` | 331–332 | Criação de usuário sem verificar duplicidade nem tratar violação de unicidade |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/user/model.py` | 20–23 | `username`/`email` únicos, `username` limitado a 20 caracteres |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/user/schemas.py` | 22–27 | DTO sem limites de tamanho correspondentes às colunas |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/shared/repository.py` | 14–22 | Rollback e relançamento genérico da exceção |
| `projeto_aplicado_foodtruck-main/projeto_aplicado/resources/user/controller.py` | 263–272 | Documentação promete HTTP 409 para duplicidade |

**3. CWE**
- **Principal:** CWE-755 — Improper Handling of Exceptional Conditions.
- **Secundária:** CWE-20 — Improper Input Validation (tamanhos não validados antes de chegar ao banco).

**4. OWASP Top 10 2021:** A04:2021 – Insecure Design, **por afinidade**. CWE-755 não foi identificada nas listas oficiais de 2021. A categoria A05 (tratamento de erros que expõe detalhes) só se aplicaria se houvesse vazamento de *stack trace*, e isso não foi demonstrado.

**5. CVSS v3.1**
- **Vetor:** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:N`
- **Score:** 0,0 · **Severidade:** Nenhuma

| Métrica | Valor | Justificativa |
|---|---|---|
| AV | N | Acionável pela API HTTP |
| AC | L | Basta enviar dado duplicado ou acima do tamanho da coluna |
| PR | L | Exige conta autenticada, e o menor perfil suficiente (`attendant`) aciona o caminho em pedidos |
| UI | N | Nenhuma interação |
| S | U | Restrito ao backend |
| C | N | Com a configuração padrão do FastAPI, a resposta 500 é genérica. A diferença 500 vs. 201 na criação de usuários só é observável por `admin`, que já pode listar todos os usuários. Nenhum ganho de informação demonstrado |
| I | N | O repositório faz rollback, então nenhum dado inconsistente é persistido |
| A | N | A falha é por requisição, e nenhuma indisponibilidade do serviço é demonstrada |

**Interpretação:** o item continua confirmado como defeito, porque o código falha de modo não controlado. Seu impacto de segurança medido por CVSS, porém, é nulo com a evidência disponível. Recomenda-se tratá-lo como **fraqueza de robustez** na matriz de risco, com revisão do score caso a validação manual encontre exposição de detalhes de erro.

**6. CVE/NVD:** não aplicável (código próprio).

**7. MITRE ATT&CK:** não aplicável. Não há cenário realista de ataque com a evidência disponível.

**8. Pré-requisitos, impacto e limitações**
- **Pré-requisitos:** conta autenticada com permissão de criar ou atualizar usuários ou pedidos.
- **Impacto técnico:** respostas 500 inesperadas, contrato de API inconsistente (409 documentado e não implementado) e ruído em logs.
- **Limitações de validação:**
  - Se algum ambiente roda com modo de depuração ou recarga automática que exponha detalhes de exceção: **necessita validação manual**. Se houver exposição, C passaria a L e a CWE-209 deveria ser incluída.
  - O conteúdo registrado em logs de servidor nessas falhas, como valores de campos únicos: **necessita validação manual**.

---

## 4. Limitações gerais desta etapa

- A classificação usa exclusivamente a evidência registrada no inventário. Nenhum arquivo de código, configuração, `token.json` ou `.env` foi lido nesta etapa.
- Os scores CVSS são **base**. Exposição real, controles compensatórios e criticidade de negócio entram como métricas ambientais na matriz de risco.
- Os mapeamentos ATT&CK descrevem cenários plausíveis. Eles não afirmam que ataques ocorreram.
- Todos os itens marcados como "necessita validação manual" devem ser verificados em ambiente autorizado, conforme `docs/00-contexto/escopo.md`, antes de consolidar o relatório final.
