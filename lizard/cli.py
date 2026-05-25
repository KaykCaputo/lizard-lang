import sys
from pathlib import Path

from lizard.errors import LizardSyntaxError
from lizard.transpiler import transpile
from lizard.runner import run


def main():
    if len(sys.argv) != 2:
        print("Usage: lizard <file.lz>")
        return 1

    path = sys.argv[1]

    try:
        source = Path(path).read_text()
        python_code = transpile(source)
        run(python_code)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return 1
    except LizardSyntaxError as error:
        print(f"Syntax error: {error}")
        return 1

    return 0