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
	  pip install playwright pytest pytest-playwright pytest-xdist
	  ```
4. **Instalar navegadores do Playwright**
	```bash
	playwright install
	```
5. **Configurar variáveis adicionais (se necessário)**
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

## 7. 🎨 Como expandir cenários

- **Novas tasks**: crie um método em `tasks/` para cada ação pequena e reutilizável.
- **Novas questions**: verifique estados finais (mensagens, elementos visíveis) em `questions/` usando `expect`.
- **Novos testes**: componha tasks e questions no estilo Arrange-Act-Assert em `tests/`.
- Mantenha os nomes autoexplicativos para facilitar leitura e manutenção.

## 8. 💡 Boas práticas

- Centralize seletores nas tasks para facilitar manutenção.
- Evite sleeps; prefira `expect` com Playwright para sincronização.
- Reaproveite ao máximo tasks/questions entre cenários semelhantes.
- Automatize formatação/linters (ex.: `ruff`, `black`) se o projeto crescer.

## 9. 🔧 Solução de problemas

- **Erro de navegadores ausentes**: reexecute `playwright install`.
- **Ambiente virtual não ativa**: confira o caminho correto do script de ativação conforme o shell.
- **Timeouts**: ajuste `page.set_default_timeout` dentro das tasks ou passe `--timeout` ao pytest.
- **Execução lenta**: reduza navegadores via `--browser` ou desative vídeos/traces temporariamente.

## 10. 🚀 Próximos passos sugeridos

- Adicionar pipeline CI para executar os testes automaticamente.
- Gerar relatórios enriquecidos (ex.: Allure) com integração ao Pytest.
- Documentar credenciais e ambientes de testes caso vá além do Sample App.
