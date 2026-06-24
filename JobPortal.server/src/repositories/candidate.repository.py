from sqlalchemy.orm import Session
from uuid import UUID
from src.models import CandidateProfile
from typing import Optional

class CandidateRepository:
    """
    Handles all database operations for the CandidateProfile model.
    """

    @staticmethod
    def get_by_id(db: Session, profile_id: UUID) -> Optional[CandidateProfile]:
        """
        Retrieves a candidate profile by its UUID primary key.
        """
        return db.query(CandidateProfile).filter(CandidateProfile.id == profile_id).first()

    @staticmethod
    def get_by_user_id(db: Session, user_id: UUID) -> Optional[CandidateProfile]:
        """
        Retrieves a candidate profile by the user's UUID.
        """
        return db.query(CandidateProfile).filter(CandidateProfile.user_id == user_id).first()

    @staticmethod
    def create(db: Session, profile: CandidateProfile) -> CandidateProfile:
        """
        Creates a new candidate profile in the database.
        """
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def update(db: Session, profile: CandidateProfile) -> CandidateProfile:
        """
        Saves changes to an existing candidate profile.
        """
        db.commit()
        db.refresh(profile)
        return profile
