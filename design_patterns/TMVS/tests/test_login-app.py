from controllers.controller_pages import ControllerPages
from playwright.sync_api import Page, expect

def test_successful_login(page: Page):
    """
    Testa o login com credenciais válidas.
    
    Passos:
    1. Define username e password válidos
    2. Executa o método login() com as credenciais
    3. Verifica se o label exibe a mensagem de boas-vindas com o nome do usuário
    
    Resultado esperado: "Welcome, dan!"
    """

    login_page = ControllerPages(page)

    login_page.login(login_page.login_data.username, 
                     login_page.login_data.password)

    expect(login_page.login_data.label).to_have_text(
        f"Welcome, {login_page.login_data.username}!"
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
    login_page = ControllerPages(page)

    login_page.login(login_page.login_data.username, 
                     login_page.login_data.wrong_password)

    expect(login_page.login_data.label).to_have_text(
        "Invalid username/password"
    )