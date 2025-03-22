# README.md

# Projeto Telegram Bot

Este projeto é um bot para o Telegram que responde a comandos, começando com o comando `/start`. O bot é desenvolvido em Python e utiliza as melhores práticas de desenvolvimento, incluindo o uso de Poetry para gerenciamento de dependências, Docker para containerização e um sistema de logging configurado.

## Estrutura do Projeto

A estrutura do projeto é a seguinte:

```
telegram-bot
├── pyproject.toml          # Configuração do Poetry
├── poetry.lock             # Dependências bloqueadas
├── .env.example            # Exemplo de variáveis de ambiente
├── .env                    # Variáveis de ambiente reais
├── Dockerfile              # Instruções para construir a imagem Docker
├── docker-compose.yml      # Orquestração dos serviços
├── README.md               # Documentação do projeto
├── src                     # Código fonte do bot
│   ├── __init__.py
│   ├── main.py             # Ponto de entrada da aplicação
│   ├── bot                 # Módulo do bot
│   │   ├── __init__.py
│   │   ├── handlers.py     # Manipuladores de comandos
│   │   └── telegram_bot.py # Lógica principal do bot
│   ├── config              # Configurações do projeto
│   │   ├── __init__.py
│   │   ├── settings.py     # Configurações e variáveis de ambiente
│   │   └── logging_config.py # Configuração de logging
│   └── domain              # Entidades do domínio
│       ├── __init__.py
│       └── entities.py     # Definições de entidades
└── tests                   # Testes do projeto
    ├── __init__.py
    ├── unit                # Testes unitários
    │   └── __init__.py
    └── integration         # Testes de integração
        └── __init__.py
```

## Configuração

1. **Clone o repositório**:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd telegram-bot
   ```

2. **Instale as dependências**:
   ```bash
   poetry install
   ```

3. **Configure as variáveis de ambiente**:
   - Renomeie o arquivo `.env.example` para `.env` e preencha com suas chaves privadas e tokens.

4. **Execute o bot**:
   ```bash
   poetry run python src/main.py
   ```

## Docker

Para executar o bot em um contêiner Docker, utilize o seguinte comando:

```bash
docker-compose up --build
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.