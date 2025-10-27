import pytest
from playwright.sync_api import Page
from actors.actor import prepare_actor_login_task, prepare_actor_login_question


@pytest.mark.usefixtures("browser_type_launch_args")
def test_ct001_realizar_login_com_sucesso(page: Page):
    # Arrange - Preparar o ator
    login_task = prepare_actor_login_task(page)
    login_question = prepare_actor_login_question(page)

    # Act - Executar as ações como tasks
    login_task.acessar_pagina_login()

    # Act - Executar as ações como tasks
    login_task.realizar_login("dan", "pwd")

    # Question - Verificar o resultado
    login_question.mensagem_de_boas_vindas("dan")

    # Cleanup - Fechar a página
    login_task.fechar_pagina()
