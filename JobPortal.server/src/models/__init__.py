import importlib.util
import pathlib
import sys

def _load_module(name, filename):
    path = pathlib.Path(__file__).parent / filename
    module_name = f"src.models.{name}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod

# Load modules in dependency order
base_mod = _load_module("base", "base.models.py")
admin_mod = _load_module("admin", "admin.models.py")
candidate_mod = _load_module("candidate", "candidate.models.py")
job_mod = _load_module("job", "job.models.py")
application_mod = _load_module("application", "application.models.py")

# Expose enums and model classes
Base = base_mod.Base
UserRole = base_mod.UserRole
JobStatus = base_mod.JobStatus
ApplicationStatus = base_mod.ApplicationStatus

User = admin_mod.User
CandidateProfile = candidate_mod.CandidateProfile
JobListing = job_mod.JobListing
Application = application_mod.Application

__all__ = [
    "Base",
    "UserRole",
    "JobStatus",
    "ApplicationStatus",
    "User",
    "CandidateProfile",
    "JobListing",
    "Application"
]
