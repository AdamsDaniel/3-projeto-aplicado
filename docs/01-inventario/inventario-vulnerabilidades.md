# Inventário Preliminar de Vulnerabilidades — Sistema FoodTruck

| Item | Valor |
|---|---|
| Data da análise | 2026-09-14 |
| Tipo | Revisão de segurança autorizada, **somente análise estática** (leitura de código, configuração, lockfile e histórico git) |
| Escopo | `projeto_aplicado_foodtruck-main` (backend) e `projeto_aplicado_foodtruck_frontend-main` (frontend), conforme `docs/00-contexto/escopo.md` |
| Revisão analisada | commit `598e025` |
| Ações não realizadas | Nenhuma requisição a sistemas em execução, nenhum uso de credenciais, nenhuma alteração nos repositórios, nenhum teste contra o endereço público citado no código |
| Sanitização | Senhas, tokens, chaves, e-mails e endereços IP foram redigidos. Arquivos com segredos (`token.json`, `.env`) foram examinados apenas quanto à **estrutura, tamanho e comparação booleana**, sem registrar valores |

> **Status do documento:** preliminar. Severidades são qualitativas e devem ser recalculadas com CVSS na etapa `02-classificacao`. Os achados marcados como "validação manual" não devem ser tratados como vulnerabilidades até serem confirmados em ambiente autorizado.

---

## 1. Critérios usados

### 1.1 Classificação do achado

| Sigla | Classificação | Critério |
|---|---|---|
| **VC** | Vulnerabilidade confirmada | O caminho entrada → processamento → efeito é visível e completo no código-fonte, sem depender de como o sistema foi implantado |
| **RC** | Risco de configuração | O problema está em arquivos de infraestrutura, build ou padrões do framework. O impacto real depende de como e onde o sistema está implantado |
| **VM** | Exige validação manual | Existe um indício estático, mas confirmar o problema exige teste dinâmico, medição ou informação que o código não fornece |

### 1.2 Nível de confiança

| Nível | Significado |
|---|---|
| Alta | Evidência direta no código ou na configuração, sem ambiguidade |
| Média | Evidência forte, mas depende de comportamento de biblioteca, versão efetivamente implantada ou contexto de uso |
| Baixa | Hipótese plausível que precisa de teste para ser confirmada ou descartada |

### 1.3 Referências

- **OWASP Top 10:** edição 2021 (o mapeamento para edições posteriores pode ser feito na etapa de classificação).
- **CWE:** CWE "provável", ou seja, a entrada mais específica compatível com a evidência.
- **CVE/NVD:** citado **somente** quando a versão fixada no `uv.lock` ou na tag de imagem está dentro da faixa afetada. Todos os CVEs devem ser reconferidos no NVD antes do relatório final.

---

## 2. Resumo

| ID | Título | Componente | Classe | Sev. preliminar | Confiança | OWASP 2021 | CWE provável |
|---|---|---|---|---|---|---|---|
| VULN-001 | XSS armazenado via observações do pedido e dados de produto | Frontend (4 telas) + API | VC | Alta | Alta | A03 | CWE-79 |
| VULN-002 | Preço do item do pedido definido pelo cliente | Backend `/orders` | VC | Alta | Alta | A04 | CWE-602 |
| VULN-003 | Credencial padrão de administrador fixa no código e na documentação | Backend `create_admin.py`, `.env.template`, `docs/` | VC | Alta | Alta | A07 | CWE-798 / CWE-1392 |
| VULN-004 | Token JWT de administrador versionado no git (`token.json`) | Repositório (raiz) | VC | Média | Alta | A07 | CWE-540 |
| VULN-005 | Endpoint de login sem limite de tentativas | Backend `/token` | VC | Média | Alta | A07 | CWE-307 |
| VULN-006 | Política de senha fraca (mínimo de 6 caracteres) | Backend `/users` | VC | Média | Alta | A07 | CWE-521 |
| VULN-007 | Atualização de pedido sem regra de transição, sem controle por campo e sem limites para a nota | Backend `PATCH /orders/{id}` | VC | Média | Alta (nota: Média) | A01 / A04 | CWE-840 / CWE-863 / CWE-20 |
| VULN-008 | Paginação sem limites e divisão por zero | Backend `/products`, `/orders/{id}/items`, `/users`, `/orders` | VC | Média | Alta | A04 | CWE-369 / CWE-770 |
| VULN-009 | Token de acesso em `localStorage` e resposta de login registrada no console | Frontend | VC | Média | Alta | A02 / A09 | CWE-922 / CWE-532 |
| VULN-010 | Exceções de banco não tratadas geram HTTP 500 | Backend `/users`, `/orders` | VC | Baixa | Alta | A04 | CWE-755 |
| VULN-011 | Painel e API do Traefik sem autenticação, socket Docker montado e log DEBUG | `docker-compose.yaml` | RC | Alta* | Alta | A05 | CWE-306 / CWE-250 |
| VULN-012 | Postgres, Redis (sem senha) e backend publicados diretamente no host | `docker-compose.yaml` | RC | Alta* | Alta | A05 | CWE-668 / CWE-306 |
| VULN-013 | Tráfego sem TLS (HTTP puro) | Traefik, frontend `common.js` | RC | Média* | Alta | A02 | CWE-319 |
| VULN-014 | Build da imagem: execução como root, instalador remoto sem verificação, lockfile regenerado e dependências de desenvolvimento na imagem | `Dockerfile` | RC | Média | Alta | A08 | CWE-494 / CWE-250 / CWE-1357 |
| VULN-015 | Componentes com CVEs conhecidos ou sem manutenção | Redis 7.4.2, Starlette 0.46.2, passlib 1.7.4, imagens com tags flutuantes | RC / VM | Média–Alta* | Média | A06 | CWE-1395 / CWE-1104 |
| VULN-016 | CORS permissivo: qualquer origem é refletida com credenciais | Backend `app.py` | RC | Baixa | Alta | A05 | CWE-942 |
| VULN-017 | Documentação interativa da API exposta sem autenticação | Backend `app.py` | RC | Baixa | Alta | A05 | CWE-200 |
| VULN-018 | Nenhuma CSP ou cabeçalho de segurança no frontend | Frontend e nginx | RC | Média | Alta | A05 | CWE-693 / CWE-1021 |
| VULN-019 | Tokens JWT sem revogação e sem `iss`/`aud`; algoritmo definido por variável de ambiente | Backend `auth/security.py` | VM | Baixa–Média | Média | A07 | CWE-613 |
| VULN-020 | Possível enumeração de usuários pelo tempo de resposta do login | Backend `auth/token.py` | VM | Baixa | Baixa | A07 | CWE-208 |
| VULN-021 | Localizador de pedido previsível e sem unicidade | Backend `utils.py`, `order/model.py` | VM | Baixa | Média | A04 | CWE-330 / CWE-338 |

\* A severidade depende da exposição real do ambiente, que não pode ser determinada por análise estática.

**Distribuição:** 10 VC · 8 RC · 3 VM (VULN-015 combina RC e VM).

---

## 3. Vulnerabilidades confirmadas (VC)

### VULN-001 — XSS armazenado via observações do pedido e dados de produto

- **Componente afetado:** frontend `public/atendente/acompanhar_pedidos.js`, `public/chapeiro/preparar_pedidos.js`, `public/atendente/menu.js`, `public/admin/gerenciar_produtos.js`, `public/atendente/registrar_avaliacao.js`. A origem dos dados é a API (`notes` de pedido; `name` e `description` de produto).
- **Classificação:** VC · **Confiança:** Alta
- **Descrição técnica:** campos de texto livre aceitos pela API sem sanitização (`CreateOrderDTO.notes`, `UpdateOrderDTO.notes`, `CreateProductDTO.name/description`) são inseridos no DOM por interpolação em template literal atribuída a `innerHTML`, sem escape. Nenhuma página define Content-Security-Policy (ver VULN-018). Um atendente, ou qualquer perfil que possa usar `PATCH /orders` (incluindo `kitchen`, ver VULN-007), consegue gravar HTML/JS que será executado no navegador de outros operadores, inclusive administradores que acessam as telas de atendente ou chapeiro.
- **Evidência (estática, sanitizada):**
  - `projeto_aplicado_foodtruck_frontend-main/public/atendente/acompanhar_pedidos.js:269-276`: `cartaoPedido.innerHTML = \` … <p class="order-notes">Observações: ${notes || 'N/A'}</p> …\``
  - `projeto_aplicado_foodtruck_frontend-main/public/chapeiro/preparar_pedidos.js:269-277`: mesmo padrão com `${notes}`
  - `projeto_aplicado_foodtruck_frontend-main/public/atendente/menu.js:192-197`: `productCard.innerHTML = \` … <h3>${product.name}</h3> … ${product.description || …}\``, além de `menu.js:122-123` (`${item.name}`)
  - `projeto_aplicado_foodtruck_frontend-main/public/admin/gerenciar_produtos.js:170-175`: `${item.name}` e `${item.description}` em `innerHTML`
  - `acompanhar_pedidos.js:119-122` e `registrar_avaliacao.js:151-152`: nome de produto vindo do cache e interpolado em HTML
  - Backend: `projeto_aplicado/resources/order/schemas.py:28,37` (`notes: Optional[str]`, sem restrição de conteúdo)
  - Busca reproduzível: `grep -rnE 'innerHTML' projeto_aplicado_foodtruck_frontend-main/public`
  - **Confirmação dinâmica sugerida (ambiente autorizado, sem script):** criar um pedido com observação `<i>poc-html</i>` e verificar se o texto aparece em itálico na tela do chapeiro. Isso prova injeção de HTML sem executar JavaScript.
- **Pré-requisito de exploração:** usuário autenticado com perfil `attendant` ou `kitchen` (para `notes`) ou `admin` (para produtos).
- **Impacto técnico:** execução de JavaScript arbitrário na sessão de outro operador. Combinado com VULN-009, permite roubar o token Bearer do `localStorage`, inclusive de administrador, e executar ações em nome da vítima (criar usuários, alterar preços, cancelar pedidos).
- **OWASP:** A03:2021 – Injection · **CWE:** CWE-79 · **CVE:** não aplicável (código próprio)
- **Recomendação inicial:** substituir `innerHTML` por `textContent` ou `createElement` para dados dinâmicos, ou aplicar escape de HTML centralizado. Opcionalmente usar sanitizador (ex.: DOMPurify) onde HTML for necessário. Adicionar CSP restritiva (`script-src 'self'`). No backend, validar tamanho e conjunto de caracteres de `notes`, `name` e `description`.

### VULN-002 — Preço do item do pedido definido pelo cliente

- **Componente afetado:** backend `projeto_aplicado/resources/order/` (`POST /api/v1/orders/`)
- **Classificação:** VC · **Confiança:** Alta
- **Descrição técnica:** o DTO de criação de item de pedido recebe `price` do cliente. O controlador busca o produto só para verificar se ele existe e **não usa `product.price`**. O total do pedido é calculado com o preço enviado pelo cliente. A própria suíte de testes confirma o comportamento: um pedido criado com `price: 0.01` é aceito e o total fica igual a `0.01`.
- **Evidência (estática, sanitizada):**
  - `projeto_aplicado/resources/order/schemas.py:11-18`: `class CreateOrderItemDTO: quantity; product_id; price: float = Field(gt=0.0)`
  - `projeto_aplicado/resources/order/controller.py:381-395`: `product = product_repository.get_by_id(item.product_id)` → `order_item = OrderItem.create(item)` → `new_order.total = sum(item.calculate_total() …)`
  - `projeto_aplicado/resources/order/model.py:54-55`: `return self.quantity * self.price`
  - `tests/test_api_order.py:328-350` (`test_order_total_with_small_price`): envia `price: 0.01` e espera `expected_total = 0.01`
  - Frontend: `public/atendente/menu.js:338-339` envia `price: item.price` a partir do carrinho do navegador
- **Pré-requisito de exploração:** usuário autenticado com perfil `attendant` ou `admin`.
- **Impacto técnico:** perda de integridade de dados financeiros. Pedidos podem ser registrados com qualquer valor positivo (ex.: R$ 0,01), o que afeta faturamento, relatórios e o ranking de vendas.
- **OWASP:** A04:2021 – Insecure Design · **CWE:** CWE-602 (Client-Side Enforcement of Server-Side Security); relacionado: CWE-472 · **CVE:** não aplicável
- **Recomendação inicial:** remover `price` de `CreateOrderItemDTO` e gravar `OrderItem.price = product.price` no servidor. Ajustar os testes que hoje aceitam o comportamento inseguro.

### VULN-003 — Credencial padrão de administrador fixa no código e na documentação

- **Componente afetado:** backend `create_admin.py`, `.env.template`, `docs/API.md`, `docs/INSTALL.md`, `docs/CLI*.md`, `docs/pt-br/*.md`
- **Classificação:** VC · **Confiança:** Alta
- **Descrição técnica:** o script de inicialização cria o usuário `admin` com **senha fixa no código-fonte**, sem ler variável de ambiente. A mesma senha curta aparece como valor padrão em `.env.template` e em exemplos de 9 arquivos de documentação. A variável `DEFAULT_ADMIN_PASSWORD` do `.env` **não é usada** por nenhum código (`settings.py` usa `extra='ignore'`), então quem trocar a senha no `.env` pode achar que está protegido sem estar. Uma comparação booleana no `.env` local (não versionado), sem registrar o valor, mostrou que ele também mantém o padrão do template.
- **Evidência (estática, sanitizada):**
  - `create_admin.py:13-19`: `User(username="admin", email="<redigido>", password=get_password_hash("<SENHA-PADRÃO-REDIGIDA>"), role=UserRole.ADMIN)`
  - `.env.template:14-16`: `DEFAULT_ADMIN_PASSWORD=<SENHA-PADRÃO-REDIGIDA>`
  - `grep -rn "DEFAULT_ADMIN" projeto_aplicado/` → nenhuma ocorrência (variável não utilizada)
  - Busca reproduzível, que lista apenas nomes de arquivo: `grep -rl "<valor do template>" docs/ README.md` → 9 arquivos
- **Pré-requisito de exploração:** acesso de rede ao endpoint `/api/v1/token/`, sem autenticação.
- **Impacto técnico:** controle administrativo total da API (gestão de usuários, produtos e pedidos) em qualquer instalação que tenha usado o script ou a documentação sem trocar a senha. Não há limite de tentativas (VULN-005).
- **OWASP:** A07:2021 – Identification and Authentication Failures · **CWE:** CWE-798, CWE-1392 · **CVE:** não aplicável
- **Recomendação inicial:** exigir a senha inicial por variável de ambiente obrigatória (falhar se ausente ou igual ao padrão), ou gerar senha aleatória exibida uma única vez. Forçar troca no primeiro login. Remover a senha dos exemplos da documentação. Validar em cada ambiente se a conta `admin` ainda usa a senha padrão.

### VULN-004 — Token JWT de administrador versionado no git (`token.json`)

- **Componente afetado:** raiz do repositório (`token.json`)
- **Classificação:** VC · **Confiança:** Alta
- **Descrição técnica:** o arquivo `token.json`, com a resposta completa de login de um usuário **administrador** (access token JWT, id, username, e-mail e perfil), foi adicionado ao git no commit `598e025`. Não existe `.gitignore` na raiz, e isso contraria o próprio escopo ("token.json não será versionado"). A análise estrutural, sem registrar valores, mostrou: algoritmo `HS256`, claims `sub` e `exp`, expiração em 2026-05-16 01:04 UTC (já expirado) e perfil `admin`.
- **Evidência (estática, sanitizada):**
  - `git log --oneline -- token.json` → `598e025 feat: add category selection dropdowns …`
  - `git check-ignore -v token.json` → sem regra (não ignorado)
  - Inspeção só de chaves: `python3 -c "import json;print(list(json.load(open('token.json')).keys()))"` → `access_token, token_type, user`
- **Pré-requisito de exploração:** acesso de leitura ao repositório ou a qualquer clone ou fork.
- **Impacto técnico:** (1) exposição de dados pessoais e identificadores da conta administrativa (LGPD). (2) Um JWT HS256 válido é um par mensagem/assinatura conhecido, o que permite **ataque offline de força bruta contra `JWT_SECRET_KEY`**. Se o segredo tiver baixa entropia, um atacante pode forjar tokens de qualquer usuário. (3) Enquanto estava válido, o token dava acesso administrativo direto. O arquivo continua no histórico mesmo que seja apagado.
- **OWASP:** A07:2021 (e A05:2021) · **CWE:** CWE-540 (Inclusion of Sensitive Information in Source Code); relacionado: CWE-312 · **CVE:** não aplicável
- **Recomendação inicial:** remover o arquivo e reescrever o histórico (`git filter-repo`) se o repositório for compartilhado. **Rotacionar `JWT_SECRET_KEY`** por precaução, com valor aleatório de 256 bits ou mais. Adicionar `.gitignore` na raiz e um scanner de segredos no pre-commit ou na CI (ex.: gitleaks).

### VULN-005 — Endpoint de login sem limite de tentativas

- **Componente afetado:** backend `projeto_aplicado/auth/token.py` (`POST /api/v1/token/`)
- **Classificação:** VC · **Confiança:** Alta para a camada de aplicação; é preciso validar se existe WAF ou proxy à frente em produção
- **Descrição técnica:** a documentação da rota promete HTTP 429 ("Too many login attempts"), mas não há limitador na aplicação (nenhuma dependência como slowapi, nenhum middleware) nem no proxy (não há middleware `ratelimit` nos labels Traefik do `docker-compose.yaml`). Também não há bloqueio de conta nem atraso progressivo.
- **Evidência (estática, sanitizada):**
  - `projeto_aplicado/auth/token.py:81-96`: resposta 429 apenas documentada no OpenAPI; `token.py:152-186` não contém lógica de limitação
  - `docs/pt-br/API.md:722`: documenta 429 "Limite de taxa excedido"
  - `grep -rniE 'slowapi|limiter|rate.?limit' projeto_aplicado/` → sem ocorrências
  - `docker-compose.yaml:24-27`: labels Traefik sem middleware
- **Pré-requisito de exploração:** acesso de rede ao endpoint, sem autenticação.
- **Impacto técnico:** força bruta e *credential stuffing* sem restrição, potencializados por VULN-003 e VULN-006. Consumo de CPU por hashing Argon2 em massa (DoS).
- **OWASP:** A07:2021 · **CWE:** CWE-307 · **CVE:** não aplicável
- **Recomendação inicial:** limitar tentativas por IP e por username (na aplicação ou no middleware `ratelimit` do Traefik), com bloqueio temporário e registro das tentativas falhas. Alinhar a documentação ao comportamento real.

### VULN-006 — Política de senha fraca (mínimo de 6 caracteres)

- **Componente afetado:** backend `projeto_aplicado/resources/user/schemas.py`
- **Classificação:** VC · **Confiança:** Alta
- **Descrição técnica:** a única regra de senha é `min_length=6`, na criação e na atualização. Não há verificação contra senhas comuns ou vazadas. A documentação da rota menciona "Password is too weak", mas essa regra não existe.
- **Evidência:** `user/schemas.py:25` (`password: str = Field(min_length=6)`) e `user/schemas.py:33`; `user/controller.py:235-238` (exemplo "weak_password" apenas documental)
- **Pré-requisito de exploração:** depende de um administrador cadastrar senhas fracas. A exploração em si ocorre sem autenticação, via VULN-005.
- **Impacto técnico:** contas de operadores vulneráveis a adivinhação e força bruta.
- **OWASP:** A07:2021 · **CWE:** CWE-521 · **CVE:** não aplicável
- **Recomendação inicial:** mínimo de 12 caracteres, lista de senhas comuns ou vazadas (NIST SP 800-63B) e mensagem de erro coerente com a regra.

### VULN-007 — Atualização de pedido sem regra de transição, sem controle por campo e sem limites para a nota

- **Componente afetado:** backend `PATCH /api/v1/orders/{order_id}` (`order/controller.py`, `order/schemas.py`, `shared/repository.py`)
- **Classificação:** VC (transição e controle por campo) · VM (persistência de nota fora da faixa) · **Confiança:** Alta / Média
- **Descrição técnica:**
  1. Os perfis `admin`, `attendant` e `kitchen` podem alterar **qualquer** campo de `UpdateOrderDTO` (`status`, `rating`, `notes`) em **qualquer** pedido. Assim, o chapeiro pode alterar avaliações e observações, e o atendente pode concluir pedidos.
  2. Não há máquina de estados no servidor. As transições permitidas (ex.: `COMPLETED` não volta para `PENDING`) existem **apenas no JavaScript do frontend**, e os testes confirmam transições livres.
  3. `rating` é `Optional[int]` sem `ge/le` no DTO. As restrições `ge=1, le=5` existem só no modelo `table=True`, que o SQLModel não valida na atribuição via `setattr`, e a coluna no banco não tem `CHECK` (migration `ca713c51cd3c`). É provável que valores como `0`, `-5` ou `999` sejam gravados (**validar**).
- **Evidência (estática, sanitizada):**
  - `order/controller.py:414-432`: verifica só o perfil e chama `repository.update(existing_order, dto)`
  - `order/schemas.py:21-28`: `status`, `rating: Optional[int] = None`, `notes: Optional[str] = None`
  - `shared/repository.py:37-40`: `setattr(entity, key, value)` sem validação
  - `migrations/versions/ca713c51cd3c_add_rating_to_order_table.py:24`: `sa.Column('rating', sa.Integer(), nullable=True)` sem constraint
  - `tests/test_api_order.py:354` (`test_order_status_transition_to_pending`) e `:513` (`test_kitchen_can_update_order`)
  - Frontend: `public/chapeiro/preparar_pedidos.js:250-255` (`transicoesStatus`, controle apenas no cliente)
- **Pré-requisito de exploração:** qualquer usuário autenticado da operação.
- **Impacto técnico:** fraude ou erro operacional (reabrir pedidos concluídos, cancelar pedidos pagos), manipulação de indicadores de satisfação e do ranking, e vetor adicional para VULN-001 pelo campo `notes`.
- **OWASP:** A01:2021 – Broken Access Control / A04:2021 – Insecure Design · **CWE:** CWE-840, CWE-863, CWE-20 · **CVE:** não aplicável
- **Recomendação inicial:** implementar máquina de estados no servidor. Separar endpoints ou DTOs por perfil (ex.: cozinha altera só `status` dentro das transições permitidas; atendente registra `rating` só em pedido `COMPLETED`). Adicionar `Field(ge=1, le=5)` e `max_length=255` ao DTO e `CHECK` no banco.

### VULN-008 — Paginação sem limites e divisão por zero

- **Componente afetado:** backend `GET /products/`, `GET /orders/{id}/items`, `GET /users/`, `GET /orders/`
- **Classificação:** VC · **Confiança:** Alta
- **Descrição técnica:** `offset` e `limit` são inteiros sem validação de faixa.
  - `limit=0` em `/products/` gera `ZeroDivisionError` em `Pagination.create` (HTTP 500).
  - `limit=0` em `/orders/{id}/items` gera `offset // limit` (HTTP 500).
  - Valores negativos seguem para `OFFSET/LIMIT` do SQL e provocam erro no PostgreSQL.
  - `limit` muito grande devolve a tabela inteira em uma única resposta.
- **Evidência (estática, sanitizada):**
  - `resources/shared/schemas.py:27-28`: `(total_count + limit - 1) // limit` e `offset // limit + 1`
  - `resources/product/repository.py:29-32` → `Pagination.create(offset, limit, total_count)`; `product/controller.py:98-150`
  - `resources/order/controller.py:239-247`: `page=offset // limit + 1`
  - `resources/shared/repository.py:27-29`: `.offset(offset).limit(limit)` sem validação
- **Pré-requisito de exploração:** usuário autenticado com qualquer perfil.
- **Impacto técnico:** erros 500 repetíveis, consumo excessivo de memória, CPU e banco com consultas sem limite (DoS de aplicação) e extração em massa de dados em uma chamada.
- **OWASP:** A04:2021 · **CWE:** CWE-369, CWE-770 · **CVE:** não aplicável
- **Recomendação inicial:** `offset: int = Query(0, ge=0)` e `limit: int = Query(100, ge=1, le=100)` em todas as rotas de listagem, com a validação centralizada numa dependência comum.

### VULN-009 — Token de acesso em `localStorage` e resposta de login registrada no console

- **Componente afetado:** frontend `public/index.js`, páginas que leem `accessToken`
- **Classificação:** VC · **Confiança:** Alta
- **Descrição técnica:** o JWT é salvo em `localStorage`, onde qualquer script da origem consegue lê-lo. A resposta completa do login, **incluindo `access_token` e o e-mail do usuário**, é impressa com `console.log`, e há outros `console.log` com dados de pedidos e produtos. O perfil (`userRole`) também fica no `localStorage` e só controla a exibição de menus. A autorização efetiva está no backend, o que foi verificado.
- **Evidência (estática, sanitizada):**
  - `public/index.js:34`: `console.log('Resposta da API:', data);`
  - `public/index.js:37,40`: `localStorage.setItem('accessToken', data.access_token)` / `localStorage.setItem('userRole', …)`
  - `public/atendente/menu.js:431-436`: ocultação de menu admin baseada em `localStorage`
  - `grep -rn "console.log" public` → 7 ocorrências
- **Pré-requisito de exploração:** XSS (VULN-001), extensão maliciosa ou acesso ao dispositivo ou console compartilhado (terminal de atendimento).
- **Impacto técnico:** sequestro de sessão por roubo de token. O token permanece válido até expirar, sem possibilidade de revogação (VULN-019).
- **OWASP:** A02:2021 / A09:2021 · **CWE:** CWE-922, CWE-532 · **CVE:** não aplicável
- **Recomendação inicial:** remover `console.log` de produção. Avaliar cookie `HttpOnly; Secure; SameSite=Strict` com proteção CSRF ou, no mínimo, `sessionStorage` com token de vida curta. Priorizar a correção de VULN-001, que é o vetor principal.

### VULN-010 — Exceções de banco não tratadas geram HTTP 500

- **Componente afetado:** backend `POST/PATCH /users`, `POST/PATCH /orders`
- **Classificação:** VC · **Confiança:** Alta
- **Descrição técnica:** `username` e `email` são únicos no banco, mas `create_user` não verifica duplicidade nem trata `IntegrityError` (a documentação promete 409). Os DTOs não impõem os tamanhos das colunas (`username` VARCHAR(20), `notes` VARCHAR(255)). No PostgreSQL, valores maiores geram `DataError`. `BaseRepository` faz rollback e relança a exceção, que resulta em HTTP 500.
- **Evidência (estática, sanitizada):**
  - `user/controller.py:331-332`: `user = User(**dto.model_dump()); repository.create(user)`
  - `user/model.py:20-23` (`unique=True`, `max_length=20`); `user/schemas.py:22-27` (sem `max_length`)
  - `shared/repository.py:14-22`: `except Exception as e: rollback(); raise e`
  - `user/controller.py:263-272`: documenta 409 "Email already registered"
- **Pré-requisito de exploração:** usuário autenticado (admin para `/users`, operação para `/orders`).
- **Impacto técnico:** erros não controlados, ruído em logs, respostas inconsistentes e enumeração de usernames ou e-mails existentes pelo padrão 500 vs. 201. Com as configurações padrão do FastAPI não há vazamento de *stack trace*. **Validar** se `--reload` ou modo debug é usado em algum ambiente.
- **OWASP:** A04:2021 · **CWE:** CWE-755; relacionado: CWE-209 (se houver debug) · **CVE:** não aplicável
- **Recomendação inicial:** validar tamanhos nos DTOs, verificar duplicidade antes de inserir, tratar `IntegrityError` com 409 e registrar handler global de exceções com mensagem genérica e log estruturado.

---

## 4. Riscos de configuração (RC)

### VULN-011 — Painel e API do Traefik sem autenticação, socket Docker montado e log DEBUG

- **Componente afetado:** `projeto_aplicado_foodtruck-main/docker-compose.yaml` (serviço `traefik`)
- **Classificação:** RC · **Confiança:** Alta
- **Descrição técnica:** `--api.insecure=true` expõe o dashboard e a API do Traefik na porta 8080, **publicada em todas as interfaces do host**, sem autenticação. O socket Docker está montado no contêiner. A flag `:ro` não restringe chamadas à API Docker, só a escrita no arquivo do socket. Isso significa que um comprometimento do Traefik equivale a controle do host. `--log.level=DEBUG` aumenta o volume de dados sensíveis em log.
- **Evidência:** `docker-compose.yaml:5-15`: `--log.level=DEBUG`, `--api.insecure=true`, `ports: "8080:8080"`, `/var/run/docker.sock:/var/run/docker.sock:ro`
- **Pré-requisito de exploração:** acesso de rede à porta 8080 do host.
- **Impacto técnico:** divulgação da topologia (rotas, serviços, backends) e superfície para escalar a controle do host via Docker API.
- **OWASP:** A05:2021 – Security Misconfiguration · **CWE:** CWE-306, CWE-250 · **CVE:** não citado (ver VULN-015 para varredura da imagem `traefik:v3.4.1`)
- **Recomendação inicial:** desativar `api.insecure`. Se o dashboard for necessário, protegê-lo com router autenticado (basicAuth/forwardAuth) e restringi-lo a `127.0.0.1`. Usar log `INFO`/`WARN`. Considerar *docker socket proxy* com permissões mínimas.

### VULN-012 — Postgres, Redis (sem senha) e backend publicados diretamente no host

- **Componente afetado:** `docker-compose.yaml` (serviços `postgres`, `redis`, `backend`), `projeto_aplicado/ext/cache/redis.py`
- **Classificação:** RC · **Confiança:** Alta
- **Descrição técnica:**
  - `5432:5432` e `6379:6379` publicam banco e cache em todas as interfaces do host.
  - O Redis sobe sem `requirepass`/ACL e o cliente Python conecta sem senha. O módulo de cache **não é importado por nenhum código**, então o Redis é superfície de ataque sem uso funcional.
  - O backend publica `8000:8000`, o que permite contornar o Traefik e qualquer controle futuro aplicado nele (rate limit, TLS, cabeçalhos).
  - O healthcheck do Postgres assume o usuário `postgres`. No `.env` local (não versionado), a verificação booleana indicou usuário de banco padrão e senha curta (menos de 12 caracteres). Valores não registrados.
- **Evidência:** `docker-compose.yaml:28-29`, `:57-58`, `:62`, `:71-74`; `ext/cache/redis.py:10-14` (`Redis(host=…, port=…, decode_responses=True)`, sem senha); `grep -rn "ext.cache" projeto_aplicado/` → nenhuma ocorrência
- **Pré-requisito de exploração:** acesso de rede ao host nas portas 5432, 6379 ou 8000.
- **Impacto técnico:** acesso não autenticado ao Redis (leitura e escrita, `CONFIG`, execução de Lua, ver CVEs em VULN-015). Força bruta direta contra o PostgreSQL. Uso da API sem passar pelo proxy.
- **OWASP:** A05:2021 · **CWE:** CWE-668, CWE-306 · **CVE:** ver VULN-015
- **Recomendação inicial:** remover `ports` de `postgres` e `redis`, ou vinculá-los a `127.0.0.1`. Remover a publicação de `8000` e acessar só via proxy. Habilitar senha/ACL no Redis ou remover o serviço enquanto não for usado. Usar usuário de banco dedicado com senha forte.

### VULN-013 — Tráfego sem TLS (HTTP puro)

- **Componente afetado:** Traefik (`docker-compose.yaml`), frontend `assets/js/common.js`
- **Classificação:** RC · **Confiança:** Alta (configuração) / validar em produção
- **Descrição técnica:** o único entrypoint do Traefik é `:80`, sem `websecure`, certificados ou redirecionamento HTTPS. O frontend aponta para `http://localhost:8000`, e há uma URL alternativa comentada com **endereço IPv4 público em HTTP**. Isso indica que ao menos um ambiente pode ter sido servido sem TLS. Esse endereço **não foi testado**.
- **Evidência:** `docker-compose.yaml:10` (`--entryPoints.web.address=:80`); `assets/js/common.js:7` (`http://localhost:8000`); `assets/js/common.js:8` (`//const API_BASE_URL = 'http://<IPv4-PÚBLICO-REDIGIDO>/';`)
- **Pré-requisito de exploração:** posição de rede entre cliente e servidor (Wi-Fi do food truck, rede compartilhada).
- **Impacto técnico:** interceptação de credenciais de login e tokens Bearer em trânsito.
- **OWASP:** A02:2021 – Cryptographic Failures · **CWE:** CWE-319 · **CVE:** não aplicável
- **Recomendação inicial:** configurar entrypoint HTTPS com certificado (ACME/Let's Encrypt), redirecionar HTTP para HTTPS, enviar HSTS e parametrizar `API_BASE_URL` por ambiente. Remover o IP do código-fonte.

### VULN-014 — Build da imagem: root, instalador remoto sem verificação, lockfile regenerado e dependências de desenvolvimento

- **Componente afetado:** `projeto_aplicado_foodtruck-main/Dockerfile`
- **Classificação:** RC · **Confiança:** Alta
- **Descrição técnica:**
  - O instalador do `uv` é baixado de URL remota sem versão fixa nem checksum e executado com `sh`.
  - `uv lock` durante o build **regenera o lockfile**, então as versões implantadas podem diferir do `uv.lock` revisado.
  - `uv sync` sem `--no-dev` instala o grupo `dev` (pytest, ruff, taskipy, ignr) na imagem final.
  - Não há instrução `USER`, então o processo roda como root.
  - A imagem base usa tag flutuante (`python:3.13-slim-bookworm`).
  - O `HEALTHCHECK` depende de `/docs`, o que dificulta desativar a documentação (VULN-017).
- **Evidência:** `Dockerfile:1`, `:7-9` (`ADD https://astral.sh/uv/install.sh` + `sh`), `:19-21` (`uv lock && uv sync`), `:41-42`, `:44-46` (sem `USER`)
- **Pré-requisito de exploração:** comprometimento da cadeia de fornecimento (fonte do instalador ou de pacotes) ou exploração de outra falha no contêiner.
- **Impacto técnico:** execução de código não verificado no build, divergência entre versões auditadas e implantadas, e privilégios maiores em caso de RCE.
- **OWASP:** A08:2021 – Software and Data Integrity Failures · **CWE:** CWE-494, CWE-250, CWE-1357 · **CVE:** não aplicável
- **Recomendação inicial:** usar imagem oficial `ghcr.io/astral-sh/uv:<versão>` fixada por digest, `uv sync --frozen --no-dev`, usuário não-root (`USER app`), fixar imagens por digest e trocar o healthcheck por um endpoint `/health` dedicado.

### VULN-015 — Componentes com CVEs conhecidos ou sem manutenção

- **Componente afetado:** imagem `redis:7.4.2`; `starlette 0.46.2` (via FastAPI 0.115.12); `passlib 1.7.4`; imagens `postgres:16`, `nginx:alpine`, `traefik:v3.4.1`
- **Classificação:** RC (Redis, passlib, tags flutuantes) / VM (alcance do CVE do Starlette) · **Confiança:** Média (baseada em versão; reconferir no NVD)
- **Descrição técnica e CVEs aplicáveis:**

| Componente (fonte da versão) | CVE | Resumo | Versão corrigida | Aplicabilidade neste sistema |
|---|---|---|---|---|
| Redis 7.4.2 (`docker-compose.yaml:71`) | CVE-2025-21605 | Cliente **não autenticado** provoca crescimento ilimitado de buffer de saída (DoS) | 7.4.3 | Aplicável: porta publicada e sem autenticação (VULN-012) |
| Redis 7.4.2 | CVE-2025-49844 | *Use-after-free* no interpretador Lua, com possível execução remota de código por usuário autenticado | 7.4.6 | Aplicável: sem senha, qualquer cliente é "autenticado" como usuário padrão |
| Starlette 0.46.2 (`uv.lock`) | CVE-2025-54121 | O parser multipart bloqueia a *event loop* ao transferir arquivos grandes para disco | 0.47.2 | **VM**: a app não recebe upload, mas `/token` faz parse de formulário (`OAuth2PasswordRequestForm`). Validar se um multipart com parte de arquivo grande alcança o caminho vulnerável |

  - `passlib 1.7.4` está sem manutenção ativa. Hoje funciona com Argon2, mas há incompatibilidades conhecidas com versões recentes de dependências. `pwdlib` já está declarado e não é usado.
  - `postgres:16`, `nginx:alpine` e `traefik:v3.4.1`: com tags flutuantes ou sem varredura de imagem, não é possível afirmar CVEs estaticamente. Isso **exige varredura** (Trivy ou Grype).
  - **Verificados e não aplicáveis ao runtime**, para não gerar falsos positivos: `h11 0.16.0` (já corrige CVE-2025-43859), `jinja2 3.1.6` (já corrige CVE-2025-27516), `python-multipart 0.0.20` (já corrige CVE-2024-53981), `pyjwt 2.10.1` (já corrige CVE-2024-53861). `requests 2.32.3` (CVE-2024-47081) e `urllib3 2.4.0` (CVE-2025-50181) aparecem **apenas no grupo `test`** (via testcontainers), que não é instalado pelo `Dockerfile`.
- **Evidência:** `docker-compose.yaml:4,42,54,71`; `uv.lock` (versões extraídas via `tomllib`); análise de alcançabilidade das dependências feita a partir do grafo do `uv.lock`
- **Ressalva:** como o `Dockerfile` executa `uv lock` (VULN-014), as versões **efetivamente implantadas** podem diferir do `uv.lock`. É preciso validar na imagem construída.
- **Pré-requisito de exploração:** Redis: acesso de rede à porta 6379. Starlette: acesso de rede a `/token`.
- **Impacto técnico:** DoS do cache ou da API e possível RCE no contêiner Redis.
- **OWASP:** A06:2021 – Vulnerable and Outdated Components · **CWE:** CWE-1395, CWE-1104
- **Recomendação inicial:** atualizar Redis para 7.4.6 ou superior (ou remover o serviço). Atualizar FastAPI/Starlette para versões com Starlette 0.47.2 ou superior. Migrar hashing para `pwdlib`. Fixar imagens por digest. Incluir `pip-audit`/`uv` audit e Trivy na CI.

### VULN-016 — CORS permissivo: qualquer origem é refletida com credenciais

- **Componente afetado:** backend `projeto_aplicado/app.py`
- **Classificação:** RC · **Confiança:** Alta
- **Descrição técnica:** `allow_origins=['*']` com `allow_credentials=True`. A leitura do código do Starlette 0.46.2 instalado confirma que o *preflight* reflete a origem solicitada (`preflight_explicit_allow_origin = not allow_all_origins or allow_credentials`) e que requisições simples com cookie também refletem a origem. O impacto atual é **limitado** porque a autenticação usa header `Authorization: Bearer`, que um site de terceiros não consegue anexar sem possuir o token. O risco aumenta se a autenticação migrar para cookies.
- **Evidência:** `app.py:60-66`; `starlette/middleware/cors.py:36,113,159-160` (versão 0.46.2)
- **Pré-requisito de exploração:** vítima autenticada visitando site malicioso. Só é relevante com autenticação por cookie ou recurso que não exija autenticação.
- **Impacto técnico:** hoje baixo. Seria alto (leitura cross-origin de dados autenticados) com sessão por cookie.
- **OWASP:** A05:2021 · **CWE:** CWE-942 · **CVE:** não aplicável
- **Recomendação inicial:** lista explícita de origens por ambiente (ex.: domínio do frontend), `allow_credentials=False` enquanto a autenticação for por header, e métodos e cabeçalhos mínimos.

### VULN-017 — Documentação interativa da API exposta sem autenticação

- **Componente afetado:** backend `projeto_aplicado/app.py`
- **Classificação:** RC · **Confiança:** Alta
- **Descrição técnica:** `FastAPI()` é instanciado sem `docs_url`, `redoc_url` ou `openapi_url`, então `/docs`, `/redoc` e `/openapi.json` ficam públicos. A flag `API_DEBUG` existe em `settings.py`, mas não é usada para controlar a exposição.
- **Evidência:** `app.py:21-57`; `settings.py:8`; `Dockerfile:41-42` (healthcheck em `/docs`)
- **Pré-requisito de exploração:** acesso de rede, sem autenticação.
- **Impacto técnico:** mapeamento completo de rotas, parâmetros e perfis, o que facilita o reconhecimento para os demais achados.
- **OWASP:** A05:2021 · **CWE:** CWE-200 · **CVE:** não aplicável
- **Recomendação inicial:** desabilitar a documentação em produção (`docs_url=None if not settings.API_DEBUG`) ou protegê-la com autenticação.

### VULN-018 — Nenhuma CSP ou cabeçalho de segurança no frontend

- **Componente afetado:** frontend (`public/*.html`) e serviço `frontend` (`nginx:alpine` com configuração padrão)
- **Classificação:** RC · **Confiança:** Alta
- **Descrição técnica:** nenhuma página define `Content-Security-Policy` via `<meta>`, e não há `nginx.conf` customizado que envie CSP, `X-Frame-Options`/`frame-ancestors`, `X-Content-Type-Options` ou `Referrer-Policy`. Além disso, o volume monta o diretório inteiro do frontend (incluindo `README.md`) como raiz web.
- **Evidência:** `grep -rn "http-equiv\|Content-Security-Policy" public` → sem ocorrências; `find . -name '*.conf'` → nenhum arquivo; `docker-compose.yaml:40-46`
- **Pré-requisito de exploração:** depende de outra falha (XSS em VULN-001, clickjacking).
- **Impacto técnico:** sem defesa em profundidade contra XSS e exfiltração de token; telas administrativas podem ser embutidas em *iframe*.
- **OWASP:** A05:2021 · **CWE:** CWE-693, CWE-1021 · **CVE:** não aplicável
- **Recomendação inicial:** `nginx.conf` com `Content-Security-Policy: default-src 'self'; connect-src <API>; frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`. Servir apenas `public/` e `assets/`.

---

## 5. Pontos que exigem validação manual (VM)

### VULN-019 — Tokens JWT sem revogação e sem `iss`/`aud`; algoritmo definido por variável de ambiente

- **Componente afetado:** backend `projeto_aplicado/auth/security.py`, `settings.py`
- **Classificação:** VM · **Confiança:** Média
- **Descrição técnica:**
  - Os tokens trazem apenas `sub` e `exp`, sem `iss`, `aud`, `iat` ou `jti`.
  - Não há logout no servidor, lista de revogação nem invalidação após troca de senha ou de perfil. O usuário é recarregado a cada requisição, então exclusão de conta e mudança de perfil têm efeito imediato, mas **troca de senha não invalida tokens emitidos**.
  - `JWT_ALGORITHM` vem do ambiente sem lista de valores permitidos.
  - No `.env` local, o algoritmo é `HS256`, a expiração é de 30 min e o segredo tem 35 caracteres. A entropia real é desconhecida, e isso é crítico por causa de VULN-004.
- **Evidência:** `auth/security.py:31-38` (claims), `:52-54` (`algorithms=[settings.JWT_ALGORITHM]`); `settings.py:39-41`
- **O que validar:** (1) entropia de `JWT_SECRET_KEY` em cada ambiente, sem expor o valor (ex.: confirmar que foi gerado por CSPRNG com 32 bytes ou mais); (2) se um token emitido antes de uma troca de senha continua aceito; (3) se algum ambiente define `JWT_ALGORITHM` com valor diferente de `HS256`/`RS256`.
- **Pré-requisito de exploração:** posse de um token previamente emitido.
- **Impacto técnico:** janela de uso de token comprometido de até `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`, mesmo após resposta a incidente.
- **OWASP:** A07:2021 · **CWE:** CWE-613; relacionado: CWE-1391 (se o segredo for fraco) · **CVE:** não aplicável
- **Recomendação inicial:** fixar a lista de algoritmos no código, incluir `iss`/`aud`/`iat`/`jti`, invalidar tokens após troca de senha (ex.: `token_version` no usuário) e gerar o segredo com `secrets.token_urlsafe(32)` ou mais.

### VULN-020 — Possível enumeração de usuários pelo tempo de resposta do login

- **Componente afetado:** backend `projeto_aplicado/auth/token.py`
- **Classificação:** VM · **Confiança:** Baixa
- **Descrição técnica:** quando o username não existe, a função retorna 401 **sem executar** a verificação Argon2. Quando existe, executa o hash. A mensagem é idêntica, mas o tempo de resposta tende a ser diferente.
- **Evidência:** `auth/token.py:24-36` (`if not user: raise …` antes de `verify_password`)
- **O que validar:** medir em ambiente autorizado a distribuição de tempos (dezenas de amostras) para usernames existentes e inexistentes.
- **Pré-requisito de exploração:** acesso de rede ao endpoint, sem autenticação.
- **Impacto técnico:** identificação de contas válidas para direcionar força bruta (VULN-005).
- **OWASP:** A07:2021 · **CWE:** CWE-208 · **CVE:** não aplicável
- **Recomendação inicial:** executar `verify_password` contra um hash fictício quando o usuário não existir, combinado com rate limiting.

### VULN-021 — Localizador de pedido previsível e sem unicidade

- **Componente afetado:** backend `projeto_aplicado/utils.py`, `resources/order/model.py`
- **Classificação:** VM · **Confiança:** Média
- **Descrição técnica:** o localizador tem 1 letra e 3 dígitos (26.000 combinações), é gerado com `random` (PRNG não criptográfico) e o índice no banco não é único. Hoje o localizador é só exibido aos operadores e todas as rotas exigem autenticação. Por isso **não há exploração demonstrada**. O risco passa a existir se ele virar identificador para clientes (ex.: consulta pública de status ou retirada de pedido), e há colisões garantidas com volume de pedidos.
- **Evidência:** `utils.py:61-67` (`random.choice`, `random.choices(string.digits, k=3)`); `order/model.py:19-21`; `migrations/versions/8649a7b6eb8e_init_migration.py:36` (`unique=False`)
- **O que validar:** se o localizador é ou será usado fora do contexto autenticado (ex.: chamada no painel, retirada), e se colisões no mesmo dia causam entrega errada.
- **Pré-requisito de exploração:** depende de uso futuro não autenticado.
- **Impacto técnico:** adivinhação de pedidos de terceiros ou confusão operacional por colisão.
- **OWASP:** A04:2021 · **CWE:** CWE-330, CWE-338 · **CVE:** não aplicável
- **Recomendação inicial:** gerar com `secrets`, garantir unicidade por dia (constraint mais nova tentativa) e não usar o localizador como fator de autorização.

---

## 6. Limitações desta análise

- Não houve execução da aplicação, dos testes ou de scanners dinâmicos. Comportamentos de runtime (ex.: VULN-007 item 3, VULN-015 Starlette, VULN-020) estão indicados como validação manual.
- Imagens Docker não foram baixadas nem varridas. Versões vêm das tags e do `uv.lock`.
- A infraestrutura de produção real, se existir, é desconhecida. A severidade dos RC depende dela.
- A documentação do backend cita uma CLI (`projeto_aplicado/cli`) que **não existe** no repositório. Ela não foi analisada.
- CVEs foram associados por versão e devem ser reconferidos no NVD e nos *advisories* dos fornecedores antes do relatório final.
- **Sem achado relevante nos seguintes pontos:** SQL injection (todas as consultas usam SQLAlchemy/SQLModel parametrizado); hashing de senha (Argon2); verificação de perfil nas rotas administrativas de usuários e produtos (feita no servidor); scripts externos no frontend (não há CDN, portanto SRI não se aplica); arquivo `.env` (ignorado pelo git e nunca commitado, verificado no histórico).

---

## 7. Técnica sugerida de priorização por dados

Proposta simples, auditável e baseada **apenas em atributos já registrados neste inventário** ou medidos depois (CVSS, EPSS). Nenhum valor numérico foi atribuído aqui, para não antecipar evidências que ainda não existem.

### 7.1 Fatores (preencher em `dados/vulnerabilidades.csv`)

| Fator | Escala | De onde vem o dado |
|---|---|---|
| **I – Impacto** | 1 a 5 | Subíndice de impacto do CVSS v3.1/v4.0 calculado na etapa 02 (C/I/A), ou a nota base normalizada (`CVSS ÷ 2`) |
| **P – Probabilidade** | 1 a 5 | Campo "Pré-requisito de exploração" de cada achado: sem autenticação e exposto na rede = 5; autenticado com qualquer perfil = 4; perfil específico = 3; admin ou acesso local = 2; dependente de outra falha = 1. Para itens com CVE, somar +1 (limitado a 5) se o CVE constar no **CISA KEV** ou tiver **EPSS** ≥ 0,1 |
| **C – Confiança** | multiplicador | VC com confiança Alta = 1,0 · Média = 0,8 · RC = 0,7 (até confirmar a exposição do ambiente) · VM = 0,5 |
| **E – Esforço de correção** | 1 a 3 | Estimativa da equipe responsável (1 = ajuste de configuração ou poucas linhas; 3 = mudança de arquitetura) |

### 7.2 Cálculo

```
Risco         = I × P × C          (faixa 0,5 a 25)
Prioridade    = Risco ÷ E          (desempate e identificação de "quick wins")
```

Na planilha, com o CSV já contendo as colunas `impacto`, `probabilidade`, `confianca` e `esforco`: `=I2*J2*K2` para risco e `=L2/M2` para prioridade. Em Python: `df["risco"] = df.impacto * df.probabilidade * df.confianca`, seguido de `df.sort_values(["risco", "esforco"], ascending=[False, True])`.

### 7.3 Uso do resultado

1. **Ordenar por Risco** e aplicar **Pareto**: tratar primeiro o menor conjunto de achados que soma cerca de 80% do risco total.
2. **Plotar Risco × Esforço** (quadrantes). Alto risco e baixo esforço são as correções imediatas. Alto risco e alto esforço entram no plano da etapa `04-mitigacao-raci`.
3. **Considerar encadeamentos** registrados no inventário. Quando um achado habilita outro (ex.: VULN-018 → VULN-001 → VULN-009; VULN-003 + VULN-005 + VULN-006; VULN-004 → VULN-019), o fator P do achado habilitador deve usar o maior P da cadeia.
4. **Reavaliar a cada validação.** Quando um VM for confirmado, C passa para 1,0. Quando for descartado, o item é encerrado com status "Falso positivo" no CSV. Isso mantém a matriz da etapa `03-matriz-risco` rastreável até a evidência.

### 7.4 Mapeamento sugerido para o CSV existente

O arquivo `dados/vulnerabilidades.csv` já tem as colunas `id, titulo, componente, ativo_afetado, origem, evidencia, cwe, cve, owasp, cvss_preliminar, impacto_tecnico, status`. Este inventário **não o alterou**. Sugere-se preencher uma linha por VULN deste documento, usar `origem = análise estática` e acrescentar as colunas `classificacao` (VC/RC/VM), `confianca`, `pre_requisito`, `probabilidade`, `esforco` e `risco` para aplicar a técnica acima.
