from playwright.sync_api import Page, Locator
from models.login_data import LoginPageData
from models.search_data import SearchData


class ControllerPages:

    def __init__(self, page: Page):
        self.page = page
        self.login_data = None
        self.search_data = None

    def login(self, username, password):
        self.login_data = LoginPageData(self.page)
        self.login_data.username_input.fill(username)
        self.login_data.password_input.fill(password)
        self.login_data.login_btn.click()

    def visit_docs(self):
        self.search_data = SearchData(self.page)
        self.search_data.docs_link.click()

    def search(self, query):
        self.search_data = SearchData(self.page)
        self.page.keyboard.press("Control+KeyK")
        self.search_data.search_input.fill(query)

    def search_results(self) -> Locator:
        print("Search Results:")
        for result in self.page.locator("span.DocSearch-Hit-title").all():
            print(result.inner_text())
        return self.page.locator("div.DocSearch-Dropdown")