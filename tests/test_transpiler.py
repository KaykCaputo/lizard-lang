import ast
import io
import textwrap
from contextlib import redirect_stdout

from lizard.transpiler import transpile


def transpile_and_exec(source: str):
    python_code = transpile(textwrap.dedent(source).strip("\n"))
    ast.parse(python_code)
    env: dict[str, object] = {}
    exec(compile(python_code, "<lizard>", "exec"), env, env)
    return python_code, env


def transpile_and_capture_output(source: str):
    python_code = transpile(textwrap.dedent(source).strip("\n"))
    ast.parse(python_code)
    env: dict[str, object] = {}
    output = io.StringIO()
    with redirect_stdout(output):
        exec(compile(python_code, "<lizard>", "exec"), env, env)
    return python_code, env, output.getvalue()


def test_factorial_example_output():
    _, _, output = transpile_and_capture_output(
        """
        def factorial(n) {
            if n <= 1 {
                return 1;
            }

            return n * factorial(n - 1);
        }

        print(factorial(5));
        """
    )

    assert output.strip() == "120"


def test_conditionals_and_boolean_logic():
    _, env = transpile_and_exec(
        """
        value = 10;
        if value > 10 {
            result = "greater";
        } elif value == 10 {
            result = "equal";
        } else {
            result = "less";
        }

        flag = (value == 10) and not False or False;
        """
    )

    assert env["result"] == "equal"
    assert env["flag"] is True


def test_for_loop_and_list_append():
    _, env = transpile_and_exec(
        """
        values = [];
        for i in range(5) {
            values.append(i * 2);
        }
        """
    )

    assert env["values"] == [0, 2, 4, 6, 8]


def test_while_loop_break_continue():
    _, env = transpile_and_exec(
        """
        i = 0;
        values = [];
        while True {
            i += 1;
            if i == 2 {
                continue;
            }
            values.append(i);
            if i >= 4 {
                break;
            }
        }
        """
    )

    assert env["values"] == [1, 3, 4]


def test_functions_default_args_and_recursion():
    _, env = transpile_and_exec(
        """
        def power(base, exp=2) {
            if exp == 0 {
                return 1;
            }
            return base * power(base, exp - 1);
        }

        squared = power(3);
        cubed = power(2, 3);
        """
    )

    assert env["squared"] == 9
    assert env["cubed"] == 8


def test_list_and_tuple_literals():
    _, env = transpile_and_exec(
        """
        items = [1, 2, 3];
        coords = (4, 5, 6);
        """
    )

    assert env["items"] == [1, 2, 3]
    assert env["coords"] == (4, 5, 6)


def test_list_comprehension():
    _, env = transpile_and_exec(
        """
        squares = [n * n for n in range(6) if n % 2 == 0];
        """
    )

    assert env["squares"] == [0, 4, 16]


def test_imports_and_attribute_access():
    _, env = transpile_and_exec(
        """
        import math;
        root = math.sqrt(81);
        """
    )

    assert env["root"] == 9


def test_try_except_finally():
    _, env = transpile_and_exec(
        """
        result = [];
        try {
            1 / 0;
        } except ZeroDivisionError {
            result.append("handled");
        } finally {
            result.append("finished");
        }
        """
    )

    assert env["result"] == ["handled", "finished"]


def test_class_definition_and_method():
    _, env = transpile_and_exec(
        """
        class Counter {
            def __init__(self, start=0) {
                self.value = start;
            }

            def inc(self) {
                self.value += 1;
            }
        }

        counter = Counter(5);
        counter.inc();
        """
    )

    assert env["counter"].value == 6


def test_strings_with_braces_and_semicolons():
    _, env = transpile_and_exec(
        r"""
        text = "{;}";
        pattern = "value{0}".format(3);
        """
    )

    assert env["text"] == "{;}"
    assert env["pattern"] == "value3"


def test_comments_with_braces():
    _, env = transpile_and_exec(
        """
        value = 1; # comment with { } ;
        """
    )

    assert env["value"] == 1


def test_dict_literal():
    transpile_and_exec(
        """
        data = {"a": 1, "b": 2};
        """
    )


def test_dict_comprehension():
    transpile_and_exec(
        """
        data = {x: x * 2 for x in range(3)};
        """
    )


def test_set_literal():
    transpile_and_exec(
        """
        items = {1, 2, 3};
        """
    )


def test_triple_quoted_string():
    _, env = transpile_and_exec(
        """
        text = \"\"\"line1
        line2\"\"\";
        """
    )

    assert env["text"] == "line1\nline2"


def test_decorator_support():
    _, env = transpile_and_exec(
        """
        def add_one(fn) {
            def wrapper() {
                return fn() + 1;
            }
            return wrapper;
        }

        @add_one
        def base() {
            return 41;
        }

        result = base();
        """
    )

    assert env["result"] == 42
