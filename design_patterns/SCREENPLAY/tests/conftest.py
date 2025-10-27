import pytest
from actors.actor import Actor


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    # Arrange - Preparar o ator
    return Actor().web_perform(browser_type_launch_args)