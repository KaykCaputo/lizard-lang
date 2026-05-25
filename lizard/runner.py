import ast


def run(python_code: str):
    tree = ast.parse(python_code)
    compiled = compile(tree, filename="<lizard>", mode="exec")
    env = {}
    exec(compiled, env, env)

