import enum
from enum import Enum

class UserRole(enum.Enum):

    """
    Enumeration of possible user roles.

    Attributes:
        dm (str): Represents a dungeon master role.
        player (str): Represents a regular player role.
    """

    dm = "dm"
    player = "player"

class TokenType(str, Enum):
    PC = "pc"
    ENEMY = "enemy"