from enum import Enum


class TokenType(Enum):
    CODE = "CODE"
    STRING = "STRING"
    COMMENT = "COMMENT"
    LBRACE = "{"
    RBRACE = "}"
    SEMICOLON = ";"


class Token:
    def __init__(self, token_type, value, line, col):
        self.type = token_type
        self.value = value
        self.line = line
        self.col = col