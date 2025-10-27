from playwright.sync_api import Page


class LoginTask:

    def __init__(self, page: Page):
        self.page = page

    def acessar_pagina_login(self):
        self.page.goto("http://uitestingplayground.com/sampleapp")
    
    def fechar_pagina(self):
        self.page.close()

    def realizar_login(self, username: str, password: str):
        username_input = self.page.get_by_placeholder("User Name")
        password_input = self.page.locator("input[name=\"Password\"]")
        login_btn = self.page.get_by_role("button", name="Log In")

        username_input.fill(username)
        password_input.fill(password)
        login_btn.click()