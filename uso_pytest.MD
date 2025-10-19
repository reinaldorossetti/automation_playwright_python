# Guia de Uso do Pytest em Python

Este documento é um guia prático para começar a usar o `pytest`, um dos frameworks de teste mais populares e poderosos para Python. Ele simplifica a escrita de testes, desde os mais simples até os mais complexos.

## 1. O que é o Pytest?

Pytest é um framework que permite escrever testes de forma mais simples e "Pythônica". Suas principais vantagens são:
- **Sintaxe Simples:** Usa a palavra-chave `assert` nativa do Python, sem a necessidade de aprender novos métodos de asserção.
- **Descoberta Automática:** Encontra e executa automaticamente os testes no seu projeto.
- **Fixtures Poderosas:** Um sistema de injeção de dependências que facilita o gerenciamento do estado e da configuração dos testes (setup/teardown).
- **Ecossistema de Plugins:** Milhares de plugins que estendem suas funcionalidades (ex: `pytest-django`, `pytest-playwright`, `pytest-cov` para cobertura de código).
- **Relatórios Detalhados:** Fornece informações claras sobre falhas em asserções.

## 2. Instalação

Para começar, instale o `pytest` usando `pip`. É altamente recomendado fazer isso em um ambiente virtual.

```sh
pip install pytest
```

## 3. Escrevendo seu Primeiro Teste

O `pytest` descobre testes automaticamente seguindo convenções de nomenclatura:
- **Arquivos:** Devem começar com `test_` ou terminar com `_test.py`.
- **Funções:** Devem começar com `test_`.
- **Classes:** Devem começar com `Test`.

#### Passo a Passo

1.  **Crie uma função para testar:**
    Vamos criar um arquivo chamado `calculadora.py` com funções simples.

    ````python
    # filepath: calculadora.py
    def somar(a, b):
        """Soma dois números."""
        return a + b

    def subtrair(a, b):
        """Subtrai dois números."""
        return a - b
    ````

2.  **Crie o arquivo de teste:**
    Agora, crie um arquivo chamado `test_calculadora.py` no mesmo diretório.

    ````python
    # filepath: test_calculadora.py
    from calculadora import somar, subtrair

    def test_somar():
        """Testa a função de soma com números positivos."""
        assert somar(2, 3) == 5
        assert somar(10, 10) == 20

    def test_subtrair():
        """Testa a função de subtração."""
        assert subtrair(10, 5) == 5
    ````
    **O que fizemos?**
    - Importamos as funções que queríamos testar.
    - Criamos funções de teste começando com `test_`.
    - Usamos `assert` para verificar se o resultado da função é o esperado. Se a condição do `assert` for `False`, o teste falha.

## 4. Executando os Testes

Abra o terminal na raiz do seu projeto e simplesmente execute o comando:

```sh
pytest
```

O `pytest` irá procurar por arquivos e funções que sigam a convenção e executá-los. A saída será algo como:

```
============================= test session starts ==============================
platform win32 -- Python 3.11.1, pytest-8.2.2, pluggy-1.5.0
rootdir: d:\github-projects\automation_playwright_python
collected 2 items

test_calculadora.py ..                                                   [100%]

============================== 2 passed in 0.01s ===============================
```
- `..` indica que dois testes passaram com sucesso.
- Se um teste falhar, você verá um `F` e um relatório detalhado do erro.

## 5. Fixtures: Gerenciando Estado e Dependências

Fixtures são a funcionalidade mais poderosa do `pytest`. Elas são usadas para fornecer dados, objetos ou qualquer tipo de configuração para seus testes.

#### Exemplo: Fornecendo Dados

Imagine que você precisa de um conjunto de dados para vários testes. Em vez de recriá-lo em cada função, você pode usar uma fixture.

1.  **Crie uma fixture:**
    Use o decorador `@pytest.fixture` para definir uma fixture.

    ````python
    # filepath: test_dados.py
    import pytest

    @pytest.fixture
    def dados_iniciais():
        """Fixture que retorna um dicionário de exemplo."""
        print("\n(SETUP) Criando dicionário...")
        return {"nome": "Ana", "idade": 30}

    def test_verificar_nome(dados_iniciais):
        """Testa se o nome no dicionário está correto."""
        assert dados_iniciais["nome"] == "Ana"

    def test_verificar_idade(dados_iniciais):
        """Testa se a idade é um número inteiro."""
        assert isinstance(dados_iniciais["idade"], int)
    ````
    **O que fizemos?**
    - A função `dados_iniciais` é uma fixture. O que ela retorna é injetado nos testes.
    - As funções de teste `test_verificar_nome` e `test_verificar_idade` recebem `dados_iniciais` como um argumento. O `pytest` identifica que é uma fixture e a executa.

2.  **Execute com a flag `-s`** para ver os `prints`:
    ```sh
    pytest -s
    ```
    Você verá que a mensagem de "SETUP" aparece antes de cada teste, pois o escopo padrão de uma fixture é `function`.

#### Fixtures com Setup e Teardown (Configuração e Desmontagem)

Fixtures são ideais para ações que precisam ser feitas antes e depois de um teste, como conectar a um banco de dados ou limpar arquivos.

```python
@pytest.fixture
def cliente_db():
    """Fixture para conectar e desconectar de um DB."""
    print("\n(SETUP) Conectando ao banco de dados...")
    db = conectar_ao_db()
    
    yield db  # O teste é executado aqui
    
    print("\n(TEARDOWN) Desconectando do banco de dados...")
    db.desconectar()
```
- O código antes do `yield` é o **setup**.
- O código depois do `yield` é o **teardown** (desmontagem), que é executado mesmo se o teste falhar.

## 6. Marcadores (Markers): Agrupando e Pulando Testes

Marcadores são usados para categorizar seus testes.

-   `@pytest.mark.skip`: Para pular um teste incondicionalmente.
-   `@pytest.mark.skipif`: Para pular um teste se uma condição for verdadeira.
-   `@pytest.mark.xfail`: Para marcar um teste que você espera que falhe.
-   **Marcadores personalizados:** Para agrupar testes (ex: `slow`, `smoke`, `api`).

#### Exemplo de Marcadores

````python
# filepath: test_marcadores.py
import pytest
import sys

@pytest.mark.smoke
def test_funcionalidade_essencial():
    assert True

@pytest.mark.slow
def test_funcionalidade_lenta():
    import time
    time.sleep(2)
    assert True

@pytest.mark.skip(reason="Funcionalidade ainda não implementada.")
def test_funcionalidade_futura():
    assert False

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requer Python 3.10+")
def test_funcionalidade_python10():
    # Lógica específica para Python 3.10+
    assert True

@pytest.mark.xfail(reason="Bug conhecido #123")
def test_com_bug_conhecido():
    assert 1 == 2
```

## 7. Executando Testes em Paralelo com `pytest-xdist`

Para acelerar a execução da sua suíte de testes, especialmente em projetos grandes, você pode rodar os testes em paralelo. O plugin `pytest-xdist` é a ferramenta perfeita para isso, distribuindo os testes entre múltiplos processos.

#### O que é o `pytest-xdist`?

É um plugin para o `pytest` que estende suas funcionalidades, permitindo que os testes sejam distribuídos por múltiplos processos ou até mesmo máquinas remotas. A forma mais comum de uso é para paralelizar a execução em uma única máquina, utilizando vários núcleos de CPU.

#### Passo a Passo

1.  **Instalação:**
    Primeiro, instale o plugin. (Nota: ele já está listado no arquivo `requirements.txt` deste projeto).

    ```sh
    pip install pytest-xdist
    ```

2.  **Executando em Paralelo:**
    Para executar seus testes usando múltiplos processos, use a flag `-n` (ou `--numprocesses`).

    *   **Especificando o número de processos:**
        Se você quiser usar, por exemplo, 4 processos, execute:

        ```sh
        pytest -n 4
        ```

    *   **Usando o número de CPUs disponíveis:**
        Para que o `pytest-xdist` utilize automaticamente o número de núcleos de CPU disponíveis na sua máquina, use `auto`:

        ```sh
        pytest -n auto
        ```

#### Exemplo Prático

Vamos usar o arquivo `test_marcadores.py` que criamos anteriormente. Ele contém um teste lento (`test_funcionalidade_lenta`) que leva 2 segundos. Se executarmos os testes em paralelo, o tempo total da suíte deve ser menor.

1.  **Execute os testes com 2 processos:**

    ```sh
    pytest test_marcadores.py -n 2
    ```

2.  **Analisando a Saída:**
    A saída será um pouco diferente. O `pytest-xdist` atribui cada teste a um "worker" (trabalhador). Você notará que, embora o teste lento demore 2 segundos, o tempo total da execução será próximo a 2 segundos, pois os outros testes rodam em paralelo em outro processo.

    ```
    ============================= test session starts ==============================
    platform win32 -- Python 3.11.1, pytest-8.2.2, pluggy-1.5.0
    rootdir: d:\github-projects\automation_playwright_python
    plugins: xdist-3.8.0, ...
    gw0 [4] / gw1 [4]
    ....                                                                     [100%]
    ================== 4 passed, 1 skipped, 1 xfailed in 2.05s ===================
    ```
    - `gw0` e `gw1` representam os dois "gateways" ou workers.
    - O tempo total de execução é significativamente menor do que seria em modo sequencial.

> **Importante:** Para que os testes possam ser executados em paralelo sem problemas, eles devem ser independentes uns dos outros. Evite testes que dependam de estado compartilhado ou da ordem de execução, pois isso pode levar a resultados inconsistentes (`flaky tests`).