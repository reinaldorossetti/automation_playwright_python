from playwright.sync_api import Page, expect
import pytest

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,  # Set headless to False
    }

def test_app(page: Page):
    page.goto("https://bootswatch.com/default")
    
    default_checkbox = page.get_by_label("Default checkbox")
    checked_checkbox = page.get_by_label("Checked checkbox")

    # expect checked
    expect(checked_checkbox).to_be_checked()

    # expect unchecked
    expect(default_checkbox).not_to_be_checked()