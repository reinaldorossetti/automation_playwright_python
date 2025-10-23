from dataclasses import dataclass
from playwright.sync_api import Page, Locator

@dataclass
class LoginPageData:
    username_input: Locator
    password_input: Locator
    login_btn: Locator
    label: Locator
    username = "dan"
    password = "cnasdjc"
    wrong_password = "wrong_password"

    def __init__(self, page: Page):
        page.goto("http://uitestingplayground.com/sampleapp")
        self.username_input = page.get_by_placeholder("User Name")
        self.password_input = page.get_by_placeholder("********")

        self.login_btn = page.get_by_role(
            "button", name="Log In"
        )

        self.label = page.locator("label#loginstatus")
