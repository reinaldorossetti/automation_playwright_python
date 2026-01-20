# 🐳 Imagem base oficial do Playwright para Python
# Baseada no Ubuntu 24.04 LTS (Noble Numbat) com navegadores pré-instalados
FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

# 📂 Define o diretório de trabalho
WORKDIR /app

# 📦 Copia apenas o requirements.txt primeiro (otimização de cache)
# Se as dependências não mudarem, o Docker reutiliza essa camada
COPY requirements.txt .

# 🔧 Instala as dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 📁 Copia o código da aplicação
# Copiado por último para aproveitar o cache de camadas anteriores
COPY . .

# 🚀 Comando padrão ao iniciar o container
# Pode ser sobrescrito ao executar: docker run <imagem> <comando>
CMD ["pytest", "tests", "-v"]