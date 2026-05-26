from lizard._bootstrap.errors import LizardSyntaxError
from lizard._bootstrap.tokens import Token, TokenType

KEYWORDS = {
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "case",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "match",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
}

OPERATORS = [
    "==",
    "!=",
    "<=",
    ">=",
    "//=",
    "**=",
    "<<=",
    ">>=",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "&=",
    "|=",
    "^=",
    "//",
    "**",
    "<<",
    ">>",
    "->",
    ":=",
    "=",
    "+",
    "-",
    "*",
    "/",
    "%",
    "<",
    ">",
    "&",
    "|",
    "^",
    "~",
    "@",
]

PUNCTUATION = {
    TokenType.LBRACE.value: TokenType.LBRACE,
    TokenType.RBRACE.value: TokenType.RBRACE,
    TokenType.LPAREN.value: TokenType.LPAREN,
    TokenType.RPAREN.value: TokenType.RPAREN,
    TokenType.LBRACKET.value: TokenType.LBRACKET,
    TokenType.RBRACKET.value: TokenType.RBRACKET,
    TokenType.COMMA.value: TokenType.COMMA,
    TokenType.DOT.value: TokenType.DOT,
    TokenType.COLON.value: TokenType.COLON,
    TokenType.SEMICOLON.value: TokenType.SEMICOLON,
}


def lex_line(line: str, line_number: int) -> list[Token]:
    tokens = []
    buffer = []
    buffer_start_col = 1

    in_string = False
    quote_char = ""

    i = 0

    while i < len(line):
        ch = line[i]
        col = i + 1

        if in_string:
            buffer.append(ch)
            if ch == quote_char:
                tokens.append(Token(TokenType.STRING, "".join(buffer), line_number, buffer_start_col))
                buffer = []
                in_string = False
                quote_char = ""
            i += 1
            continue

        if ch in ('"', "'"):
            if buffer:
                tokens.append(Token(TokenType.CODE, "".join(buffer), line_number, buffer_start_col))
                buffer = []
            in_string = True
            quote_char = ch
            buffer_start_col = col
            buffer.append(ch)
            i += 1
            continue

        if ch == "#":
            if buffer:
                tokens.append(Token(TokenType.CODE, "".join(buffer), line_number, buffer_start_col))
                buffer = []
            tokens.append(Token(TokenType.COMMENT, line[i:], line_number, col))
            break

        if ch in (TokenType.LBRACE.value, TokenType.RBRACE.value, TokenType.SEMICOLON.value):
            if buffer:
                tokens.append(Token(TokenType.CODE, "".join(buffer), line_number, buffer_start_col))
                buffer = []
            if ch == TokenType.LBRACE.value:
                tokens.append(Token(TokenType.LBRACE, ch, line_number, col))
            elif ch == TokenType.RBRACE.value:
                tokens.append(Token(TokenType.RBRACE, ch, line_number, col))
            else:
                tokens.append(Token(TokenType.SEMICOLON, ch, line_number, col))
            i += 1
            continue

        if not buffer:
            buffer_start_col = col
        buffer.append(ch)
        i += 1

    if in_string:
        tokens.append(Token(TokenType.STRING, "".join(buffer), line_number, buffer_start_col))
    elif buffer:
        tokens.append(Token(TokenType.CODE, "".join(buffer), line_number, buffer_start_col))

    return tokens


def _lex_string(source: str, start: int, line_number: int, col: int) -> tuple[str, int, int, int]:
    quote = source[start]
    triple = source.startswith(quote * 3, start)
    i = start + (3 if triple else 1)
    escaped = False
    line = line_number
    column = col + (3 if triple else 1)

    while i < len(source):
        ch = source[i]

        if not triple:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                i += 1
                column += 1
                return source[start:i], i, line, column

        if triple and source.startswith(quote * 3, i):
            i += 3
            column += 3
            return source[start:i], i, line, column

        if ch == "\n":
            line += 1
            column = 1
            i += 1
            continue

        i += 1
        column += 1

    raise LizardSyntaxError(f"Unterminated string at line {line_number}")


def _lex_number(source: str, start: int) -> tuple[str, int]:
    i = start

    if source[i] == ".":
        i += 1

    while i < len(source) and source[i].isdigit():
        i += 1

    if i < len(source) and source[i] == "." and source[start] != ".":
        i += 1
        while i < len(source) and source[i].isdigit():
            i += 1

    if i < len(source) and source[i] in ("e", "E"):
        i += 1
        if i < len(source) and source[i] in ("+", "-"):
            i += 1
        while i < len(source) and source[i].isdigit():
            i += 1

    return source[start:i], i


def _match_operator(source: str, index: int) -> str:
    for operator in OPERATORS:
        if source.startswith(operator, index):
            return operator
    return ""


def lex_source(source: str) -> list[Token]:
    tokens = []
    i = 0
    line_number = 1
    col = 1

    while i < len(source):
        ch = source[i]

        if ch in (" ", "\t", "\r"):
            i += 1
            col += 1
            continue

        if ch == "\n":
            tokens.append(Token(TokenType.NEWLINE, "\n", line_number, col))
            i += 1
            line_number += 1
            col = 1
            continue

        if ch in ('"', "'"):
            start_line = line_number
            start_col = col
            value, i, line_number, col = _lex_string(source, i, line_number, col)
            tokens.append(Token(TokenType.STRING, value, start_line, start_col))
            continue

        if ch == "#":
            start = i
            start_col = col
            while i < len(source) and source[i] != "\n":
                i += 1
                col += 1
            tokens.append(Token(TokenType.COMMENT, source[start:i], line_number, start_col))
            continue

        if source.startswith(TokenType.ELLIPSIS.value, i):
            tokens.append(Token(TokenType.ELLIPSIS, TokenType.ELLIPSIS.value, line_number, col))
            i += 3
            col += 3
            continue

        if ch.isdigit() or (ch == "." and i + 1 < len(source) and source[i + 1].isdigit()):
            value, i = _lex_number(source, i)
            tokens.append(Token(TokenType.NUMBER, value, line_number, col))
            col += len(value)
            continue

        if ch == "_" or ch.isalpha():
            start = i
            i += 1
            while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                i += 1
            value = source[start:i]
            token_type = TokenType.KEYWORD if value in KEYWORDS else TokenType.IDENTIFIER
            tokens.append(Token(token_type, value, line_number, col))
            col += len(value)
            continue

        operator = _match_operator(source, i)
        if operator:
            tokens.append(Token(TokenType.OPERATOR, operator, line_number, col))
            i += len(operator)
            col += len(operator)
            continue

        if ch in PUNCTUATION:
            tokens.append(Token(PUNCTUATION[ch], ch, line_number, col))
            i += 1
            col += 1
            continue

        raise LizardSyntaxError(f"Unexpected character '{ch}' at line {line_number}, column {col}")

    tokens.append(Token(TokenType.NEWLINE, "\n", line_number, col))
    tokens.append(Token(TokenType.EOF, "", line_number, col))
    return tokens
