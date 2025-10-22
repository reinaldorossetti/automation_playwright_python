import pytest
from playwright.sync_api import Page, Browser, expect


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,
        "slow_mo": 500,
    }


# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args):
#     return {
#         **browser_context_args,
#         "storage_state": "auth/storage_state.json",
#     }


def test_page_has_docs_link(page: Page):
    page.goto("http://playwright.dev/python")

    docs_link = page.get_by_role("link", name="Docs")

    expect(docs_link).to_be_visible()


@pytest.mark.only_browser("chromium")
def test_visits_google_account(page: Page, browser: Browser):
    # create a new incognito browser context
    context = browser.new_context()
    # create a new page inside context.
    page = context.new_page()
    page.goto("https://accounts.google.com")
    page.screenshot(path="account.jpg")
    
    # Save the storage state to a file
    context.storage_state(path="auth/storage_state.json")

    # dispose context once it is no longer needed.
    context.close()