# Lizard

| | |
| --- | --- |
| <img src="https://raw.githubusercontent.com/KaykCaputo/lizard-lang/master/gecko.png" alt="Lizard icon" width="185" height="185" /> | Lizard is a Python‑compatible language that adds curly braces and optional semicolons to Python syntax, with a self‑hosted compiler that targets clean Python via the `ast` module. |

```lz
def hello_world() {
    print("Hello World!");
}

if True {
    hello_world();
}
```

Transpiled output:

```python
def hello_world():
    print('Hello World!')

if True:
    hello_world()
```

---

## Features

- Python‑compatible syntax with `{}` blocks and optional `;`
- Lexer → parser → AST → `ast.unparse` pipeline (no text‑based indentation tricks)
- Supports comprehensions, decorators, and triple‑quoted strings
- Runs on the standard Python runtime
- Self‑hosting compiler (Lizard in Lizard), bootstrapped from Python
- VSCode syntax highlighting support

---

## Examples

- **Hello world:** `examples/hello.lz`
- **Factorial:** `examples/factorial.lz`
- **Comprehensions + dict/set literals:** `examples/comprehensions.lz`
- **Decorators:** `examples/decorators.lz`
- **Multiline strings:** `examples/multiline_strings.lz`

---

## Installation

- PyPI: [lizard-lang](https://pypi.org/project/lizard-lang/)
- VSCode Extension: [Lizard Lang](https://marketplace.visualstudio.com/items?itemName=KaykCaputo.lizard-lang)

```bash
pip install lizard-lang
```

Run:

```bash
lizard examples/hello.lz
```

---

## Development

```bash
pytest
```

---

## Current Status

Lizard is experimental.

Implemented:
- lexer + parser + AST pipeline
- brace blocks and semicolon‑optional syntax
- Python code generation via `ast.unparse`
- self‑hosting compiler (Lizard in Lizard)

Planned:
- formatter
- LSP support
- LLVM + hybrid FFI backend

---

## Why?

Because some developers prefer:

```js
if (condition) {
    doSomething();
}
```

over:

```python
if condition:
    do_something()
```

Lizard explores whether Python can support both styles while staying fully compatible with Python semantics.

---

## License

MIT