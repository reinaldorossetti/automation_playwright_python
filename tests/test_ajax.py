from playwright.sync_api import Page, expect
import pytest

# Configuração global para aumentar o timeout padrão das asserções do `expect`
expect.set_options(timeout=20_000)

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,  # Set headless to False
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "ignore_https_errors": True,  # Ignore HTTPS errors
    }

@pytest.fixture(scope="session")
def set_global_timeout(page: Page):
    """Define um timeout padrão para todas as ações da página (ex: click, fill)."""
    page.set_default_timeout(30_000)
    yield

def test_ajax(page: Page):
    page.goto("http://uitestingplayground.com/ajax")

    btn = page.get_by_role(
       "button", name="Button Triggering AJAX Request"
    )
    btn.click()
    paragraph = page.locator("p.bg-success")
    paragraph.wait_for()
    expect(paragraph).to_be_visible()
    expect(page.get_by_text("Data loaded with AJAX get request.")).to_be_visible()