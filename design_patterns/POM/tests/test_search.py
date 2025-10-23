from POM.pages.search_page import SearchPage
from playwright.sync_api import Page, expect


def test_docs_link(page: Page):
    homepage = SearchPage(page)
    homepage.visit_docs()

    expect(homepage.page).to_have_url(
        "https://playwright.dev/python/docs/intro"
    )

def test_docs_search(page: Page):
    query = "assertions"

    homepage = SearchPage(page)
    homepage.search(query)

    expect(homepage.search_results()).to_contain_text(
        "List of assertions"
    )