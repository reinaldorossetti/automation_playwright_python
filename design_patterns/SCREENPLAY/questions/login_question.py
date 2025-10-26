from playwright.sync_api import Page, expect

class LoginQuestion:
    def __init__(self, page: Page):
        self.page = page

    def mensagem_de_boas_vindas(self, username: str):
        """Questão para verificar a mensagem de boas-vindas"""
        label = self.page.locator("label#loginstatus")
        expect(label).to_have_text(
            f"Welcome, {username}!"
        )
