from __future__ import annotations

import importlib.abc
import importlib.util
import sys
from pathlib import Path

from lizard._bootstrap.transpiler import transpile as bootstrap_transpile

BASE_DIR = Path(__file__).resolve().parent
_transpiler = bootstrap_transpile


def _set_transpiler(new_transpiler):
    global _transpiler
    _transpiler = new_transpiler


class LizardLoader(importlib.abc.Loader):
    def __init__(self, path: Path, is_package: bool):
        self.path = path
        self.is_pkg = is_package

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        source = self.path.read_text()
        python_code = _transpiler(source)
        code = compile(python_code, str(self.path), "exec")
        module.__file__ = str(self.path)
        if self.is_pkg:
            module.__path__ = [str(self.path.parent)]
        exec(code, module.__dict__)
        if module.__name__ == "lizard.transpiler" and hasattr(module, "transpile"):
            _set_transpiler(module.transpile)

    def is_package(self, fullname):
        return self.is_pkg


class LizardFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == "lizard":
            return None
        if not fullname.startswith("lizard."):
            return None

        parts = fullname.split(".")[1:]
        module_root = BASE_DIR.joinpath(*parts)

        if module_root.is_dir():
            init_path = module_root / "__init__.lz"
            if init_path.exists():
                loader = LizardLoader(init_path, True)
                return importlib.util.spec_from_file_location(
                    fullname,
                    init_path,
                    loader=loader,
                    submodule_search_locations=[str(module_root)],
                )

        module_path = module_root.with_suffix(".lz")
        if module_path.exists():
            loader = LizardLoader(module_path, False)
            return importlib.util.spec_from_file_location(fullname, module_path, loader=loader)
        return None


def install():
    if not any(isinstance(finder, LizardFinder) for finder in sys.meta_path):
        sys.meta_path.insert(0, LizardFinder())


def main():
    install()
    from lizard.cli import main as lizard_main

    return lizard_main()


def run_tests():
    install()
    from lizard.tests.runner import main as test_main

    return test_main()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-tests":
        sys.argv.pop(1)
        raise SystemExit(run_tests())
    raise SystemExit(main())
