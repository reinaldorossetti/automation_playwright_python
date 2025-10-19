### 1. Explique a diferença entre `page.locator()` e `page.query_selector()` no Playwright.

**Resposta:**

-   `page.locator()`: É a abordagem moderna e recomendada que retorna um objeto `Locator`. Os localizadores são estritos por padrão, aguardam automaticamente os elementos e suportam novas tentativas. Eles não resolvem o elemento imediatamente, mas esperam até que uma ação seja executada.
-   `page.query_selector()`: É a API legada `ElementHandle` que consulta o DOM imediatamente e retorna um `ElementHandle`. Não possui capacidade de espera automática e pode levar a testes instáveis.

**Exemplo em Python:**

````python
# Abordagem recomendada
page.locator('button').click()

# Abordagem legada (não recomendada)
button = page.query_selector('button')
if button:
    button.click()
`````
4. Como você lida com vários contextos de navegador no Playwright e por que os usaria?

**Resposta:** Contextos de navegador no Playwright são sessões isoladas, semelhantes ao modo incógnito, dentro de uma instância do navegador. Cada contexto possui seus próprios cookies, cache e armazenamento local.

**Exemplo em Python:**

````python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context1 = browser.new_context()
    context2 = browser.new_context()
    
    page1 = context1.new_page()
    page2 = context2.new_page()
    
    page1.goto('https://example.com')
    page2.goto('https://example.com')
    
    browser.close()
`````
Casos de uso incluem:

-   Testar cenários de múltiplos usuários simultaneamente
-   Isolar dados de teste entre testes
-   Testar diferentes permissões ou funções de usuário
-   Simular diferentes dispositivos ou viewports
-   Melhorar o desempenho do teste reutilizando instâncias do navegador
5. Quais são os diferentes tipos de localizadores no Playwright e quando você deve usar cada um?

**Resposta:** O Playwright suporta várias estratégias de localizador:

-   Localizadores de texto: Melhor para texto visível
-   Localizadores de função: Melhor para testes de acessibilidade
-   Localizadores de rótulo: Para entradas de formulário com rótulos
-   Localizadores de espaço reservado: Para entradas com espaços reservados
-   Localizadores de ID de teste: Mais confiáveis para testes
-   Seletores CSS: Para seleções complexas
-   XPath: Para travessia complexa do DOM

**Exemplo em Python:**

````python
# Localizadores de texto
page.get_by_text('Submit').click()

# Localizadores de função
page.get_by_role('button', name='Submit').click()

# Localizadores de rótulo
page.get_by_label('Email').fill('test@example.com')

# Localizadores de espaço reservado
page.get_by_placeholder('Enter email').fill('test@example.com')

# Localizadores de ID de teste
page.get_by_test_id('submit-btn').click()

# Seletores CSS
page.locator('.submit-button').click()

# XPath
page.locator('xpath=//button[@type="submit"]').click()
`````
A melhor prática é preferir atributos voltados para o usuário (papel, texto, rótulo) em vez de detalhes de implementação (classes CSS, IDs).
6. Como você implementa o Page Object Model (POM) no Playwright?

**Resposta:** O Page Object Model é um padrão de design que cria um repositório de objetos para elementos da web.

**Exemplo em Python:**

````python
# pages/login_page.py
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.email_input = page.get_by_label('Email')
        self.password_input = page.get_by_label('Password')
        self.submit_button = page.get_by_role('button', name='Login')
    
    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
    
    def goto(self):
        self.page.goto('/login')

# arquivo de teste
import pytest
from pages.login_page import LoginPage

def test_user_can_login(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login('user@example.com', 'password123')
`````
7. Qual é o propósito do `playwright.config` e quais são algumas configurações importantes?

**Resposta:** O arquivo de configuração é o local central para as configurações dos testes do Playwright.

**Exemplo em Python (pytest.ini ou conftest.py):**

````python
# conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "base_url": "http://localhost:3000",
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": True,
    }

# pytest.ini
[pytest]
testpaths = tests
addopts = 
    --browser chromium
    --browser firefox
    --browser webkit
    --screenshot only-on-failure
    --video retain-on-failure
    --tracing on
`````
As principais configurações controlam a execução dos testes, as configurações do navegador, capturas de tela, vídeos, rastros, execução paralela e testes entre navegadores.
8. Como você lida com uploads e downloads de arquivos no Playwright?

**Resposta:**

**Exemplo em Python:**

````python
# Upload de Arquivo
page.set_input_files('input[type="file"]', 'path/to/file.pdf')

# Vários arquivos
page.set_input_files('input[type="file"]', [
    'file1.pdf',
    'file2.pdf'
])

# Usando o evento do seletor de arquivos
with page.expect_file_chooser() as fc_info:
    page.click('button#upload')
file_chooser = fc_info.value
file_chooser.set_files('file.pdf')

# Download de Arquivo
with page.expect_download() as download_info:
    page.click('a#download-link')
download = download_info.value

download.save_as('/path/to/save/file.pdf')
`````
9. Explique como realizar testes de API com Playwright.

**Resposta:** O Playwright inclui recursos de teste de API integrados.

**Exemplo em Python:**

````python
import pytest
from playwright.sync_api import APIRequestContext

def test_api_example(playwright):
    # Criar contexto de requisição API
    request_context = playwright.request.new_context(
        base_url='https://api.example.com'
    )
    
    # Requisição GET
    response = request_context.get('/users')
    assert response.ok
    assert response.status == 200
    
    data = response.json()
    assert len(data) == 10
    
    # Requisição POST
    new_user = request_context.post('/users', data={
        'name': 'John Doe',
        'email': 'john@example.com'
    })
    assert new_user.ok
    
    # Usando autenticação
    auth_context = playwright.request.new_context(
        extra_http_headers={
            'Authorization': 'Bearer token123'
        }
    )
    
    request_context.dispose()
    auth_context.dispose()
`````
10. Como você lida com autenticação e gerenciamento de sessão nos testes do Playwright?

**Resposta:** Existem várias abordagens para lidar com autenticação.

**Exemplo em Python:**

````python
# conftest.py
import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="session")
def authenticated_state(playwright, browser_type):
    browser = browser_type.launch()
    context = browser.new_context()
    page = context.new_page()
    
    # Realizar login
    page.goto('/login')
    page.fill('#email', 'user@example.com')
    page.fill('#password', 'password')
    page.click('button[type="submit"]')
    
    # Salvar estado da storage
    context.storage_state(path='auth.json')
    
    context.close()
    browser.close()

@pytest.fixture
def authenticated_page(context):
    # Carregar estado da storage
    context = browser.new_context(storage_state='auth.json')
    page = context.new_page()
    yield page
    context.close()

# Usando fixture nos testes
def test_with_auth(authenticated_page):
    authenticated_page.goto('/dashboard')
    # Lógica do teste aqui

# Usando fixture de configuração
@pytest.fixture(autouse=True)
def setup_login(page: Page):
    page.goto('/login')
    page.fill('#email', 'user@example.com')
    page.fill('#password', 'password')
    page.click('button[type="submit"]')
`````
11. O que são fixtures no Playwright e como você cria fixtures personalizadas?

**Resposta:** Fixtures fornecem uma maneira de estabelecer ambientes de teste confiáveis com lógica de configuração e desmontagem.

**Exemplo em Python:**

````python
# conftest.py
import pytest
from playwright.sync_api import Page

@pytest.fixture
def authenticated_page(page: Page):
    """Fixture que fornece uma página autenticada"""
    page.goto('/login')
    page.fill('#email', 'user@example.com')
    page.fill('#password', 'password')
    page.click('button[type="submit"]')
    yield page

@pytest.fixture
def database():
    """Fixture que fornece conexão com o banco de dados"""
    db = connect_to_database()
    yield db
    db.close()

@pytest.fixture
def test_user(database):
    """Fixture que cria um usuário de teste"""
    user = database.create_user({
        'email': 'test@example.com',
        'name': 'Test User'
    })
    yield user
    database.delete_user(user.id)

# Usando fixtures nos testes
def test_with_auth(authenticated_page):
    authenticated_page.goto('/dashboard')
    # Lógica do teste aqui

def test_with_user(page, test_user):
    page.goto(f'/users/{test_user.id}')
    # Lógica do teste aqui
`````
12. Como você depura testes no Playwright?

**Resposta:** O Playwright oferece várias opções de depuração.

**Exemplo em Python:**

````python
# Executar com flag de depuração
# pytest --headed --slowmo 1000

# Pausar execução
page.pause()

# Modo lento
browser = playwright.chromium.launch(slow_mo=1000)

# Capturas de tela
page.screenshot(path='screenshot.png')

# Logs de console
page.on('console', lambda msg: print(msg.text))

# Usando debugger
import pdb; pdb.set_trace()

# Modo com cabeçalho para depuração
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": False,
        "slow_mo": 1000,
    }
`````
Comandos comuns de depuração:

```bash
# JavaScript
npx playwright test --debug
npx playwright test --headed
npx playwright test --headed --slowmo 1000
npx playwright show-trace trace.zip

# Python
pytest --headed --slowmo 1000
pytest --browser chromium --headed
playwright show-trace trace.zip
```
13. Explique como lidar com iframes no Playwright.

**Resposta:** O Playwright fornece várias maneiras de interagir com iframes.

**Exemplo em Python:**

````python
# Método 1: Usando frame_locator (Recomendado)
frame = page.frame_locator('iframe#myframe')
frame.locator('button').click()

# Método 2: Usando método frame()
frame = page.frame(name='frameName')
frame.click('button')

# Ou por URL
frame = page.frame(url=lambda url: 'domain.com' in url)

# Método 3: Iframes aninhados
parent_frame = page.frame_locator('iframe#parent')
child_frame = parent_frame.frame_locator('iframe#child')
child_frame.locator('input').fill('text')

# Aguardando o iframe carregar
page.wait_for_load_state('networkidle')
frame = page.frame_locator('iframe')
frame.locator('button').wait_for()

# Obtendo todos os frames
frames = page.frames
for frame in frames:
    print(frame.url)
`````
14. Como você realiza testes de regressão visual com Playwright?

**Resposta:** O Playwright possui recursos integrados de comparação visual.

**Exemplo em Python:**

````python
import pytest
from playwright.sync_api import Page, expect

def test_visual_regression(page: Page):
    page.goto('https://example.com')
    
    # Comparação de captura de tela da página inteira
    expect(page).to_have_screenshot('homepage.png')
    
    # Comparação de captura de tela de elemento
    element = page.locator('.header')
    expect(element).to_have_screenshot('header.png')
    
    # Com opções
    expect(page).to_have_screenshot(
        'homepage.png',
        max_diff_pixels=100,
        threshold=0.2,
        full_page=True
    )
    
    # Máscara de conteúdo dinâmico
    expect(page).to_have_screenshot(
        mask=[page.locator('.dynamic-content')]
    )

# Atualizar capturas de tela de referência
# pytest --update-snapshots
`````
15. Qual é a diferença entre `test.describe()`, `test.beforeEach()` e `test.afterEach()`?

**Resposta:** Esses métodos ajudam a organizar e estruturar os testes.

**Exemplo em Python:**

````python
import pytest
from playwright.sync_api import Page

class TestUserAuthentication:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self):
        """Executa uma vez antes de todos os testes nesta classe"""
        print('Configurando suíte de teste')
        yield
        print('Limpando suíte de teste')
    
    @pytest.fixture(autouse=True)
    def setup_method(self, page: Page):
        """Executa antes de cada teste"""
        page.goto('/login')
        yield
        # Teardown após cada teste
        page.context.clear_cookies()
    
    def test_should_login_successfully(self, page: Page):
        # Lógica do teste
        pass
    
    def test_should_show_error_on_invalid_credentials(self, page: Page):
        # Lógica do teste
        pass

# Alternativa usando fixtures em nível de módulo
@pytest.fixture(scope="module", autouse=True)
def setup_module():
    """Executa uma vez antes de todos os testes no módulo"""
    print('Configurando módulo')
    yield
    print('Limpando módulo')

@pytest.fixture(autouse=True)
def setup_function(page: Page):
    """Executa antes de cada função de teste"""
    page.goto('/login')
`````
16. Como você lida com requisições e respostas de rede no Playwright?

**Resposta:** O Playwright fornece poderosas capacidades de interceptação de rede.

**Exemplo em Python:**

````python
# Bloquear imagens
page.route('**/*.{png,jpg,jpeg}', lambda route: route.abort())

# Modificar requisição
def handle_route(route):
    headers = route.request.headers
    headers['Authorization'] = 'Bearer token123'
    route.continue_(headers=headers)

page.route('**/api/users', handle_route)

# Resposta de API simulada
def mock_api(route):
    route.fulfill(
        status=200,
        content_type='application/json',
        body='[{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]'
    )

page.route('**/api/users', mock_api)

# Aguardando requisições de rede
with page.expect_response('**/api/users') as response_info:
    page.click('button#load-users')
response = response_info.value

data = response.json()

# Escutando eventos de rede
page.on('request', lambda request: 
    print('>>', request.method, request.url)
)

page.on('response', lambda response: 
    print('<<', response.status, response.url)
)

# Exemplo mais complexo com gerenciador de contexto
from playwright.sync_api import Route

def handle_api_route(route: Route):
    if 'POST' in route.request.method:
        route.fulfill(
            status=201,
            body='{"success": true}'
        )
    else:
        route.continue_()

page.route('**/api/**', handle_api_route)
`````
17. Explique o mecanismo de nova tentativa de teste do Playwright e quando você deve usá-lo.

**Resposta:** O Playwright suporta novas tentativas automáticas de teste para lidar com testes instáveis.

**Exemplo em Python (pytest.ini):**

````ini
[pytest]
addopts = --maxfail=1 --reruns=2 --reruns-delay=1
`````
Quando usar novas tentativas:

-   Em ambientes CI/CD onde as condições de rede variam
-   Para testes que falham ocasionalmente devido a problemas de temporização
-   Ao testar em ambientes instáveis
-   NÃO deve ser usado para mascarar testes mal escritos

### Como você lida com testes móveis e emulação de dispositivos no Playwright?

**Resposta:** O Playwright fornece amplas capacidades de teste móvel.

**Exemplo em Python:**

````python
import pytest
from playwright.sync_api import Page, Browser

# Usando dispositivos predefinidos
@pytest.fixture
def iphone_context(browser: Browser):
    iphone_13 = playwright.devices['iPhone 13 Pro']
    context = browser.new_context(**iphone_13)
    yield context
    context.close()

def test_mobile(iphone_context):
    page = iphone_context.new_page()
    page.goto('https://example.com')
    # Testar na viewport do iPhone 13 Pro

# Configuração de dispositivo personalizada
@pytest.fixture
def custom_mobile_context(browser: Browser):
    context = browser.new_context(
        viewport={'width': 375, 'height': 667},
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
        has_touch=True,
        is_mobile=True,
        device_scale_factor=2,
        geolocation={'longitude': -122.4194, 'latitude': 37.7749},
        permissions=['geolocation']
    )
    yield context
    context.close()

# Testando vários dispositivos
@pytest.mark.parametrize('device_name', [
    'iPhone 13 Pro',
    'Pixel 5',
    'iPad Pro'
])
def test_on_multiple_devices(browser: Browser, device_name: str):
    device = playwright.devices[device_name]
    context = browser.new_context(**device)
    page = context.new_page()
    page.goto('https://example.com')
    # Lógica do teste
    context.close()

# Ações de toque
def test_touch_actions(page: Page):
    page.locator('button').tap()
    page.touchscreen.tap(100, 200)

# Teste de geolocalização
def test_geolocation(context):
    context.set_geolocation({'longitude': -122.4194, 'latitude': 37.7749})
    context.grant_permissions(['geolocation'])
    page = context.new_page()
    page.goto('https://example.com/map')
`````
19. Quais são as melhores práticas para escrever testes Playwright manuteníveis?

**JavaScript Melhores Práticas:**

```javascript
// 1. Use localizadores voltados para o usuário
// Bom
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByLabel('Email').fill('test@example.com');

// Evitar
await page.locator('#btn-123').click();

// 2. Implemente o Page Object Model
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Login' });
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// 3. Evite esperas explícitas
// Ruim
await page.waitForTimeout(5000);

// Bom
await page.waitForLoadState('networkidle');
await page.locator('button').waitFor();

// 4. Use nomes de teste significativos
test('should display error when email is invalid', async ({ page }) => {
  // Clareza sobre o que o teste faz
});

// 5. Mantenha os testes independentes
test.beforeEach(async ({ page }) => {
  // Redefinir estado antes de cada teste
  await page.goto('/');
});

// 6. Use fixtures para configuração comum
const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    // Configuração
    await page.goto('/login');
    await page.fill('#email', 'user@example.com');
    await page.fill('#password', 'password');
    await page.click('button[type="submit"]');
    await use(page);
    // Teardown acontece automaticamente
  }
});
```python
# 1. Use localizadores voltados para o usuário
# Bom
page.get_by_role('button', name='Submit').click()
page.get_by_label('Email').fill('test@example.com')

# Evitar
page.locator('#btn-123').click()

# 2. Implemente o Page Object Model
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.email_input = page.get_by_label('Email')
        self.password_input = page.get_by_label('Password')
        self.submit_button = page.get_by_role('button', name='Login')
    
    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

# 3. Evite esperas explícitas
# Ruim
import time
time.sleep(5)

# Bom
page.wait_for_load_state('networkidle')
page.locator('button').wait_for()

# 4. Use nomes de teste significativos
def test_should_display_error_when_email_is_invalid(page):
    # Clareza sobre o que o teste faz
    pass

# 5. Mantenha os testes independentes
@pytest.fixture(autouse=True)
def setup(page):
    # Redefinir estado antes de cada teste
    page.goto('/')

# 6. Use fixtures para configuração comum
@pytest.fixture
def authenticated_page(page):
    """Fornece uma página autenticada"""
    page.goto('/login')
    page.fill('#email', 'user@example.com')
    page.fill('#password', 'password')
    page.click('button[type="submit"]')
    yield page

# 7. Use dicas de tipo
from playwright.sync_api import Page, expect

def test_example(page: Page) -> None:
    page.goto('https://example.com')
    expect(page).to_have_title('Example Domain')

# 8. Organize os testes em classes
class TestUserAuthentication:
    def test_successful_login(self, page: Page):
        pass
    
    def test_failed_login(self, page: Page):
        pass
```yaml
name: Playwright Tests
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - uses: actions/setup-node@v3
      with:
        node-version: 18
        
    - name: Install dependencies
      run: npm ci
      
    - name: Install Playwright Browsers
      run: npx playwright install --with-deps
      
    - name: Run Playwright tests
      run: npx playwright test
      
    - uses: actions/upload-artifact@v3
      if: always()
      with:
        name: playwright-report
        path: playwright-report/
        retention-days: 30
```yaml
name: Playwright Tests
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Install Playwright Browsers
      run: playwright install --with-deps
      
    - name: Run Playwright tests
      run: pytest --browser chromium --browser firefox --browser webkit
      
    - uses: actions/upload-artifact@v3
      if: always()
      with:
        name: playwright-report
        path: test-results/
        retention-days: 30
        
```dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

CMD ["npx", "playwright", "test"]
```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.40.0-focal

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["pytest"]
```groovy
pipeline {
    agent any
    
    stages {
        stage('Install') {
            steps {
                sh 'npm ci'  // or: sh 'pip install -r requirements.txt'
                sh 'npx playwright install --with-deps'  // or: sh 'playwright install --with-deps'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npx playwright test'  // or: sh 'pytest'
            }
        }
    }
    
    post {
        always {
            publishHTML([
                reportDir: 'playwright-report',  // or: 'test-results'
                reportFiles: 'index.html',
                reportName: 'Playwright Report'
            ])
        }
    }
}
```yaml
image: mcr.microsoft.com/playwright:v1.40.0-focal

stages:
  - test

playwright-tests:
  stage: test
  script:
    - npm ci
    - npx playwright install --with-deps
    - npx playwright test
  artifacts:
    when: always
    paths:
      - playwright-report/
    expire_in: 30 days
```yaml
image: mcr.microsoft.com/playwright/python:v1.40.0-focal

stages:
  - test

playwright-tests:
  stage: test
  script:
    - pip install -r requirements.txt
    - playwright install --with-deps
    - pytest
  artifacts:
    when: always
    paths:
      - test-results/
    expire_in: 30 days
```