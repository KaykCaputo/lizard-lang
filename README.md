# Lizard

| | |
| --- | --- |
| <img src="https://raw.githubusercontent.com/KaykCaputo/lizard-lang/master/gecko.png" alt="Lizard icon" width="185" height="185" /> | Lizard is a Python-based programming language that adds semicolons and curly braces to Python syntax. |

It transpiles directly to Python and runs on the Python runtime.

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
    print("Hello World!")

if True:
    hello_world()
```

---

# Features

- Python-compatible syntax
- Curly brace blocks (`{}`)
- Optional semicolons (`;`)
- Direct transpilation to Python
- Lightweight implementation
- VSCode syntax highlighting support

---

# Example

## Lizard

```python
def factorial(n) {
    if n <= 1 {
        return 1;
    }

    return n * factorial(n - 1);
}

print(factorial(5));
```

## Generated Python

```python
def factorial(n):
    if n <= 1:
        return 1

    return n * factorial(n - 1)

print(factorial(5))
```

---

# Installation

- PyPI: [lizard-lang](https://pypi.org/project/lizard-lang/)
- VSCode Extension: [Lizard Lang](https://marketplace.visualstudio.com/items?itemName=KaykCaputo.lizard-lang)

## Clone repository

```bash
git clone https://github.com/KaykCaputo/lizard-lang.git
cd lizard-lang
```

## Install (CLI)

```bash
pip install lizard-lang
```

## Run

```bash
lizard examples/hello.lz
```

---

# VSCode Extension

Lizard includes a VSCode extension with:
- syntax highlighting
- bracket matching
- `.lz` file support

To install locally:

```bash
vsce package
code --install-extension lizard-0.0.1.vsix
```

---

# Current Status

Lizard is currently experimental.

Implemented:
- semicolon removal
- brace blocks
- automatic indentation
- Python transpilation

Planned:
- lexer
- parser
- AST
- formatter
- LSP support
- self-hosting experiments

---

# Project Structure

```txt
lizard/
├── lizard/
│   ├── transpiler.py
│   ├── runner.py
│   └── cli.py
│
├── examples/
├── vscode-extension/
└── pyproject.toml
```

---

# Why?

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

Lizard explores whether Python can support both styles while preserving readability and simplicity.

---

# License

MIT