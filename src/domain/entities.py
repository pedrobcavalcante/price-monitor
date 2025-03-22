# Conteúdo do arquivo: /telegram-bot/telegram-bot/src/domain/entities.py

class Usuario:
    """Classe que representa um usuário do bot."""

    def __init__(self, id_usuario: int, nome: str):
        self.id_usuario = id_usuario  # ID único do usuário
        self.nome = nome  # Nome do usuário

    def __str__(self):
        return f"Usuário(id={self.id_usuario}, nome={self.nome})"

class Comando:
    """Classe que representa um comando enviado pelo usuário."""

    def __init__(self, texto: str):
        self.texto = texto  # Texto do comando

    def __str__(self):
        return f"Comando(texto={self.texto})"