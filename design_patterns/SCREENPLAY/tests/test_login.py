import pytest
import allure
from playwright.sync_api import Page
from actors.actor import prepare_actor_login_task, prepare_actor_login_question


@allure.feature("Autenticação")
@allure.story("Login de Usuário")
@allure.title("CT001 - Realizar login com sucesso")
@allure.description("Verifica se o usuário consegue realizar login com credenciais válidas")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.usefixtures("browser_type_launch_args")
def test_ct001_realizar_login_com_sucesso(page: Page):
    with allure.step("# Arrange - Preparar o ator com suas habilidades"):
        login_task = prepare_actor_login_task(page)
        login_question = prepare_actor_login_question(page)

    with allure.step("# Act - Acessar a página de login"):
        login_task.acessar_pagina_login()

    with allure.step("# Act - Realizar login com usuário 'dan' e senha 'pwd'"):
        login_task.realizar_login("dan", "pwd")

    with allure.step("# Assert - Verificar mensagem de boas-vindas"):
        login_question.mensagem_de_boas_vindas("dan")

    with allure.step("# Cleanup - Fechar a página"):
        login_task.fechar_pagina()
