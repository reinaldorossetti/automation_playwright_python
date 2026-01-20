# 🐳 Playwright com Docker e paralelismo na esteira de CI/CD: guia completo para QA 🚀

## 📜 Introdução

O `Dockerfile` é a porta de entrada para rodar scripts do Playwright em um ambiente Dockerizado. 📦 A imagem já vem com os navegadores do Playwright e todas as dependências de sistema necessárias.

O projeto https://github.com/reinaldorossetti/automation_playwright_python/tree/main já está configurado para rodar com paralelismo no CI/CD usando GitHub Actions. Confira o arquivo `.github/workflows/playwright_docker.yml`.

## 🐳 O que é Docker?

O **Docker** é uma plataforma que empacota aplicações e suas dependências em **contêineres**. Isso garante portabilidade, repetibilidade e ambientes consistentes — essencial para QA, CI/CD e testes automatizados.

### ✅ Principais comandos do Docker

- `docker pull <imagem>`: baixa uma imagem do registro.
- `docker build -t <nome> .`: cria uma imagem a partir do Dockerfile atual.
- `docker run <opções> <imagem>`: cria e executa um contêiner.
- `docker ps`: lista contêineres em execução.
- `docker exec -it <id> <comando>`: executa comandos dentro de um contêiner ativo.
- `docker stop <id>`: para um contêiner em execução.
- `docker rm <id>`: remove um contêiner parado.
- `docker rmi <imagem>`: remove uma imagem local.

### ✅ Cursos na Udemy
[Docker zero ao avançado](https://www.udemy.com/course/docker-zero-avancado)
[DevOps: Automação sem Enrolação](https://www.udemy.com/course/devops-automacao-sem-enrolacao/)
[Docker básico ao avançado](https://www.udemy.com/course/docker-basico-ao-avancado/)

Foco em QAs:
[Docker para QAs](https://www.udemy.com/course/docker-para-qas/)
[Docker for SDET & QA: Build, Test & Automate with Containers](https://www.udemy.com/course/docker-for-sdet-automation-and-testing/)

## 🧩 Paralelismo de testes - Plawright

Para realizar o paralelismo de testes com múltiplos navegadores, usamos o `pytest -n` ou `pytest --numprocesses auto` do pacote `pytest-xdist`. Você também pode especificar um valor fixo de processos, por exemplo: `pytest -n 4` ou `pytest --numprocesses 4`. Tudo isso porque estamos usando o Python como linguagem de automação. No caso do Node.js, o paralelismo é gerenciado nativamente pelo Playwright Test Runner.

Exemplo de comando para rodar 4 workers no Node.js. Esse número pode ser ajustado conforme a capacidade da sua máquina ou do agente de CI, geralmente dividido pelo número de núcleos de CPU disponíveis:
```
npx playwright test --workers 4
```
Para desativar o paralelismo, use `--workers=1`.
```
npx playwright test --workers=1
```

**No projeto, o paralelismo está configurado com `pytest-xdist` no arquivo abaixo:**  
```bash
pytest.ini
```

## 🛠️ Como usar a imagem oficial do Playwright

A imagem Docker oficial é publicada no **Microsoft Artifact Registry**, e não no Docker Hub.

> ℹ️ **Info:** Essa imagem Docker destina-se **apenas** para fins de desenvolvimento e testes. ⚠️ **Não é recomendado** usá-la para visitar sites não confiáveis.

### 📥 Baixando a imagem (pull)

A versão mais atual é a `v1.57.0` (Junho de 2024). Substitua pela versão desejada conforme necessário. Mas isso pode mudar com o tempo, então sempre verifique a [página oficial](https://mcr.microsoft.com/en-us/artifact/mar/playwright/tags) para as versões mais recentes.

Versões para x86:  
```bash
docker pull mcr.microsoft.com/playwright:v1.57.0-noble
docker pull mcr.microsoft.com/playwright:v1.57.0-jammy
docker pull mcr.microsoft.com/playwright:v1.57.0
```

Versões específicas para arquitetura ARM64 e AMD64:
```bash
docker pull mcr.microsoft.com/playwright:v1.57.0-noble-amd64
docker pull mcr.microsoft.com/playwright:v1.57.0-jammy-arm64
docker pull mcr.microsoft.com/playwright:v1.57.0-amd64
```

Como estou usando uma imagem específica do Playwright para Python, a tag utilizada é mais antiga. Segue abaixo a imagem:  
```bash
docker pull mcr.microsoft.com/playwright/python:v1.57.0-noble
```
Link: https://mcr.microsoft.com/en-us/artifact/mar/playwright/python/about

## 🏷️ Tags de imagem disponíveis

Mantenha seus testes consistentes pinando a versão! 📌

*   `:v1.57.0` - Ubuntu 24.04 LTS (Noble Numbat)
*   `:v1.57.0-noble` - Ubuntu 24.04 LTS (Noble Numbat)
*   `:v1.57.0-jammy` - Ubuntu 22.04 LTS (Jammy Jellyfish)

> ⚠️ **Atenção:** Alpine Linux e outras distros baseadas em `musl` **não** são suportadas oficialmente para Firefox e WebKit.

### 🏃‍♂️ Rodando a imagem

Por padrão, a imagem Docker usa o usuário `root` para rodar os navegadores. Isso desabilita o *sandbox* do Chromium, que não funciona com root.

*   **Códigos confiáveis (ex: Testes E2E):** Se você confia no código (seus testes), usar o `root` é tranquilo e evita a gestão de usuários extras.
*   **Web scraping/crawling:** Recomendamos criar um usuário separado dentro do contêiner e usar um perfil `seccomp`.

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

## ⚙️ Configuração recomendada do Docker

Para garantir a melhor performance e estabilidade dos seus testes no Docker:

1.  **Use `--init`:** Recomendado para evitar processos zumbis (processos com PID=1 precisam de tratamento especial). 🧟‍♂️
2.  **Use `--ipc=host`:** Essencial para o Chromium! Sem isso, ele pode ficar sem memória e crashar. 💥
3.  **Erro ao lançar Chromium?** Tente rodar com `docker run --cap-add=SYS_ADMIN` se estiver desenvolvendo localmente.

---

## 🌐 Conexão remota

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

Precisa acessar um servidor rodando na sua máquina host de dentro do contêiner? Use `--add-host`.

```bash
docker run --add-host=hostmachine:host-gateway -p 3000:3000 ...
```

Agora, dentro dos testes, use `hostmachine` em vez de `localhost`!

> 📝 **Nota:** A versão do Playwright nos testes DEVE ser a mesma da imagem Docker.

---

## 🏗️ Construa sua própria imagem personalizada

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

### 🧠 Entendendo os passos

1.  **Base Sólida (`FROM python:3.12-bookworm`):** Começamos com uma imagem oficial do Python, garantindo compatibilidade total com suas bibliotecas `pip`.
2.  **Ambiente Híbrido:** Adicionamos o script de setup do NodeSource para instalar o Node.js 20. Isso é útil se você usa ferramentas mistas ou reporters que dependem de Node.
3.  **Otimização de Camadas:** Ao copiar e instalar o `requirements.txt` *antes* do resto do código (`COPY . .`), fazemos com que o Docker não precise reinstalar as bibliotecas toda vez que você altera apenas um arquivo de teste. Economiza muito tempo de build! ⏱️
4.  **Browsers Prontos:** O `playwright install --with-deps` é o comando mágico que deixa o ambiente pronto para rodar testes com UI (mesmo headless).

---

No nosso `Dockerfile`, usamos uma imagem oficial do Playwright. Exemplo de Dockerfile:

```dockerfile
FROM mcr.microsoft.com/playwright:v1.57.0-noble
```

## 🔄 Integração Contínua (CI)

Leve seus testes para a esteira de CI/CD! 🚀

### ⚡ 3 passos para o sucesso no CI

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

#### Em push ou pull_request
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
```

#### 📄 Exemplo: .github/workflows/playwright_docker.yml

Se o seu projeto é **Python**, este é o workflow ideal! Ele utiliza a imagem Docker oficial do Playwright para Python, instala suas dependências e roda os testes com Pytest.

```yaml
name: Tests Com Docker e Python
on:
  - push

permissions:
  contents: write
  pages: write
  id-token: write

jobs:

  test-docker:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/playwright/python:v1.57.0-noble
      options: --user root
    
    env:
      HOME: /root

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Necessário para histórico do Allure
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Playwright tests (container)
        continue-on-error: true
        run: xvfb-run --auto-servernum -- pytest tests --alluredir=./output/allure
    
      - name: Generate Allure Report
        uses: andgineer/allure-report@v3.6
        if: always()
        with:
          allure-results: output/allure # Directory with test results
          website: allure-results          # Directory to store the report
          reports-site: allure-results
          reports-site-path: allure-results
          github-pages: github-pages

      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }} 
        with:
          name: playwright-traces
          path: allure-results/
          
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: allure-results
          destination_dir: allure-results
```

No exemplo do nosso projeto acima, removemos os passos de instalação do Playwright e dos navegadores, pois a imagem Docker já os inclui. Caso seja necessário instalar pacotes adicionais, adicione um passo antes de rodar os testes:
```bash
    - name: Install dependencies
      run: npm ci
    - name: Install Playwright Browsers
      run: npx playwright install --with-deps
```

#### Via containers (recomendado para consistência visual)
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

## 💾 Cache de navegadores

🤔 **Vale a pena?** Geralmente **não**. O tempo para baixar o binário do cache é quase o mesmo de baixar da internet, e dependências de SO no Linux não são cacheáveis facilmente.

---

## 🐛 Depuração

Problemas para lançar o navegador? Ative os logs de debug!

```bash
DEBUG=pw:browser npx playwright test
```

### Rodando com interface gráfica (headed) no CI 🖥️

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
O `xvfb-run` tenta alocar um número de servidor de display (ex: `:99`). Em ambientes de CI modernos com tarefas paralelas ou múltiplos contêineres, esse número padrão pode já estar em uso, causando falhas misteriosas.

A flag `--auto-servernum` instrui o `Xvfb` a procurar automaticamente o primeiro número de servidor livre disponível, garantindo que seus testes rodem sem conflitos de display. Sempre use em CI! 🛡️

---

*Documentação traduzida, revisada e organizada para a comunidade QA do Brasil!* 🇧🇷💚# 🐳 Playwright com Docker e paralelismo na esteira de CI/CD: guia completo para QA 🚀

## 📜 Introdução

O `Dockerfile` é a porta de entrada para rodar scripts do Playwright em um ambiente Dockerizado. 📦 A imagem já vem com os navegadores do Playwright e todas as dependências de sistema necessárias.

O projeto https://github.com/reinaldorossetti/automation_playwright_python/tree/main já está configurado para rodar com paralelismo no CI/CD usando GitHub Actions. Confira o arquivo `.github/workflows/playwright_docker.yml`.

## 🐳 O que é Docker?

O **Docker** é uma plataforma que empacota aplicações e suas dependências em **containers**. Isso garante portabilidade, repetibilidade e ambientes consistentes — essencial para QA, CI/CD e testes automatizados.

### ✅ Principais comandos do Docker

- `docker pull <imagem>`: baixa uma imagem do registry. 
- `docker build -t <nome> .`: cria uma imagem a partir do Dockerfile atual.
- `docker run <opções> <imagem>`: cria e executa um container.
- `docker ps`: lista containers em execução.
- `docker exec -it <id> <comando>`: executa comandos dentro de um container ativo.
- `docker stop <id>`: para um container em execução.
- `docker rm <id>`: remove um container parado.
- `docker rmi <imagem>`: remove uma imagem local.

## 🧩 Paralelismo de testes

Para realizar o paralelismo de testes com múltiplos navegadores, usamos o `pytest -n` ou `pytest --numprocesses auto` do pacote `pytest-xdist`. Você também pode especificar um valor fixo de processos, por exemplo: `pytest -n 4` ou `pytest --numprocesses 4`. Tudo isso porque estamos usando o Python como linguagem de automação. No caso do Node.js, o paralelismo é gerenciado nativamente pelo Playwright Test Runner.

Exemplo de comando para rodar 4 workers no Node.js. Esse número pode ser ajustado conforme a capacidade da sua máquina ou do agente de CI, geralmente dividido pelo número de núcleos de CPU disponíveis:
```
npx playwright test --workers 4
```
Para desativar o paralelismo, use `--workers=1`.
```
npx playwright test --workers=1
```

**No projeto, o paralelismo está configurado com `pytest-xdist` no arquivo abaixo:**  
```bash
pytest.ini
```

## 🛠️ Como usar a imagem oficial

A imagem Docker do Playwright oficial é publicada no **Microsoft Artifact Registry**, e não no Docker Hub.

> ℹ️ **Info:** Essa imagem Docker destina-se **apenas** para fins de desenvolvimento e testes. ⚠️ **Não é recomendado** usá-la para visitar sites não confiáveis.


### 📥 Baixando a Imagem (Pull)  
A versão mais atual é a `v1.57.0` (Junho de 2024). Substitua pela versão desejada conforme necessário. Mas isso pode mudar com o tempo, então sempre verifique a [página oficial](https://mcr.microsoft.com/en-us/artifact/mar/playwright/tags) para as versões mais recentes.

Versões para x86  
```bash
docker pull mcr.microsoft.com/playwright:v1.57.0-noble
docker pull mcr.microsoft.com/playwright:v1.57.0-jammy
docker pull mcr.microsoft.com/playwright:v1.57.0
```

Versões específicas para arquitetura ARM64 e AMD64:
```bash
docker pull mcr.microsoft.com/playwright:v1.57.0-noble-amd64
docker pull mcr.microsoft.com/playwright:v1.57.0-jammy-arm64
docker pull mcr.microsoft.com/playwright:v1.57.0-amd64
```

Como estou usando uma versão específica do Playwright para Python, ela está em uma versão mais antiga. Segue abaixo a imagem:  
```bash
docker pull mcr.microsoft.com/playwright/python:v1.57.0-noble
```
Link: https://mcr.microsoft.com/en-us/artifact/mar/playwright/python/about


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
## 🐳 O que é Docker?
# 8️⃣ Comando padrão ao iniciar o container (pode ser sobrescrito)
### ✅ Principais comandos do Docker
- `docker pull <imagem>`: baixa uma imagem do registro.
- `docker build -t <nome> .`: cria uma imagem a partir do Dockerfile atual.
- `docker run <opções> <imagem>`: cria e executa um contêiner.
- `docker ps`: lista contêineres em execução.
- `docker exec -it <id> <comando>`: executa comandos dentro de um contêiner ativo.
- `docker stop <id>`: para um contêiner em execução.
- `docker rm <id>`: remove um contêiner parado.
- `docker rmi <imagem>`: remove uma imagem local.

## 🛠️ Como usar a imagem oficial do Playwright

Versões para x86:  
Como estou usando uma imagem específica do Playwright para Python, ela está em uma versão mais antiga. Segue abaixo a imagem:  
```dockerfile
### 🏃‍♂️ Rodando a imagem
*   **Códigos confiáveis (ex: Testes E2E):** Se você confia no código (seus testes), usar o `root` é tranquilo e evita a gestão de usuários extras.
*   **Web scraping/crawling:** Recomendamos criar um usuário separado dentro do contêiner e usar um perfil `seccomp`.
## 🔄 Integração Contínua (CI)
Para sites desconhecidos, segurança em primeiro lugar! 🛡️ Use um usuário separado (`pwuser`) e o perfil `seccomp`:
Leve seus testes para a esteira de CI/CD! 🚀
## ⚙️ Configuração recomendada do Docker
### ⚡ 3 Passos para o Sucesso no CI
Para garantir a melhor performance e estabilidade dos seus testes no Docker:
1.  **Ambiente:** Garanta que o agente CI possa rodar browsers (use nossa imagem Docker ou instale dependências via CLI).
## 🌐 Conexão remota
    ```bash
Agora, dentro dos testes, use `hostmachine` em vez de `localhost`!
    npx playwright install --with-deps
## 🏗️ Construa sua própria imagem personalizada
3.  **Execução:**
### 🧠 Entendendo os passos
    npx playwright test
No nosso `Dockerfile`, usamos uma imagem oficial do Playwright. Exemplo:

### ⚡ 3 passos para o sucesso no CI

### 👷 Workers no CI

#### Em push ou pull_request
```typescript
#### Via containers (recomendado para consistência visual)

## 💾 Cache de navegadores
  // Desabilita paralelismo no CI para maior estabilidade
## 🐛 Depuração
});
Problemas para lançar o navegador? Ative os logs de debug!

### Rodando com interface gráfica (headed) no CI 🖥️

Em ambientes de CI modernos com tarefas paralelas ou múltiplos contêineres, esse número padrão pode já estar em uso, causando falhas misteriosas.
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
  pages: write
  id-token: write

jobs:

  test-docker:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/playwright/python:v1.57.0-noble
      options: --user root
    
    env:
      HOME: /root

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Necessário para histórico do Allure
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Playwright tests (container)
        continue-on-error: true
        run: xvfb-run --auto-servernum -- pytest tests --alluredir=./output/allure
    
      - name: Generate Allure Report
        uses: andgineer/allure-report@v3.6
        if: always()
        with:
          allure-results: output/allure # Directory with test results
          website: allure-results          # Directory to store the report
          reports-site: allure-results
          reports-site-path: allure-results
          github-pages: github-pages

      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }} 
        with:
          name: playwright-traces
          path: allure-results/
          
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: allure-results
          destination_dir: allure-results
```
No exemplo do nosso projeto acima, removemos os passos de instalação do Playwright e dos navegadores, pois a imagem Docker já os inclui. Caso seja necessário instalar pacotes adicionais, adicione um passo antes de rodar os testes:
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

## 📄 Conclusão

Usar Docker em testes automatizados traz consistência, isolamento e reprodutibilidade. Com ambientes padronizados, você reduz o “na minha máquina funciona”, acelera o onboarding do time e garante que os testes rodem da mesma forma localmente e no CI. Além disso, o controle de versões de navegadores e dependências fica mais simples, o que diminui flutuações e aumenta a confiabilidade dos resultados.

