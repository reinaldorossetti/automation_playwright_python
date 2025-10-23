from controllers.controller_pages import ControllerPages
from playwright.sync_api import Page, expect

def test_docs_link(page: Page):
    """
    Testa a navegação para a página de documentação do Playwright.
    
    Cenário: Acesso direto à documentação
    
    Passos executados:
    1. Executa o método visit_docs() para navegar até a página de documentação
    2. Verifica se a URL corresponde à página de introdução da documentação

    Resultado esperado:
    - A URL da página deve ser: "https://playwright.dev/python/docs/intro"
    - A página de introdução da documentação deve ser carregada corretamente
    
    Pré-condições:
    - Site do Playwright deve estar acessível
    """
    pages = ControllerPages(page)
    pages.visit_docs()

    expect(page).to_have_url(
        "https://playwright.dev/python/docs/intro"
    )

def test_docs_search(page: Page):
    """
    Testa a funcionalidade de busca na documentação do Playwright.
    
    Cenário: Busca por termo específico na documentação
    
    Passos executados:
    1. Executa o método search() passando o termo "assertions"
    2. Aguarda o carregamento dos resultados da pesquisa
    3. Verifica se os resultados contêm o texto esperado relacionado a assertions
    
    Resultado esperado:
    - Os resultados da busca devem conter o texto: "List of assertions"
    - A página de resultados deve exibir conteúdo relevante sobre assertions
    
    Pré-condições:
    - Funcionalidade de busca deve estar operacional
    """
    pages = ControllerPages(page)
    pages.search("assertions")
    expect(pages.search_results()).to_contain_text(
        "List of assertions"
    )