import pytest
import re
from playwright.sync_api import BrowserContext, Page, expect

DOCS_URL = "https://playwright.dev/python/docs/intro"

# Configuração global para aumentar o timeout padrão das asserções
expect.set_options(timeout=15_000)

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,  # Set headless to False
    }

def test_page_has_get_started_link(page: Page):
    """
    Teste original: Verifica se a página inicial tem um link "GET STARTED"
    e se ele redireciona para a URL de documentação correta.
    """
    page.goto("https://playwright.dev/python")

    # Localizador corrigido para evitar ambiguidade
    header = page.locator("header")
    link = header.get_by_role("link", name="GET STARTED")
    
    # Asserção de Atributo: Verifica se o link tem o atributo href esperado.
    expect(link).to_have_attribute("href", "/python/docs/intro")
    expect(page).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright Python")
   
    link.click()
    
    # Asserção de URL: Verifica se a URL da página é a esperada após o clique.
    expect(page).to_have_url(DOCS_URL)


def test_assertion_examples(page: Page):
    """
    Novo teste: Demonstra várias asserções do Playwright.
    """
    page.goto("https://playwright.dev/python")

    # 1. Asserção de Título: Verifica se o título da página contém um texto específico.
    expect(page).to_have_title(re.compile("Playwright"))

    # 2. Asserção de Visibilidade: Verifica se um elemento está visível na página.
    heading = page.get_by_role("heading", name="Playwright")
    expect(heading).to_be_visible()

    # 3. Asserção de Texto: Verifica se um elemento contém um texto exato.
    header = page.locator("header")
    header.get_by_role("link", name="GET STARTED").click()
    
    slogan = page.locator("#installing-playwright-pytest")
    expect(slogan).to_have_text("Installing Playwright Pytest")

    # 4. Asserção de Contagem: Verifica o número de elementos que correspondem a um localizador.
    # Neste caso, contamos os links de navegação principais.
    nav_links = page.locator(".dropdown__menu > li")
    expect(nav_links).to_have_count(4)

    # 5. Asserção de Classe CSS: Verifica se um elemento possui uma classe CSS específica.
    search_button = page.locator(".DocSearch-Button")
    expect(search_button).to_have_class(re.compile("DocSearch-Button"))

    # 6. Asserção de Habilitação: Verifica se um botão ou link está habilitado para interação.
    get_started_link = page.get_by_role("link", name="Community").first
    expect(get_started_link).to_be_enabled()

    # 7. Asserção de Conteúdo de Texto (parcial): Verifica se o elemento contém um pedaço de texto.
    footer = page.locator("footer.footer")
    expect(footer).to_contain_text("Copyright © 2025 Microsoft")

    # 8. Asserção de Valor de Input (to_have_value): Verifica o valor de um campo de input.
    # Clica no botão de busca para abrir o campo de input.
    search_button = page.locator(".DocSearch-Button")
    search_button.click()
    
    # Localiza o input de busca e digita um valor.
    search_input = page.locator("#docsearch-input")
    search_text = "assertions"
    search_input.fill(search_text)
    
    # Verifica se o input contém o valor digitado.
    expect(search_input).to_have_value(re.compile(search_text))
