import importlib.util
import pathlib
import sys

_dir = pathlib.Path(__file__).parent

def _load(name, filename):
    module_name = f"src.Modules.Candidate.{name}"
    spec = importlib.util.spec_from_file_location(module_name, str(_dir / filename))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

types = _load("types", "candidate.types.py")
validator = _load("validator", "candidate.validator.py")
service = _load("service", "candidate.service.py")
controller = _load("controller", "candidate.controller.py")
route = _load("route", "candidate.route.py")

router = route.router
