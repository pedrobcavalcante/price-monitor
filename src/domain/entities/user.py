from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    """Entidade que representa um usuário do sistema."""
    id: int
    name: str
    first_access: datetime
