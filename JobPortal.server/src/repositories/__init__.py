import importlib.util
import pathlib
import sys

def _load_module(name, filename):
    path = pathlib.Path(__file__).parent / filename
    module_name = f"src.repositories.{name}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

user_mod = _load_module("user", "user.repository.py")
candidate_mod = _load_module("candidate", "candidate.repository.py")
job_mod = _load_module("job", "job.repository.py")
application_mod = _load_module("application", "application.repository.py")

# Expose
UserRepository = user_mod.UserRepository
CandidateRepository = candidate_mod.CandidateRepository
JobRepository = job_mod.JobRepository
ApplicationRepository = application_mod.ApplicationRepository

__all__ = [
    "UserRepository",
    "CandidateRepository",
    "JobRepository",
    "ApplicationRepository"
]
