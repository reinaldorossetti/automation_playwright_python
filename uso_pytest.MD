🧪 Guia Definitivo de Uso do Pytest em Python

Autor: Reinaldo

Versão: 2.0 (Atualizada para 2025)

Frameworks abordados: pytest, pytest-xdist, pytest-playwright, pytest-mock

## 1. 📘 O que é o Pytest?

O pytest é um dos frameworks de teste mais populares e poderosos do ecossistema Python.

Ele oferece uma forma simples, declarativa e Pythonic de escrever testes — desde unitários até testes de integração e fim a fim.

**Principais vantagens:**
*   **Sintaxe Simples:** você escreve `assert` como no Python puro.
*   **Descoberta Automática:** pytest encontra os testes automaticamente.
*   **Fixtures:** permitem gerenciar dependências e estados de teste.
*   **Ecosistema de Plugins:** integração com Django, FastAPI, Playwright, cobertura de código, mocks, paralelização e muito mais.
*   **Excelente Relatório de Falhas:** mensagens ricas e fáceis de ler.

## 2. ⚙️ Instalação

É sempre recomendado o uso de um ambiente virtual.

````bash
pip install pytest
````

Plugins úteis:
````bash
pip install pytest-mock pytest-cov pytest-xdist pytest-playwright
````

## 3. 🧮 Escrevendo o primeiro teste
Código a ser testado — calculadora.py
```python
def somar(a, b):
    """Soma dois números."""
    return a + b

def subtrair(a, b):
    """Subtrai dois números."""
    return a - b
```

Arquivo de teste — test_calculadora.py
```python
from calculadora import somar, subtrair

def test_somar():
    """Testa a função somar com números positivos."""
    assert somar(2, 3) == 5
    assert somar(10, 10) == 20

def test_subtrair():
    """Testa a subtração simples."""
    assert subtrair(10, 5) == 5
```

Executar:
````bash
pytest -v
````

## 4. ⚡ Fixtures – Injeção de Dependências Reutilizáveis

Fixtures são funções que preparam um contexto (dados, conexões, objetos) e o injetam nos testes automaticamente.

Fixture simples — test_dados.py
```python
import pytest

@pytest.fixture
def dados_iniciais():
    """Fixture que retorna um dicionário de exemplo."""
    print("\n(SETUP) Criando dicionário...")
    return {"nome": "Ana", "idade": 30}

def test_verificar_nome(dados_iniciais):
    assert dados_iniciais["nome"] == "Ana"

def test_verificar_idade(dados_iniciais):
    assert isinstance(dados_iniciais["idade"], int)
```


Execute com:

````bash
pytest -s
````

## 5. 🔄 Fixtures com Setup e Teardown

Use yield dentro da fixture para executar código antes e depois dos testes (setup/teardown).

```python
@pytest.fixture
def cliente_db():
    print("\n(SETUP) Conectando ao banco de dados...")
    db = conectar_ao_db()
    yield db
    print("\n(TEARDOWN) Desconectando do banco de dados...")
    db.desconectar()
```

## 6. 🏷️ Marcadores e Agrupamentos

Marcadores permitem categorizar e filtrar testes.

```python
import pytest
import time, sys

@pytest.mark.smoke
def test_funcionalidade_essencial():
    assert True

@pytest.mark.slow
def test_funcionalidade_lenta():
    time.sleep(2)
    assert True

@pytest.mark.skip(reason="Ainda não implementado")
def test_funcionalidade_futura():
    assert False

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requer Python 3.10+")
def test_python10():
    assert True

@pytest.mark.xfail(reason="Bug conhecido #123")
def test_com_bug():
    assert 1 == 2

### Marcadores Específicos do Playwright

O `pytest-playwright` fornece marcadores especiais para controlar a execução de testes com base no navegador.

```python
import pytest
from playwright.sync_api import Page

@pytest.mark.skip_browser("firefox")
def test_funcionalidade_nao_suportada_no_firefox(page: Page):
    """
    Este teste será pulado se estiver sendo executado no Firefox.
    Será executado em Chromium e WebKit.
    """
    page.goto("https://example.com")
    assert "Example" in page.title()

@pytest.mark.only_browser("chromium")
def test_funcionalidade_apenas_no_chromium(page: Page):
    """
    Este teste será executado APENAS no Chromium.
    Será pulado em Firefox e WebKit.
    """
    page.goto("https://example.com")
    assert "Example" in page.title()
```

## 7. 🚀 Testes em Paralelo com pytest-xdist

Para projetos grandes, paralelize:

````bash
pytest -n 4
````

Ou use todos os núcleos disponíveis:

````bash
pytest -n auto
````

## 8. 🔀 Parametrização de Testes
```python
import pytest
from calculadora import somar

@pytest.mark.parametrize("a,b,resultado", [
    (2, 3, 5),
    (-1, 1, 0),
    (10, 10, 20),
])
def test_somar_varios(a, b, resultado):
    assert somar(a, b) == resultado
```

## 9. ❌ Testando Exceções
```python
import pytest

def dividir(a, b):
    if b == 0:
        raise ValueError("Divisão por zero não permitida")
    return a / b

def test_divisao_erro():
    with pytest.raises(ValueError, match="Divisão por zero"):
        dividir(1, 0)
```

## 10. 🔧 Configuração com pytest.ini
VS Code
(rerun without)
### O arquivo pytest.ini é um arquivo de configuração que permite definir opções padrão para o pytest, evitando a necessidade de digitá-las repetidamente na linha de comando.

[pytest]: Esta é a seção principal que contém todas as configurações do pytest.
markers: Registra marcadores personalizados. Isso evita erros de digitação e permite que o pytest saiba quais marcadores são intencionais. No exemplo, smoke, slow e api são registrados com suas descrições.

testpaths: Especifica os diretórios onde o pytest deve procurar por testes. No exemplo, os testes serão procurados apenas na pasta tests.

python_files: Define os padrões de nome de arquivo que o pytest considerará como arquivos de teste. No exemplo, arquivos que começam com test_ ou terminam com _test serão coletados.

addopts: Adiciona opções de linha de comando que serão executadas por padrão em cada execução do pytest. As opções do Playwright são configuradas aqui:
--browser: Especifica em qual navegador (ou navegadores) os testes devem ser executados. Você pode listar chromium, firefox e webkit.
--screenshot only-on-failure: Captura uma imagem da tela automaticamente, mas a salva apenas se o teste falhar.
--video retain-on-failure: Grava um vídeo da execução do teste e o mantém somente se o teste falhar.
--tracing on: Habilita o rastreamento do Playwright, que gera um arquivo de rastreio detalhado para depuração pós-execução.
--numprocesses 4: Opção do pytest-xdist que executa os testes em paralelo usando 4 processos, acelerando a execução.

```ini
# filepath: pytest.ini
[pytest]
markers =
    smoke: Testes essenciais de validação
    slow: Testes lentos
    api: Testes de API
addopts = 
    --browser chromium
    --browser firefox
    --browser webkit
    --screenshot only-on-failure
    --video retain-on-failure
    --tracing on
    --numprocesses 4
testpaths = tests
python_files = test_*.py *_test.py
```

## 11. 📈 Relatório de Cobertura de Código
````bash
pytest --cov=calculadora --cov-report=term-missing --cov-report=html
````


Gera um relatório no console e um HTML em htmlcov/index.html.

## 12. 🧩 Integrando Pytest com Playwright

O plugin pytest-playwright permite automatizar navegadores (Chromium, Firefox, WebKit) facilmente.

Instalação:
````bash
pip install pytest-playwright
playwright install
````

Exemplo de Fixture com Page:
```python
# filepath: tests/test_google.py
def test_titulo_google(page):
    """Verifica o título da página principal do Google."""
    page.goto("https://www.google.com")
    assert "Google" in page.title()
```

Fixture personalizada para login automatizado:
```python
import pytest

@pytest.fixture(scope="session")
def pagina_logada(browser):
    """Abre o navegador, faz login e retorna página autenticada."""
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://meusistema.com/login")
    page.fill("#usuario", "admin")
    page.fill("#senha", "123456")
    page.click("#entrar")
    page.wait_for_selector("#dashboard")
    yield page
    context.close()

def test_dashboard_acesso(pagina_logada):
    """Verifica se a página do dashboard carrega corretamente."""
    assert "Dashboard" in pagina_logada.title()
```

## 13. 🌐 Mockando Requisições com Pytest + Requests + pytest-mock

Usar o plugin pytest-mock simplifica o uso de mocks, sem precisar do unittest.mock manualmente.

Exemplo — Mockando uma requisição com requests.get
```python
import pytest
import requests

def buscar_usuario():
    resposta = requests.get("https://api.example.com/users/1")
    return resposta.json()

def test_buscar_usuario_mockado(mocker):
    """Mocka a função requests.get para simular uma API externa."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"id": 1, "nome": "Reinaldo"}
    mocker.patch("requests.get", return_value=mock_response)

    resultado = buscar_usuario()
    assert resultado["nome"] == "Reinaldo"
```

Mockando Requisição dentro do Playwright:
```python
def test_mock_request(page):
    """Simula a resposta de uma API dentro do navegador."""
    page.route("**/api/dados", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"usuario":"mockado","status":"ok"}'
    ))

    page.goto("https://meusistema.com/dashboard")
    response = page.evaluate("fetch('/api/dados').then(r => r.json())")
    assert response["usuario"] == "mockado"
```

## 14. ⏱️ Dicas Avançadas de Uso Diário
*   `pytest -s` → mostra `print()` no terminal
*   `pytest -x` → para no primeiro erro
*   `pytest --lf` → roda apenas os últimos testes que falharam
*   `pytest -v -m "smoke and not slow"` → filtros de marcadores compostos
*   `pytest tests/nome_do_arquivo_de_teste.py` → roda todos os testes em um arquivo específico

## 15. 💡 Boas Práticas
*   Cada teste deve isolar comportamento independente.
*   Nomeie claramente os testes com verbos: `test_calcula_media`, `test_login_sucesso`, etc.
*   Use fixtures reutilizáveis em `conftest.py` (escopos: function, class, module, session).
*   Sempre use `pytest-cov` em pipelines CI/CD para medir cobertura.
*   Evite chamadas reais de rede; prefira mockar requisições (consistência + performance).

## 16. 🌍 Estrutura de Projeto Recomendada
```plaintext
/automation_playwright_python
├── src/
│   ├── calculadora.py
│   └── ...
├── tests/
│   ├── conftest.py        # Fixtures globais
│   ├── test_calculadora.py
│   ├── test_api_mock.py
│   └── test_ui_login.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## 17. 🔬 Exemplos de fixtures com todos os escopos (Playwright) — explicado

Abaixo há exemplos de fixtures usando pytest-playwright cobrindo todos os escopos suportados pelo pytest: function (padrão), class, module, package e session. Cada exemplo mostra como criar contextos/páginas e quando usar cada escopo.

Importante: pytest-playwright já fornece fixtures úteis como `browser` e `page` (o `page` é function-scoped por padrão). Nos exemplos abaixo usamos a fixture `browser` para criar contextos e páginas manualmente.

### Escopo: function (padrão)
Isolamento máximo — cria contexto/página para cada teste. Recomendada para maior independência entre testes.
```python
import pytest

def test_function_scope(page):  # usa o page fornecido pelo pytest-playwright
    page.goto("https://example.com")
    assert "Example" in page.title()
```

### Escopo: class
Reusa a mesma página/contexto para todos os testes de uma classe. Útil quando múltiplos testes dentro da classe podem compartilhar estado ou setup custoso.
```python
import pytest

@pytest.fixture(scope="class")
def class_page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

class TestClassScope:
    def test_a(self, class_page):
        class_page.goto("https://example.com/a")
        assert "Example" in class_page.title()

    def test_b(self, class_page):
        class_page.goto("https://example.com/b")
        assert "Example" in class_page.title()
```

### Escopo: module
Cria uma página/contexto para todos os testes dentro de um módulo (arquivo .py). Boa opção quando vários testes do mesmo módulo compartilham setup.
```python
import pytest

@pytest.fixture(scope="module")
def module_page(browser):
    ctx = browser.new_context()
    page = ctx.new_page()
    yield page
    ctx.close()

def test_module_1(module_page):
    module_page.goto("https://example.com/1")
    assert module_page.url.endswith("/1")

def test_module_2(module_page):
    module_page.goto("https://example.com/2")
    assert module_page.url.endswith("/2")
```

### Escopo: package
Reusa o mesmo contexto/página para todos os testes em um pacote (diretório com __init__.py). Útil para suites grandes organizadas por pacotes.
Observação: o `scope="package"` tem efeito quando os testes estão dentro de um pacote Python.
```python
import pytest

@pytest.fixture(scope="package")
def package_context(browser):
    ctx = browser.new_context()
    yield ctx
    ctx.close()

# Em testes dentro do mesmo package, use package_context para criar páginas:
def test_in_package(page_factory, package_context):
    page = package_context.new_page()
    page.goto("https://example.com/package")
    assert "Example" in page.title()
    page.close()
```

### Escopo: session
Cria o recurso uma vez por sessão de testes (toda execução do pytest). Máxima economia de tempo, porém maior risco de vazamento de estado entre testes — usar com cuidado.
```python
import pytest

@pytest.fixture(scope="session")
def session_context(browser):
    # abre um contexto que dura toda a sessão de testes
    ctx = browser.new_context()
    yield ctx
    ctx.close()

def test_session_1(session_context):
    p = session_context.new_page()
    p.goto("https://example.com/s1")
    assert "Example" in p.title()
    p.close()

def test_session_2(session_context):
    p = session_context.new_page()
    p.goto("https://example.com/s2")
    assert "Example" in p.title()
    p.close()
```

### Observações e recomendações rápidas
* Use `function` (padrão) para maior isolamento e testes confiáveis.
* Use `class` ou `module` quando o setup for custoso e os testes puderem compartilhar estado com segurança.
* Use `session` ou `package` apenas quando a redução de tempo justificar o risco de vazamento de estado — prefira criar/fechar páginas (page.close()) entre testes.
* Ao reutilizar contextos/páginas, sempre fechar páginas abertas (`page.close()`) e testar se o estado compartilhado não afeta assertivas.

## 18. 🧩 Pytest‑BDD — exemplos rápidos

Abaixo há exemplos mínimos de uso do pytest-bdd integrados com pytest-playwright: um arquivo feature (Gherkin), definições de passos (step definitions) em Python e uma nota sobre fixtures. Copie os arquivos para a estrutura do projeto indicada e adapte seletores/URLs ao seu sistema.

Breve execução: instale pytest-bdd e execute com `pip install pytest-bdd` e depois `pytest -k login` ou apenas `pytest`.

````gherkin
# filepath: features/login.feature
Feature: Login de usuário

  Background:
    Given the application is running

  Scenario: Login com sucesso
    Given I open the login page
    When I submit valid credentials
    Then I should see the dashboard

  Scenario Outline: Falha de login
    Given I open the login page
    When I submit credentials "<user>" "<password>"
    Then I should see an error message

    Examples:
      | user    | password |
      | wrong   | wrong    |
      | locked  | secret   |
````

Definições de passos — test_login.py
```python
import pytest
from playwright.sync_api import Page

@pytest.mark.playwright
@pytest.fixture(scope="feature")
def dado_aplicacao_em_execucao(page: Page):
    """Cenário: A aplicação está em execução"""
    # Supondo que o servidor da aplicação esteja rodando localmente na porta 8000
    page.goto("http://localhost:8000")
    yield
    # Aqui você pode adicionar código para rodar após o teste, se necessário

@pytest.mark.playwright
def test_login_com_sucesso(page: Page, dado_aplicacao_em_execucao):
    """Cenário: Login com sucesso"""
    page.goto("http://localhost:8000/login")
    page.fill("input[name='username']", "usuario_valido")
    page.fill("input[name='password']", "senha_valida")
    page.click("button[type='submit']")
    page.wait_for_selector("text=Bem-vindo ao seu painel")
    assert page.url == "http://localhost:8000/dashboard"

@pytest.mark.playwright
def test_login_falha(page: Page, dado_aplicacao_em_execucao):
    """Cenário: Falha de login"""
    page.goto("http://localhost:8000/login")
    page.fill("input[name='username']", "usuario_invalido")
    page.fill("input[name='password']", "senha_invalida")
    page.click("button[type='submit']")
    page.wait_for_selector("text=Credenciais inválidas")
    assert page.url == "http://localhost:8000/login"
```

Nota sobre fixtures:

As fixtures do pytest-bdd (como `given`, `when`, `then`) são usadas para definir o comportamento esperado da aplicação em cada passo do cenário. Elas são automaticamente vinculadas aos testes baseados em suas marcações (por exemplo, `@pytest.mark.playwright`).

## Referências

- Documentação do projeto
  - README principal: [README.md](./README.md) — visão geral do repositório e instruções de uso.
  - Documentação interna: [docs/](./docs/) — guias, padrões e exemplos internos (se existir).
  - Contribuição: [CONTRIBUTING.md](./CONTRIBUTING.md) — normas para commits, PRs e execução de testes no CI.
  - Arquivos de configuração e fixtures: [conftest.py](./tests/conftest.py) — exemplos de fixtures compartilhadas.

- Documentação oficial e plugins
  - Pytest: https://docs.pytest.org/
  - Playwright for Python: https://playwright.dev/python/
  - pytest-playwright (plugin): https://github.com/microsoft/playwright-pytest
  - pytest-mock: https://pytest-mock.readthedocs.io/
  - pytest-xdist (paralelização): https://pypi.org/project/pytest-xdist/
  - pytest-cov (cobertura): https://pytest-cov.readthedocs.io/

- Comandos úteis / referência rápida
  - Instalar navegadores Playwright: `playwright install` — veja https://playwright.dev/docs/installation
  - Executar testes com múltiplos navegadores: `pytest --browser chromium --browser firefox --browser webkit`
  - Executar testes em paralelo: `pytest -n auto` (requires pytest-xdist)

## ✅ Conclusão

Com o pytest, pytest-mock, pytest-cov, pytest-xdist e pytest-playwright, você tem uma suíte completa para:

*   Testes unitários e de integração
*   Testes de interface automatizados
*   Mock de chamadas HTTP
*   Execução paralela e cobertura de código
*   Manutenção facilitada com fixtures organizadas

