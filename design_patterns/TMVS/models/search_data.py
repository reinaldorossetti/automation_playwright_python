from dataclasses import dataclass
from playwright.sync_api import Page, Locator

@dataclass
class SearchData:
    docs_link: Locator
    search_input: Locator

    def __init__(self, page: Page):
        page.goto("https://playwright.dev/python")
        self.docs_link = page.get_by_role("link", name="Docs")
        self.search_input = page.get_by_placeholder("Search docs")