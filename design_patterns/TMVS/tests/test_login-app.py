from controllers.controller_pages import ControllerPages
from playwright.sync_api import Page, expect

def test_successful_login(page: Page):
    username = "dan"
    password = "pwd"

    login_page = ControllerPages(page)

    login_page.login(username, password)

    expect(login_page.login_data.label).to_have_text(
        f"Welcome, {username}!"
        )


def test_failed_login(page: Page):
    username = "dan"
    password = "cnasdjc"

    login_page = ControllerPages(page)

    login_page.login(username, password)

    expect(login_page.login_data.label).to_have_text(
        "Invalid username/password"
    )