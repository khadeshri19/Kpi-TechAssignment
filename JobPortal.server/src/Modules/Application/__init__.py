import importlib.util
import pathlib
import sys

_dir = pathlib.Path(__file__).parent

def _load(name, filename):
    module_name = f"src.Modules.Application.{name}"
    spec = importlib.util.spec_from_file_location(module_name, str(_dir / filename))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

types = _load("types", "application.types.py")
validator = _load("validator", "application.validator.py")
service = _load("service", "application.service.py")
controller = _load("controller", "application.controller.py")
route = _load("route", "application.route.py")

router = route.router
