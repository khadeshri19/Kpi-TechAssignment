from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from backend.database import get_db
from backend.models import JobListing, JobStatus
from backend.schemas import JobListingCreate, JobListingUpdate, JobListingResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("", response_model=JobListingResponse, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobListingCreate, db: Session = Depends(get_db)):
    job = JobListing(**payload.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("", response_model=List[JobListingResponse])
def list_jobs(
    skill: Optional[str] = Query(None, description="Filter by required skill"),
    location: Optional[str] = Query(None, description="Filter by location (case-insensitive)"),
    experience_level: Optional[str] = Query(None, description="Filter by experience level (case-insensitive)"),
    db: Session = Depends(get_db)
):
    query = db.query(JobListing).filter(JobListing.status == JobStatus.open)
    
    if skill:
        # Match search term against PostgreSQL skill array
        query = query.filter(JobListing.required_skills.any(skill))
    if location:
        query = query.filter(JobListing.location.ilike(f"%{location}%"))
    if experience_level:
        query = query.filter(JobListing.experience_level.ilike(f"%{experience_level}%"))
        
    return query.all()

@router.put("/{id}", response_model=JobListingResponse)
def update_job(id: UUID, payload: JobListingUpdate, db: Session = Depends(get_db)):
    job = db.query(JobListing).filter(JobListing.id == id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job listing not found")
        
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job, key, value)
        
    db.commit()
    db.refresh(job)
    return job
