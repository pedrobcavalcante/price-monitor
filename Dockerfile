FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock ./

# Instala o Poetry
RUN pip install poetry

# Instala as dependências do projeto
RUN poetry install --no-dev

# Copia o código-fonte para o contêiner
COPY src ./src

# Copia o arquivo .env para o contêiner
COPY .env ./

# Comando para iniciar o bot
CMD ["poetry", "run", "python", "src/main.py"]