import importlib.util
import pathlib
import sys

def _load_module(name, filename):
    path = pathlib.Path(__file__).parent / filename
    module_name = f"src.core.{name}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

# Load modules
config_mod = _load_module("config", "config.core.py")
database_mod = _load_module("database", "database.core.py")
security_mod = _load_module("security", "security.core.py")
dependencies_mod = _load_module("dependencies", "dependencies.core.py")

# Expose key symbols
settings = config_mod.settings
DATABASE_URL = database_mod.DATABASE_URL
engine = database_mod.engine
SessionLocal = database_mod.SessionLocal
get_db = database_mod.get_db
oauth2_scheme = dependencies_mod.oauth2_scheme
get_current_user = dependencies_mod.get_current_user
RoleChecker = dependencies_mod.RoleChecker
hash_password = security_mod.hash_password
verify_password = security_mod.verify_password
create_access_token = security_mod.create_access_token
decode_token = security_mod.decode_token
