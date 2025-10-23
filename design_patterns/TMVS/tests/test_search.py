from controllers.controller_pages import ControllerPages
from playwright.sync_api import Page, expect

def test_docs_link(page: Page):
    pages = ControllerPages(page)
    pages.visit_docs()

    expect(page).to_have_url(
        "https://playwright.dev/python/docs/intro"
    )

def test_docs_search(page: Page):
    pages = ControllerPages(page)
    query = "assertions"
    pages.search(query)
    expect(pages.search_results()).to_contain_text(
        "List of assertions"
    )