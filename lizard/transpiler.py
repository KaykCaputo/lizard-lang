from lizard.errors import LizardSyntaxError
from lizard.lexer import lex_line
from lizard.tokens import TokenType


INDENT = "    "


def transpile_line(line: str, line_number: int) -> tuple[str, bool, bool]:
    result = []

    opens_block = False
    closes_block = False
    has_comment = False

    tokens = lex_line(line, line_number)

    for token in tokens:
        if token.type == TokenType.SEMICOLON:
            continue

        if token.type == TokenType.COMMENT:
            result.append(token.value)
            has_comment = True
            break

        if token.type == TokenType.LBRACE:
            result.append(":")
            opens_block = True
            continue

        if token.type == TokenType.RBRACE:
            closes_block = True
            continue

        result.append(token.value)

    transformed = "".join(result)
    if not has_comment:
        transformed = transformed.rstrip()

    return transformed, opens_block, closes_block


def transpile(source: str) -> str:
    output = []

    indent_level = 0

    for line_number, raw_line in enumerate(source.splitlines(), start=1):

        stripped = raw_line.strip()

        if not stripped:
            output.append("")
            continue

        transformed, opens_block, closes_block = transpile_line(stripped, line_number)

        if closes_block:
            indent_level -= 1

            if indent_level < 0:
                raise LizardSyntaxError(f"Unexpected '}}' at line {line_number}")

        output.append(
            INDENT * indent_level + transformed
        )

        if opens_block:
            indent_level += 1

    if indent_level != 0:
        raise LizardSyntaxError("Unclosed block")

    return "\n".join(output)