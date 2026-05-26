import ast

from lizard.errors import LizardSyntaxError
from lizard.lexer import lex_line
from lizard.parser import parse
from lizard.tokens import TokenType


INDENT = "    "


def _has_content_after(tokens, index: int) -> bool:
    for token in tokens[index + 1:]:
        if token.type == TokenType.COMMENT:
            break
        if token.type == TokenType.SEMICOLON:
            continue
        if token.type == TokenType.CODE:
            if token.value.strip():
                return True
            continue
        return True
    return False


def _has_content_before(tokens, index: int) -> bool:
    for token in tokens[:index]:
        if token.type == TokenType.COMMENT:
            break
        if token.type == TokenType.SEMICOLON:
            continue
        if token.type == TokenType.CODE:
            if token.value.strip():
                return True
            continue
        return True
    return False


def transpile_line(line: str, line_number: int) -> tuple[str, bool, bool]:
    result = []

    opens_block = False
    closes_block = False
    has_comment = False

    tokens = lex_line(line, line_number)

    for index, token in enumerate(tokens):
        if token.type == TokenType.SEMICOLON:
            continue

        if token.type == TokenType.COMMENT:
            result.append(token.value)
            has_comment = True
            break

        if token.type == TokenType.LBRACE:
            if not _has_content_after(tokens, index):
                result.append(":")
                opens_block = True
            else:
                result.append(token.value)
            continue

        if token.type == TokenType.RBRACE:
            if not _has_content_before(tokens, index):
                closes_block = True
            else:
                result.append(token.value)
            continue

        if token.type == TokenType.CODE and closes_block and not result:
            result.append(token.value.lstrip())
            continue

        result.append(token.value)

    transformed = "".join(result)
    if not has_comment:
        transformed = transformed.rstrip()

    return transformed, opens_block, closes_block


def transpile(source: str) -> str:
    tree = parse(source)
    try:
        return ast.unparse(tree)
    except AttributeError as error:
        raise LizardSyntaxError("Python 3.9+ is required for AST unparse.") from error