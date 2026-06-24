import enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserRole(str, enum.Enum):
    admin = "admin"
    candidate = "candidate"

class JobStatus(str, enum.Enum):
    open = "open"
    closed = "closed"

class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    shortlisted = "shortlisted"
    rejected = "rejected"
