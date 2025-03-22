import logging

def configurar_logging():
    """Configura o logging para a aplicação."""
    logging.basicConfig(
        level=logging.INFO,  # Define o nível de log
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato da mensagem de log
        handlers=[
            logging.FileHandler("app.log"),  # Log em arquivo
            logging.StreamHandler()  # Log no console
        ]
    )

# Chama a função de configuração de logging ao importar o módulo
configurar_logging()