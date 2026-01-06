# 🎭 SCREENPLAY com Playwright e Pytest

Guia passo a passo para configurar, entender e executar o projeto de testes automatizados usando Playwright com o padrão Screenplay.

## 1. 🎯 Visão geral

- **Objetivo**: automatizar cenários de login no site Sample App aplicando o padrão Screenplay em Python.
- **Tecnologias**: Playwright (API síncrona), Pytest, Xdist (execução paralela) e relatórios padrões do Playwright Test Runner.
- **Papéis**: `tasks` executam ações na página, `questions` validam resultados e `actors` coordenam esses comportamentos.

## 2. 📚 O Padrão Screenplay - Explicado em Detalhes

### 🤔 O que é Screenplay?

Screenplay é um padrão de design para testes de automação que organiza o código seguindo a metáfora de uma **peça de teatro**:
- **Ator**: o personagem que executa as ações.
- **Tasks (Tarefas)**: o que o ator faz (ações).
- **Questions (Questões)**: o que o ator observa ou valida (verificações).
- **Ability (Habilidade)**: como o ator executa as ações (ex.: interagir com a página web via Playwright).

### Estrutura Básica

```
┌─────────────────────────────────────────┐
│           Teste (test_login.py)         │
│                                         │
│  Arrange  → Actor.prepare()             │
│  Act      → actor.tasks.realizar_login()│
│  Assert   → actor.questions.validar()   │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│          Actor (actors/actor.py)        │
│   (Coordenador de Tasks e Questions)    │
└─────────────────────────────────────────┘
    ↙                               ↘
┌──────────────────────┐  ┌──────────────────────┐
│  Tasks               │  │  Questions           │
│  (O que fazer)       │  │  (O que observar)    │
│                      │  │                      │
│ • acessar_pagina()   │  │ • mensagem_boas_     │
│ • realizar_login()   │  │   vindas()           │
│ • fechar_pagina()    │  │ • campo_habilitado() │
└──────────────────────┘  └──────────────────────┘
         ↓                        ↓
┌───────────────────────────────────────────┐
│   Ability: Playwright Page                │
│   (Capacidade técnica do ator)            │
└───────────────────────────────────────────┘
```

### ✅ Vantagens do Screenplay

1. **Leitura Natural**: Os testes leem como um cenário, não como comandos técnicos.
   ```python
   # Sem Screenplay (imperativo):
   page.goto("...")
   page.get_by_placeholder(...).fill(...)
   page.get_by_role(...).click()
   
   # Com Screenplay (descritivo):
   login_task.realizar_login("dan", "pwd")
   login_question.mensagem_de_boas_vindas("dan")
   ```

2. **Reutilização**: Tasks e questions são componentes independentes reutilizáveis.
   - Uma task pode ser usada em múltiplos testes.
   - Mudanças na tela só afetam a task correspondente.

3. **Manutenção Simplificada**: Mudanças na interface afetam apenas uma task/question.
   - Centralização de seletores evita repetições.
   - Um único lugar para ajustar lógica.

4. **Escalabilidade**: Fácil adicionar novos cenários sem duplicação.
   - Novas combinações de tasks/questions com reutilização.
   - Arquitetura clara para times maiores.

5. **Legibilidade**: O código comunica intenção, não implementação.

### 🔧 Componentes Principais

#### ✏️ A) Tasks (Tarefas - O Que Fazer)

Tasks encapsulam **ações** que o usuário executa na página.

```python
# tasks/login_task.py
class LoginTask:
    def __init__(self, page: Page):
        self.page = page
    
    def acessar_pagina_login(self):
        """Tarefa: Navegar para a página de login"""
        self.page.goto("http://uitestingplayground.com/sampleapp")
    
    def realizar_login(self, username: str, password: str):
        """Tarefa: Preencher formulário e clicar em Login"""
        username_input = self.page.get_by_placeholder("User Name")
        password_input = self.page.locator("input[name=\"Password\"]")
        login_btn = self.page.get_by_role("button", name="Log In")
        
        username_input.fill(username)
        password_input.fill(password)
        login_btn.click()
    
    def fechar_pagina(self):
        """Tarefa: Fechar a página"""
        self.page.close()
```

**Boas práticas para Tasks:**
- Um método = uma ação lógica (micro-tasks).
- Nomes descritivos no imperativo (realizar_login, acessar_pagina).
- Centralizar todos os seletores.
- Sem assertions/validações (isso é função de questions).

#### 🔍 B) Questions (Questões - O Que Observar)

Questions encapsulam **validações** e **verificações** de estado.

```python
# questions/login_question.py
from playwright.sync_api import expect

class LoginQuestion:
    def __init__(self, page: Page):
        self.page = page
    
    def mensagem_de_boas_vindas(self, username: str):
        """Questão: A mensagem de boas-vindas aparece corretamente?"""
        label = self.page.locator("label#loginstatus")
        expect(label).to_have_text(f"Welcome, {username}!")
    
    def campo_senha_visivel(self):
        """Questão: O campo de senha está visível?"""
        password_field = self.page.locator("input[name=\"Password\"]")
        expect(password_field).to_be_visible()
```

**Boas práticas para Questions:**
- Nomes interrogativos semânticos (mensagem_de_boas_vindas, usuario_logado).
- Usar `expect` do Playwright para sincronização e legibilidade.
- Uma verificação clara por método.
- Sem efeitos colaterais (leitura apenas).

#### 🎬 C) Actor (Ator - Quem Executa)

Actor é o orquestrador que:
- Encapsula o acesso a tasks e questions.
- Gerencia habilidades (abilities) do ator.
- Conecta o ator ao navegador.

```python
# actors/actor.py
class Actor:
    def web_perform(self, task):
        """Ability: Executar ações na web"""
        return self.browser_type_launch_args(task)
    
    def browser_type_launch_args(self, browser_type_launch_args):
        """Configura navegador do ator"""
        return {
            **browser_type_launch_args,
            "headless": False,  # Ator vê o que faz
        }

def prepare_actor_login_task(page):
    """Factory: Ator com habilidade de realizar login"""
    return LoginTask(page)

def prepare_actor_login_question(page):
    """Factory: Ator com habilidade de verificar login"""
    return LoginQuestion(page)
```

### 📋 D) Teste - Orquestração Final

O teste monta a história completa:

```python
# tests/test_login.py
@pytest.mark.usefixtures("browser_type_launch_args")
def test_ct001_realizar_login_com_sucesso(page: Page):
    with allure.step("# Arrange - Preparar o ator com suas habilidades"):
        login_task = prepare_actor_login_task(page)
        login_question = prepare_actor_login_question(page)

    with allure.step("# Act - Acessar a página de login"):
        login_task.acessar_pagina_login()

    with allure.step("# Act - Realizar login com usuário 'dan' e senha 'pwd'"):
        login_task.realizar_login("dan", "pwd")

    with allure.step("# Assert - Verificar mensagem de boas-vindas"):
        login_question.mensagem_de_boas_vindas("dan")

    with allure.step("# Cleanup - Fechar a página"):
        login_task.fechar_pagina()
```

**Fluxo AAA (Arrange-Act-Assert):**
1. **Arrange**: Preparar o ator e seu contexto.
2. **Act**: Executar ações (tasks).
3. **Assert**: Validar resultado (questions).

### Exemplo Expandido: Adicionar Novo Cenario

Se quiser testar logout:

1. **Criar task em `LoginTask`**:
   ```python
   def realizar_logout(self):
       logout_btn = self.page.get_by_role("button", name="Log Out")
       logout_btn.click()
   ```

2. **Criar question em `LoginQuestion`**:
   ```python
   def usuario_deslogado(self):
       label = self.page.locator("label#loginstatus")
       expect(label).to_have_text("User logged out.")
   ```

3. **Usar no teste**:
   ```python
   login_task.realizar_logout()
   login_question.usuario_deslogado()
   ```

Sem duplicação, sem mudança na arquitetura. Puro Screenplay!

## 3. 📋 Requisitos

- Python 3.10 ou superior.
- Pip atualizado (`python -m pip install --upgrade pip`).
- Playwright com navegadores instalados (`playwright install`).
- Sistema operacional testado: Windows (funciona também em Linux e macOS com os mesmos comandos bash).

## 4. 🚀 Passo a passo de configuração

1. **Clonar o repositório**
	```bash
	git clone <url-do-repositorio>
	cd automation_playwright_python/design_patterns/SCREENPLAY
	```
2. **Criar ambiente virtual (recomendado)**
	```bash
	python -m venv .venv
	source .venv/Scripts/activate  # PowerShell: .venv\Scripts\Activate.ps1
	```
3. **Instalar dependências Python**
	- Se houver arquivo de requisitos, execute `pip install -r requirements.txt`.
	- Caso contrário, instale diretamente:
	  ```bash
	  pip install playwright pytest pytest-playwright pytest-xdist allure-pytest
	  ```
4. **Instalar navegadores do Playwright**
	```bash
	playwright install
	```
5. **Instalar Allure Command Line (para visualizar relatórios)**
	- **Windows** (via Scoop):
	  ```bash
	  scoop install allure
	  ```
	- **macOS** (via Homebrew):
	  ```bash
	  brew install allure
	  ```
	- **Linux** (manual):
	  ```bash
	  wget https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.tgz
	  tar -zxvf allure-2.24.0.tgz
	  sudo mv allure-2.24.0 /opt/allure
	  sudo ln -s /opt/allure/bin/allure /usr/bin/allure
	  ```
6. **Configurar variáveis adicionais (se necessário)**
	- Não há variáveis obrigatórias por padrão; ajuste apenas se o ambiente exigir proxy ou credenciais distintas.

## 5. 📂 Entendendo a estrutura

- `actors/actor.py`: cria o ator e prepara tasks/questions. Ajusta configuração do navegador (ex.: modo headless).
- `tasks/login_task.py`: encapsula cada interação com a página (acessar, logar, fechar).
- `questions/login_question.py`: valida mensagens ou estados esperados após as ações.
- `tests/test_login.py`: cenário de teste que orquestra tasks e questions.
- `tests/conftest.py`: fixture Pytest para adaptar `browser_type_launch_args` ao ator (habilita navegação visível).
- `pytest.ini`: define navegadores, paralelismo, coleta de evidências e pasta `test-reports/`.

## 6. 🧪 Executando os testes

1. Certifique-se de que o ambiente virtual esteja ativo e dependências instaladas.
2. Execute os testes com pytest:
	```bash
	pytest
	```
	- O arquivo `pytest.ini` já configura a execução nos navegadores Chromium, Firefox e WebKit, além de paralelismo (`--numprocesses 4`).
	- Screenshots, vídeos e traces são capturados somente em caso de erro e são salvos em `test-reports/`.
3. Para limitar navegadores ou desativar paralelismo, sobrescreva os argumentos:
	```bash
	pytest --browser chromium --numprocesses 1
	```

## 7. 📊 Visualizando Relatórios Allure

O projeto está configurado para gerar relatórios detalhados com Allure Report.

### Gerando e visualizando o relatório:

1. **Executar os testes** (os resultados são salvos em `allure-results/`):
	```bash
	pytest
	```

2. **Gerar e abrir o relatório HTML**:
	```bash
	allure serve allure-results
	```
	- Isso abre automaticamente o relatório no navegador.

3. **Ou gerar relatório estático**:
	```bash
	allure generate allure-results -o allure-report --clean
	```
	- Para visualizar: `allure open allure-report`

### Recursos do Allure no projeto:

- ✅ **Features e Stories**: Organização por funcionalidade (ex.: "Autenticação" > "Login de Usuário")
- ✅ **Steps detalhados**: Cada ação do teste aparece como um step visível
- ✅ **Severidade**: Classificação de criticidade dos testes (CRITICAL, NORMAL, etc.)
- ✅ **Descrições ricas**: Título e descrição clara de cada cenário
- ✅ **Screenshots e vídeos**: Anexados automaticamente em caso de falha (via Playwright)
- ✅ **Histórico de execuções**: Rastreamento de tendências ao longo do tempo
- ✅ **Gráficos e métricas**: Taxa de sucesso, duração, categorias de falhas

### Estrutura de anotações Allure no código:

```python
@allure.feature("Autenticação")  # Módulo/Feature
@allure.story("Login de Usuário")  # História de usuário
@allure.title("CT001 - Realizar login com sucesso")  # Título do teste
@allure.description("Descrição detalhada do cenário")  # Descrição
@allure.severity(allure.severity_level.CRITICAL)  # Severidade
def test_exemplo():
    with allure.step("Passo 1: Acessar página"):
        # código
    with allure.step("Passo 2: Preencher formulário"):
        # código
```

## 8. 🎨 Como expandir cenários

- **Novas tasks**: crie um método em `tasks/` para cada ação pequena e reutilizável.
- **Novas questions**: verifique estados finais (mensagens, elementos visíveis) em `questions/` usando `expect`.
- **Novos testes**: componha tasks e questions no estilo Arrange-Act-Assert em `tests/`.
- Mantenha os nomes autoexplicativos para facilitar leitura e manutenção.

## 9. 💡 Boas práticas

- Centralize seletores nas tasks para facilitar manutenção.
- Evite sleeps; prefira `expect` com Playwright para sincronização.
- Reaproveite ao máximo tasks/questions entre cenários semelhantes.
- Automatize formatação/linters (ex.: `ruff`, `black`) se o projeto crescer.
- **Use anotações Allure**: Adicione `@allure.feature`, `@allure.story`, `@allure.step` para documentação visual.
- **Organize por severidade**: Classifique testes críticos com `@allure.severity(allure.severity_level.CRITICAL)`.

## 10. 🔧 Solução de problemas

- **Erro de navegadores ausentes**: reexecute `playwright install`.
- **Ambiente virtual não ativa**: confira o caminho correto do script de ativação conforme o shell.
- **Timeouts**: ajuste `page.set_default_timeout` dentro das tasks ou passe `--timeout` ao pytest.
- **Execução lenta**: reduza navegadores via `--browser` ou desative vídeos/traces temporariamente.
- **Allure não encontrado**: certifique-se de que o Allure CLI está instalado (`allure --version`).
- **Relatório vazio**: verifique se a pasta `allure-results/` contém arquivos JSON após a execução.

## 11. 🚀 Próximos passos sugeridos

- Adicionar pipeline CI para executar os testes automaticamente e publicar relatórios Allure.
- Integrar Allure TestOps para gestão centralizada de testes.
- Documentar credenciais e ambientes de testes caso vá além do Sample App.
- Adicionar testes de API usando o mesmo padrão Screenplay.
- Configurar notificações (Slack, email) com resumo dos relatórios Allure.

---

## 12. 📝 Conclusão: Screenplay - Vale a Pena?

Após implementar e trabalhar com o padrão Screenplay, é importante entender suas vantagens e limitações para decidir quando aplicá-lo.

### ✅ Pontos Positivos

#### 1. **Legibilidade Superior**
Os testes ficam muito mais fáceis de ler e entender, mesmo para não-programadores. A metáfora teatral torna o código autoexplicativo:
```python
login_task.realizar_login("dan", "pwd")
login_question.mensagem_de_boas_vindas("dan")
```
É imediatamente claro o que está acontecendo, sem precisar mergulhar em detalhes técnicos.

#### 2. **Manutenção Centralizada**
Mudanças na interface afetam apenas um lugar. Se um seletor mudar, você ajusta apenas na task correspondente, e todos os testes que usam aquela task são automaticamente atualizados.

#### 3. **Reutilização Máxima**
Tasks e questions são componentes reutilizáveis. Uma vez criada, a task `realizar_login()` pode ser usada em dezenas de cenários diferentes sem duplicação de código.

#### 4. **Separação Clara de Responsabilidades**
- **Tasks**: só fazem ações (sem validações)
- **Questions**: só validam (sem efeitos colaterais)
- **Actor**: só orquestra
- **Testes**: só compõem a história

Essa separação torna o código mais limpo e previsível.

#### 5. **Escalabilidade para Times Grandes**
Em projetos com múltiplos QAs/desenvolvedores, o padrão facilita:
- Divisão de trabalho (um cria tasks, outro questions)
- Onboarding de novos membros (estrutura clara)
- Revisão de código (cada componente tem responsabilidade única)

#### 6. **Documentação Viva**
O código Screenplay serve como documentação. Um novo membro do time pode ler os testes e entender o fluxo da aplicação sem documentos externos.

#### 7. **Facilita TDD/BDD**
O padrão se alinha perfeitamente com Behavior-Driven Development. Os testes leem como especificações de negócio:
```python
# ARRANGE: Dado que o usuário está na página de login
# ACT: Quando ele realiza login com credenciais válidas
# ASSERT: Então ele vê a mensagem de boas-vindas
```

### ⚠️ Pontos Negativos

#### 1. **Curva de Aprendizado Inicial**
Para iniciantes em automação, Screenplay adiciona uma camada de abstração que pode confundir. Há mais conceitos para entender (Actor, Tasks, Questions, Abilities) antes de escrever o primeiro teste.

**Impacto**: Times júniores podem levar mais tempo para se adaptar.

#### 2. **Overhead de Código (Boilerplate)**
Para testes simples, Screenplay pode parecer "over-engineering". Compare:

```python
# Sem Screenplay (direto):
page.goto("url")
page.fill("input", "valor")
page.click("button")
expect(page.locator("label")).to_have_text("Sucesso")

# Com Screenplay:
# Criar LoginTask.py com classe e métodos
# Criar LoginQuestion.py com classe e métodos  
# Criar prepare_actor no actor.py
# Só então escrever o teste que usa tudo isso
```

Para um teste pontual, o Screenplay adiciona arquivos e linhas extras.

**Impacto**: Projetos pequenos (10-50 testes) podem não justificar a estrutura.

#### 3. **Performance de Desenvolvimento Inicial Mais Lenta**
Criar a estrutura de pastas, classes, e factories leva tempo. Nos primeiros testes, a velocidade de entrega é menor comparada a testes diretos.

**Impacto**: Em sprints curtos ou POCs, pode parecer lento demais.

#### 4. **Excesso de Abstração Pode Dificultar Debug**
Quando um teste falha, você precisa navegar por múltiplos arquivos (task → question → locator) para encontrar o problema. Em testes diretos, tudo está em um lugar.

**Impacto**: Debugging pode ser menos intuitivo, especialmente com stacks trace longas.

#### 5. **Risco de Micro-Tasks Excessivas**
Há uma tentação de criar tasks para cada clique ou preenchimento, levando a uma fragmentação exagerada:
```python
# Excesso de granularidade:
login_task.clicar_campo_usuario()
login_task.digitar_usuario("dan")
login_task.clicar_campo_senha()
login_task.digitar_senha("pwd")
login_task.clicar_botao_login()
```

Isso torna o código verboso e dificulta a leitura.

**Impacto**: É preciso bom senso para definir o nível certo de granularidade.

#### 6. **Não Elimina Flakiness**
Screenplay organiza o código, mas não resolve problemas de sincronização, timeouts ou instabilidade de aplicação. Testes ainda podem falhar por problemas externos ao padrão.

**Impacto**: Não é uma solução mágica para testes instáveis.

#### 7. **Dependência de Convenções do Time**
O sucesso do Screenplay depende do time seguir as convenções consistentemente. Se alguns membros criam tasks detalhadas e outros criam tasks genéricas, a base de código fica inconsistente.

**Impacto**: Requer disciplina e code reviews rigorosos.

### 🎯 Quando Usar Screenplay?

**✅ USE quando:**
- Projeto tem **10+ cenários de teste**
- Time tem **múltiplos QAs/desenvolvedores**
- Aplicação tem **alta taxa de mudança na UI**
- Precisa de **testes legíveis para stakeholders**
- Vai construir uma **suite de testes de longo prazo**
- Time valoriza **manutenção sobre velocidade inicial**

**❌ EVITE quando:**
- Projeto tem **menos de 5 testes**
- É um **POC ou MVP rápido**
- Time é **muito júnior** e sem mentoria
- Deadline é **extremamente apertado**
- Testes são **descartáveis ou temporários**
- Não há **compromisso com padrões** no time

### 🏆 Veredicto Final

O padrão Screenplay é uma **excelente escolha para projetos de médio a grande porte** onde manutenibilidade, legibilidade e escalabilidade são prioridades. O investimento inicial em estrutura se paga rapidamente quando a suite de testes cresce.

Porém, não é bala de prata. Para projetos pequenos ou experimentais, a simplicidade de testes diretos pode ser mais adequada. **O contexto do projeto deve guiar a decisão**.

**Recomendação**: Se você está começando um projeto de automação que vai crescer, adote Screenplay desde o início. Se está fazendo testes pontuais, comece simples e refatore para Screenplay quando sentir a dor da duplicação e manutenção.
