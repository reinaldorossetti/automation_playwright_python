# 🎭 SCREENPLAY com Playwright e Pytest

Guia passo a passo para configurar, entender e executar o projeto de testes automatizados usando Playwright com o padrao Screenplay.

## 1. 🎯 Visao geral

- **Objetivo**: automatizar cenarios de login no site Sample App aplicando o padrao Screenplay em Python.
- **Tecnologias**: Playwright (API sincrona), Pytest, Xdist (execucao paralela) e relatorios padroes do Playwright Test Runner.
- **Papeis**: `tasks` executam acoes na pagina, `questions` validam resultados e `actors` coordenam esses comportamentos.

## 2. 📚 O Padrao Screenplay - Explicado em Detalhes

### 🤔 O que eh Screenplay?

Screenplay eh um padrao de design para testes de automacao que organiza o codigo seguindo a metafora de uma **peca de teatro**:
- **Ator**: o personagem que executa as acoes.
- **Tasks (Tarefas)**: o que o ator faz (acoes).
- **Questions (Questoes)**: o que o ator observa ou valida (verificacoes).
- **Ability (Habilidade)**: como o ator executa as acoes (ex.: interagir com a pagina web via Playwright).

### Estrutura Basica

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
│   (Capacidade tecnica do ator)            │
└───────────────────────────────────────────┘
```

### ✅ Vantagens do Screenplay

1. **Leitura Natural**: Os testes leem como um cenario, nao como comandos tecnicos.
   ```python
   # Sem Screenplay (imperativo):
   page.goto("...")
   page.get_by_placeholder(...).fill(...)
   page.get_by_role(...).click()
   
   # Com Screenplay (descritivo):
   login_task.realizar_login("dan", "pwd")
   login_question.mensagem_de_boas_vindas("dan")
   ```

2. **Reutilizacao**: Tasks e questions sao componentes independentes reutilizaveis.
   - Uma task pode ser usada em multiplos testes.
   - Mudancas na tela so afetam a task correspondente.

3. **Manutencao Simplificada**: Mudancas na interface afetam apenas uma task/question.
   - Centralizacao de seletores evita repeticoes.
   - Um unico lugar para ajustar logic.

4. **Escalabilidade**: Facil adicionar novos cenarios sem duplicacao.
   - Novas combinacoes de tasks/questions com reutilizacao.
   - Arquitetura clara para times maiores.

5. **Legibilidade**: O codigo comunica intencao, nao implementacao.

### 🔧 Componentes Principais

#### ✏️ A) Tasks (Tarefas - O Que Fazer)

Tasks encapsulam **acoes** que o usuario executa na pagina.

```python
# tasks/login_task.py
class LoginTask:
    def __init__(self, page: Page):
        self.page = page
    
    def acessar_pagina_login(self):
        """Tarefa: Navegar para a pagina de login"""
        self.page.goto("http://uitestingplayground.com/sampleapp")
    
    def realizar_login(self, username: str, password: str):
        """Tarefa: Preencher formulario e clicar em Login"""
        username_input = self.page.get_by_placeholder("User Name")
        password_input = self.page.locator("input[name=\"Password\"]")
        login_btn = self.page.get_by_role("button", name="Log In")
        
        username_input.fill(username)
        password_input.fill(password)
        login_btn.click()
    
    def fechar_pagina(self):
        """Tarefa: Fechar a pagina"""
        self.page.close()
```

**Boas praticas para Tasks:**
- Um metodo = uma acao logica (micro-tasks).
- Nomes descritivos no imperativo (realizar_login, acessar_pagina).
- Centralizar todos os seletores.
- Sem assertions/validacoes (isso eh funcao de questions).

#### 🔍 B) Questions (Questoes - O Que Observar)

Questions encapsulam **validacoes** e **verificacoes** de estado.

```python
# questions/login_question.py
from playwright.sync_api import expect

class LoginQuestion:
    def __init__(self, page: Page):
        self.page = page
    
    def mensagem_de_boas_vindas(self, username: str):
        """Questao: A mensagem de boas-vindas aparece corretamente?"""
        label = self.page.locator("label#loginstatus")
        expect(label).to_have_text(f"Welcome, {username}!")
    
    def campo_senha_visivel(self):
        """Questao: O campo de senha estah visivel?"""
        password_field = self.page.locator("input[name=\"Password\"]")
        expect(password_field).to_be_visible()
```

**Boas praticas para Questions:**
- Nomes interrogativos semanticos (mensagem_de_boas_vindas, usuario_logado).
- Usar `expect` do Playwright para sincronizacao e legibilidade.
- Uma verificacao clara por metodo.
- Sem efeitos colaterais (leitura apenas).

#### 🎬 C) Actor (Ator - Quem Executa)

Actor eh o orquestrador que:
- Encapsula o acesso a tasks e questions.
- Gerencia habilidades (abilities) do ator.
- Conecta o ator ao navegador.

```python
# actors/actor.py
class Actor:
    def web_perform(self, task):
        """Ability: Executar acoes na web"""
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

### 📋 D) Teste - Orquestracacao Final

O teste monta a historia completa:

```python
# tests/test_login.py
def test_ct001_realizar_login_com_sucesso(page: Page):
    # ARRANGE: Preparar o ator com suas habilidades
    login_task = prepare_actor_login_task(page)
    login_question = prepare_actor_login_question(page)
    
    # ACT: Ator executa tarefas (Tasks)
    login_task.acessar_pagina_login()
    login_task.realizar_login("dan", "pwd")
    
    # ASSERT: Ator valida resultado (Questions)
    login_question.mensagem_de_boas_vindas("dan")
    
    # CLEANUP: Fechar
    login_task.fechar_pagina()
```

**Fluxo AAA (Arrange-Act-Assert):**
1. **Arrange**: Preparar o ator e seu contexto.
2. **Act**: Executar acoes (tasks).
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

Sem duplicacao, sem mudanca na arquitetura. Puro Screenplay!

## 3. 📋 Requisitos

- Python 3.10 ou superior.
- Pip atualizado (`python -m pip install --upgrade pip`).
- Playwright com navegadores instalados (`playwright install`).
- Sistema operacional testado: Windows (funciona também em Linux e macOS com os mesmos comandos bash).

## 4. 🚀 Passo a passo de configuracao

1. **Clonar o repositorio**
	```bash
	git clone <url-do-repositorio>
	cd automation_playwright_python/design_patterns/SCREENPLAY
	```
2. **Criar ambiente virtual (recomendado)**
	```bash
	python -m venv .venv
	source .venv/Scripts/activate  # PowerShell: .venv\Scripts\Activate.ps1
	```
3. **Instalar dependencias Python**
	- Se houver arquivo de requisitos, execute `pip install -r requirements.txt`.
	- Caso contrario, instale diretamente:
	  ```bash
	  pip install playwright pytest pytest-playwright pytest-xdist
	  ```
4. **Instalar navegadores do Playwright**
	```bash
	playwright install
	```
5. **Configurar variaveis adicionais (se necessario)**
	- Nao ha variaveis obrigatorias por padrao; ajuste apenas se o ambiente exigir proxy ou credenciais distintas.

## 5. 📂 Entendendo a estrutura

- `actors/actor.py`: cria o ator e prepara tasks/questions. Ajusta configuracao do navegador (ex.: modo headless).
- `tasks/login_task.py`: encapsula cada interacao com a pagina (acessar, logar, fechar).
- `questions/login_question.py`: valida mensagens ou estados esperados apos as acoes.
- `tests/test_login.py`: cenario de teste que orquestra tasks e questions.
- `tests/conftest.py`: fixture Pytest para adaptar `browser_type_launch_args` ao ator (habilita navegacao visivel).
- `pytest.ini`: define navegadores, paralelismo, coleta de evidencias e pasta `test-reports/`.

## 6. 🧪 Executando os testes

1. Certifique-se de que o ambiente virtual esteja ativo e dependencias instaladas.
2. Execute os testes com pytest:
	```bash
	pytest
	```
	- O arquivo `pytest.ini` ja configura a execucao nos navegadores Chromium, Firefox e WebKit, alem de paralelismo (`--numprocesses 4`).
	- Screenshots, videos e traces falham somente em caso de erro e sao salvos em `test-reports/`.
3. Para limitar navegadores ou desativar paralelismo, sobrescreva os argumentos:
	```bash
	pytest --browser chromium --numprocesses 1
	```

## 7. 🎨 Como expandir cenarios

- **Novas tasks**: crie um metodo em `tasks/` para cada acao pequena e reutilizavel.
- **Novas questions**: verifique estados finais (mensagens, elementos visiveis) em `questions/` usando `expect`.
- **Novos testes**: componha tasks e questions no estilo Arrange-Act-Assert em `tests/`.
- Mantenha os nomes autoexplicativos para facilitar leitura e manutencao.

## 8. 💡 Boas praticas

- Centralize seletores nas tasks para facilitar manutencao.
- Evite sleeps; prefira `expect` com Playwright para sincronizacao.
- Reaproveite ao maximo tasks/questions entre cenarios semelhantes.
- Automatize formatacao/linters (ex.: `ruff`, `black`) se o projeto crescer.

## 9. 🔧 Solucao de problemas

- **Erro de navegadores ausentes**: reexecute `playwright install`.
- **Ambiente virtual nao ativa**: confira o caminho correto do script de ativacao conforme o shell.
- **Timeouts**: ajuste `page.set_default_timeout` dentro das tasks ou passe `--timeout` ao pytest.
- **Execucao lenta**: reduza navegadores via `--browser` ou desative videos/traces temporariamente.

## 10. 🚀 Proximos passos sugeridos

- Adicionar pipeline CI para executar os testes automaticamente.
- Gerar relatorios enriquecidos (ex.: Allure) com integracao ao Pytest.
- Documentar credenciais e ambientes de testes caso va alem do Sample App.
