from lizard.tokens import Token, TokenType


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
