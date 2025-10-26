import pytest
from tasks.login_task import LoginTask
from questions.login_question import LoginQuestion
from playwright.sync_api import Page

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,  # Set headless to False
    }

def test_login_com_sucesso(page: Page):
    # Arrange - Preparar o ator
    login_task = LoginTask(page)
    login_question = LoginQuestion(page)

    # Act - Executar as ações como tasks
    login_task.acessar_pagina_login()
    login_task.realizar_login("dan", "pwd")

    # Question - Verificar o resultado
    login_question.mensagem_de_boas_vindas("dan")
    page.close()
