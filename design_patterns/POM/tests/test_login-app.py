from POM.pages.login_page import LoginPage
from playwright.sync_api import Page, expect

def test_successful_login(page: Page):
    """
    Testa o login com credenciais válidas.
    
    Passos:
    1. Define username e password válidos
    2. Inicializa o ControllerPages com a página do Playwright
    3. Executa o método login() com as credenciais
    4. Verifica se o label exibe a mensagem de boas-vindas com o nome do usuário
    
    Resultado esperado: "Welcome, dan!"
    """
    username = "dan"
    password = "pwd"

    login_page = LoginPage(page)

    login_page.login(username, password)

    expect(login_page.label).to_have_text(
        f"Welcome, {username}!"
        )


def test_failed_login(page: Page):
    """
    Testa o login com credenciais inválidas.
    
    Passos:
    1. Define username válido mas password incorreto
    2. Inicializa o ControllerPages com a página do Playwright
    3. Executa o método login() com as credenciais inválidas
    4. Verifica se o label exibe a mensagem de erro
    
    Resultado esperado: "Invalid username/password"
    """
    username = "dan"
    password = "cnasdjc"

    login_page = LoginPage(page)

    login_page.login(username, password)

    expect(login_page.label).to_have_text(
        "Invalid username/password"
    )