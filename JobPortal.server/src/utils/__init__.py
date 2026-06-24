import importlib.util
import pathlib
import sys

def _load_module(name, filename):
    path = pathlib.Path(__file__).parent / filename
    module_name = f"src.utils.{name}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

# Load modules
exceptions_mod = _load_module("exceptions", "exceptions.utils.py")
logger_mod = _load_module("logger", "logger.utils.py")

# Expose key symbols
EntityNotFoundException = exceptions_mod.EntityNotFoundException
ForbiddenException = exceptions_mod.ForbiddenException
UnauthorizedException = exceptions_mod.UnauthorizedException
BadRequestException = exceptions_mod.BadRequestException
logger = logger_mod.logger
