# 🐳 Playwright com Docker e Paralelismo na Esteira de CI/CD: Guia Completo para QA 🚀

## 📜 Introdução ao paralelismo nos testes.

O `Dockerfile` é a sua porta de entrada para rodar scripts do Playwright em um ambiente Dockerizado! 📦 Essa imagem já vem com os navegadores do Playwright e todas as dependências de sistema necessárias.

Para realizar o Paralelismo de testes com múltiplos navegadores, usamos o "pytest -n" ou "pytest --numprocesses auto" do pacote `pytest-xdist`, você também pode especificar um valor fixo de processos "pytest -n 4" ou "pytest --numprocesses 4". Isso por que estamos usando o Python como linguagem de automação.

No caso do Node.js, o paralelismo é gerenciado nativamente pelo Playwright Test Runner.
Exemplo de comando para rodar 4 workers no Node.js:
```
npx playwright test --workers 4
```
Para desativar o paralelismo, use `--workers=1`.
```
npx playwright test --workers=1
```

Para configurar o número de workers no CI, sem usar ele no comando acima, adicione a seguinte configuração no seu arquivo de configuração do Playwright:

```typescript

playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  // Limit the number of workers on CI, use default locally
  workers: process.env.CI ? 2 : undefined,
});
```

Projeto: https://github.com/reinaldorossetti/automation_playwright_python/tree/main  
 já está configurado para rodar com paralelismo no CI/CD usando GitHub Actions, confira o arquivo `.github/workflows/playwright_docker.yml`.  


## 🛠️ Como Usar

A imagem Docker oficial é publicada no **Microsoft Artifact Registry**.

> ℹ️ **Info:** Essa imagem Docker destina-se **apenas** para fins de desenvolvimento e testes. ⚠️ **Não é recomendado** usá-la para visitar sites não confiáveis.

Podemos consultar as imagens disponíveis no [Microsoft Container Registry](https://mcr.microsoft.com/en-us/artifact/mar/playwright/tags).

### 📥 Baixando a Imagem (Pull)  
A versão mais atual é a `v1.57.0` (Junho de 2024). Substitua pela versão desejada conforme necessário. Mas isso pode mudar com o tempo, então sempre verifique a [página oficial](https://mcr.microsoft.com/en-us/artifact/mar/playwright/tags) para as versões mais recentes.

Versões para x86  
```bash
docker pull mcr.microsoft.com/playwright:v1.57.0-noble
docker pull mcr.microsoft.com/playwright:v1.57.0-jammy
docker pull mcr.microsoft.com/playwright:v1.57.0
```

Versões específicas para arquitetura ARM64 e AMD64
```bash
docker pull mcr.microsoft.com/playwright:v1.57.0-noble-amd64
docker pull mcr.microsoft.com/playwright:v1.57.0-jammy-arm64
docker pull mcr.microsoft.com/playwright:v1.57.0-amd64
```

### 🏃‍♂️ Rodando a Imagem

Por padrão, a imagem Docker usa o usuário `root` para rodar os navegadores. Isso desabilita o *sandbox* do Chromium, que não funciona com root.

*   **Códigos Confiáveis (ex: Testes E2E):** Se você confia no código (seus testes), usar o `root` é tranquilo e evita a gestão de usuários extras.
*   **Web Scraping/Crawling:** Recomendamos criar um usuário separado dentro do container e usar um perfil `seccomp`.

#### ✅ Testes End-to-End (Sites Confiáveis)

Para sites confiáveis, rode direto com `root`:

```bash
docker run -it --rm --ipc=host mcr.microsoft.com/playwright:v1.57.0-noble /bin/bash
```

#### 🕷️ Crawling e Scraping (Sites Não Confiáveis)

Para sites desconhecidos, segurança em primeiro lugar! 🛡️ Use um usuário separado (`pwuser`) e o perfil `seccomp`:

```bash
docker run -it --rm --ipc=host --user pwuser --security-opt seccomp=seccomp_profile.json mcr.microsoft.com/playwright:v1.57.0-noble /bin/bash
```

**📄 seccomp_profile.json** (Necessário para o sandbox do Chromium funcionar corretamente):

```json
{
  "comment": "Allow create user namespaces",
  "names": [
    "clone",
    "setns",
    "unshare"
  ],
  "action": "SCMP_ACT_ALLOW",
  "args": [],
  "includes": {},
  "excludes": {}
}
```

---

## ⚙️ Configuração Docker Recomendada

Para garantir a melhor performance e estabilidade dos seus testes no Docker:

1.  **Use `--init`:** Recomendado para evitar processos zumbis (processos com PID=1 precisam de tratamento especial). 🧟‍♂️
2.  **Use `--ipc=host`:** Essencial para o Chromium! Sem isso, ele pode ficar sem memória e crashar. 💥
3.  **Erro ao lançar Chromium?** Tente rodar com `docker run --cap-add=SYS_ADMIN` se estiver desenvolvendo localmente.

---

## 🌐 Conexão Remota

Você pode rodar o Servidor do Playwright no Docker e executar seus testes de outra máquina! Ideal para rodar em distros Linux não suportadas.

### 1️⃣ Iniciando o Servidor Playwright no Docker

```bash
docker run -p 3000:3000 --rm --init -it --workdir /home/pwuser --user pwuser mcr.microsoft.com/playwright:v1.57.0-noble /bin/sh -c "npx -y playwright@1.57.0 run-server --port 3000 --host 0.0.0.0"
```

### 2️⃣ Conectando ao Servidor

Há duas formas de conectar:

**Opção A: Variável de Ambiente (para `@playwright/test`)**
```bash
PW_TEST_CONNECT_WS_ENDPOINT=ws://127.0.0.1:3000/ npx playwright test
```

**Opção B: API `browserType.connect()` (para outras aplicações)**
```javascript
const browser = await playwright['chromium'].connect('ws://127.0.0.1:3000/');
```

### 🔗 Configuração de Rede (Acessando Localhost)

Precisa acessar um servidor rodando na sua máquina host de dentro do container? Use `--add-host`.

```bash
docker run --add-host=hostmachine:host-gateway -p 3000:3000 ...
```

Agora, dentro dos testes, use `hostmachine` ao invés de `localhost`!

> 📝 **Nota:** A versão do Playwright nos testes DEVE ser a mesma da imagem Docker.

---

## 🏷️ Tags de Imagem Disponíveis

Mantenha seus testes consistentes pinando a versão! 📌

*   `:v1.57.0` - Ubuntu 24.04 LTS (Noble Numbat)
*   `:v1.57.0-noble` - Ubuntu 24.04 LTS (Noble Numbat)
*   `:v1.57.0-jammy` - Ubuntu 22.04 LTS (Jammy Jellyfish)

> ⚠️ **Atenção:** Alpine Linux e outras distros baseadas em `musl` **não** são suportadas oficialmente para Firefox e WebKit.

---

## 🏗️ Construa sua Própria Imagem Personalizada

Muitas vezes, precisamos de um ambiente que combine o poder do **Python** com a versatilidade do **Node.js**. Abaixo, apresento um `Dockerfile` profissional, comentado passo a passo, para criar essa imagem híbrida perfeita para seus testes.

### 📝 O Dockerfile Ideal (Python + Node.js)

Este exemplo usa uma imagem oficial do Python e adiciona o Node.js, garantindo que você tenha as duas runtimes disponíveis.

```dockerfile
# 1️⃣ Escolha a imagem base. O 'bookworm' é baseado no Debian 12 (estável e robusto)
FROM python:3.12-bookworm

# 2️⃣ Configura variáveis de ambiente para Python (logs imediatos, sem cache .pyc)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Instalação do Node.js (Versão 20 LTS)
# O Playwright muitas vezes se beneficia do Node para certas operações ou plugins
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    # Limpeza do cache do apt para reduzir o tamanho da imagem
    rm -rf /var/lib/apt/lists/*

# 4️⃣ Define o diretório de trabalho no container
WORKDIR /app

# 5️⃣ Gerenciamento de Dependências (Otimização de Cache)
# Copiamos apenas o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6️⃣ Instalação dos Navegadores do Playwright e Dependências do Sistema
# O comando 'install --with-deps' baixa os browsers e as bibliotecas Linux necessárias
RUN playwright install --with-deps

# 7️⃣ Copia o restante do código do projeto para o container
COPY . .

# 8️⃣ Comando padrão ao iniciar o container (pode ser sobrescrito)
CMD ["pytest"]
```

### 🧠 Entendendo os Passos

1.  **Base Sólida (`FROM python:3.12-bookworm`):** Começamos com uma imagem oficial do Python, garantindo compatibilidade total com suas bibliotecas `pip`.
2.  **Ambiente Híbrido:** Adicionamos o script de setup do NodeSource para instalar o Node.js 20. Isso é útil se você usa ferramentas mistas ou reporters que dependem de Node.
3.  **Otimização de Camadas:** Ao copiar e instalar o `requirements.txt` *antes* do resto do código (`COPY . .`), fazemos com que o Docker não precise reinstalar as bibliotecas toda vez que você altera apenas um arquivo de teste. Economiza muito tempo de build! ⏱️
4.  **Browsers Prontos:** O `playwright install --with-deps` é o comando mágico que deixa o ambiente pronto para rodar testes com UI (mesmo headless).

---

** No nosso dockerfile, usamos uma versão do container do PW:
Dockerfile
```dockerfile
FROM mcr.microsoft.com/playwright:v1.57.0-noble
```

## 🔄 Integração Contínua (CI)

Leve seus testes para a esteira de CI/CD! 🚀

### ⚡ 3 Passos para o Sucesso no CI

1.  **Ambiente:** Garanta que o agente CI possa rodar browsers (use nossa imagem Docker ou instale dependências via CLI).
2.  **Instalação:**
    ```bash
    npm ci
    npx playwright install --with-deps
    ```
3.  **Execução:**
    ```bash
    npx playwright test
    ```

### 👷 Workers no CI

Recomendamos `workers: 2` no CI para estabilidade (evita *flaky tests* por concorrência de recursos).

**playwright.config.ts:**
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // Desabilita paralelismo no CI para maior estabilidade
  workers: process.env.CI ? 2 : undefined,
});
```

---

## 🤖 Exemplos de Configuração de CI

### 🐙 GitHub Actions

#### No push ou pull_request
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
    - uses: actions/checkout@v5
    - uses: actions/setup-node@v6
      with:
        node-version: lts/*
    - name: Install dependencies
      run: npm ci
    - name: Install Playwright Browsers
      run: npx playwright install --with-deps
    - name: Run Playwright tests
      run: npx playwright test
    - uses: actions/upload-artifact@v5
      if: ${{ !cancelled() }}
      with:
        name: playwright-report
        path: playwright-report/
        retention-days: 30

#### 📄 Exemplo: .github/workflows/playwright_docker.yml

Se o seu projeto é **Python**, este é o workflow ideal! Ele utiliza a imagem Docker oficial do Playwright para Python, instala suas dependências e roda os testes com Pytest.

```yaml
name: Tests Com Docker e Python
on:
  - push

permissions:
  contents: write

jobs:

  test-docker:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/playwright/python:v1.55.0-noble
    
    env:
      HOME: /root

    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run Playwright tests (container)
        # --auto-servernum: Garante um display livre automaticamente (evita erros de CI) 🛑🛡️
        run: xvfb-run --auto-servernum -- pytest tests --tracing=retain-on-failure
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }} 
        with:
          name: playwright-traces
          path: test-results/
      - uses: actions/upload-artifact@v5
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```
No exemplo do nosso projeto acima, removemos os steps de instalação do Playwright e navegadores, pois a imagem Docker já os inclui. Caso tiver a necessidade de instalar pacotes adicionais, adicione um step antes de rodar os testes:
```bash
    - name: Install dependencies
      run: npm ci
    - name: Install Playwright Browsers
      run: npx playwright install --with-deps
```

#### Via Containers (Recomendado para consistência visual)
```yaml
jobs:
  playwright:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/playwright:v1.57.0-noble
      options: --user 1001
    steps:
      # ... passos de checkout, install e run ...
```

#### Sharding (Dividir para Conquistar) ⚔️
O GitHub Actions suporta **Sharding**. Divida seus testes em várias máquinas para rodar muito mais rápido! Consulte a documentação oficial para detalhes de merge de relatórios.

#### Fail-Fast (Feedback Rápido) ⚡
Rode apenas o que mudou primeiro!
```bash
npx playwright test --only-changed=$GITHUB_BASE_REF
```

---

### ☁️ Azure Pipelines

#### Linux (Com Docker containerizado)
```yaml
trigger:
- main

pool:
  vmImage: ubuntu-latest
container: mcr.microsoft.com/playwright:v1.57.0-noble

steps:
- task: UseNode@1
  inputs:
    version: '22'
- script: npm ci
- script: npx playwright test
  env:
    CI: 'true'
```

#### Publicando Resultados (JUnit) 📊
Para ver os resultados bonitos no Azure DevOps, configure o *reporter* JUnit no `playwright.config.ts` e use a task `PublishTestResults@2`.

---

### ⭕ CircleCI

Use o executor docker:

```yaml
executors:
  pw-noble-development:
    docker:
      - image: mcr.microsoft.com/playwright:v1.57.0-noble
```

---

### 🤵 Jenkins

Pipeline declarativa com Docker agent:

```groovy
pipeline {
   agent { docker { image 'mcr.microsoft.com/playwright:v1.57.0-noble' } }
   stages {
      stage('e2e-tests') {
         steps {
            sh 'npm ci'
            sh 'npx playwright test'
         }
      }
   }
}
```

---

### 🦊 GitLab CI

```yaml
tests:
  stage: test
  image: mcr.microsoft.com/playwright:v1.57.0-noble
  script:
    - npm ci
    - npx playwright test
```

Também suporta **Sharding** nativo com `parallel`!

---

## 💾 Caching de Browsers

🤔 **Vale a pena?** Geralmente **não**. O tempo para baixar o binário do cache é quase o mesmo de baixar da internet, e dependências de SO no Linux não são cacheáveis facilmente.

---

## 🐛 Debugging

Problemas para lançar o browser? Ative os logs de debug!

```bash
DEBUG=pw:browser npx playwright test
```

### Rodando com Interface Gráfica (Headed) no CI 🖥️

No Linux (Docker/CI), você precisa do `Xvfb` (já incluído na nossa imagem!).

```bash
xvfb-run npx playwright test
```

#### 💡 Dica Pro: `--auto-servernum`

Você deve ter notado o uso da flag `--auto-servernum` nos exemplos acima.

```bash
xvfb-run --auto-servernum -- pytest tests
```

**Para que serve?**
O `xvfb-run` tenta alocar um número de servidor de display (ex: `:99`). Em ambientes de CI modernos com tasks paralelas ou múltiplos containeres, esse número padrão pode já estar em uso, causando falhas misteriosas.

A flag `--auto-servernum` instrui o `Xvfb` a procurar automaticamente o primeiro número de servidor livre disponível, garantindo que seus testes rodem sem conflitos de display. Sempre use em CI! 🛡️

---

