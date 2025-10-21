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

✅ Conclusão

Com o pytest, pytest-mock, pytest-cov, pytest-xdist e pytest-playwright, você tem uma suíte completa para:

*   Testes unitários e de integração
*   Testes de interface automatizados
*   Mock de chamadas HTTP
*   Execução paralela e cobertura de código
*   Manutenção facilitada com fixtures organizadas

Reinaldo, quer que eu te monte também um exemplo prático de conftest.py completo com fixtures de Playwright e mocks integrados (como um setup real de automação web + API)?
