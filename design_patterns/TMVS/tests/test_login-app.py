import pytest
from controllers.controller_pages import ControllerPages
from playwright.sync_api import Page, expect

# Configuração global para aumentar o timeout padrão das asserções
expect.set_options(timeout=15_000)

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,  # Set headless to False
    }

def test_successful_login(page: Page):
    """
    Testa o login com credenciais válidas.
    
    Passos:
    1. Define username e password válidos
    2. Executa o método login() com as credenciais
    3. Verifica se o label exibe a mensagem de boas-vindas com o nome do usuário
    
    Resultado esperado: "Welcome, dan!"
    """
    username = "dan"
    password = "pwd"
    login_page = ControllerPages(page)
    login_page.login(username, password)

    expect(login_page.login_data.label).to_have_text(
        f"Welcome, {username}!"
    )

def test_failed_login(page: Page):
    """
    Testa o login com credenciais inválidas.
    
    Passos:
    1. Define username válido mas password incorreto
    2. Executa o método login() com as credenciais inválidas
    3. Verifica se o label exibe a mensagem de erro

    Resultado esperado: "Invalid username/password"
    """
    pages = ControllerPages(page)
    pages.login("dan", "wrong_password")

    expect(pages.login_data.label).to_have_text(
        "Invalid username/password"
    )