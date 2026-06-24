import sys
import os

# Add current folder to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.core.database import SessionLocal, engine
from src.models import Base, User, UserRole, CandidateProfile, JobListing, JobStatus, Application, ApplicationStatus
from src.core.security import hash_password

def seed_db():
    print("Initializing Database Seeding...")
    db = SessionLocal()
    try:
        # 1. Clear existing data
        print("Cleaning up old tables...")
        db.query(Application).delete()
        db.query(CandidateProfile).delete()
        db.query(JobListing).delete()
        db.query(User).delete()
        db.commit()

        # 2. Add Admin User
        print("Creating admin user...")
        admin_user = User(
            name="Platform Admin",
            email="admin@test.com",
            hashed_password=hash_password("admin123"),
            role=UserRole.admin
        )
        db.add(admin_user)
        db.commit()

        # 3. Add Candidate Users & Profiles
        print("Creating candidate accounts and profiles...")
        candidate_data = [
            {
                "name": "Alice Dev",
                "email": "alice@test.com",
                "password": "candidate123",
                "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "React", "Git"],
                "education": "B.S. in Computer Science",
                "project_summaries": "Built a scalable FastAPI microservice and designed full-stack dashboards using React.",
                "preferences": {"location": "Remote", "role_type": "Full-time", "domain_interest": "Backend"}
            },
            {
                "name": "Bob DataScientist",
                "email": "bob@test.com",
                "password": "candidate123",
                "skills": ["Python", "Machine Learning", "TensorFlow", "Pandas", "SQL", "Scikit-Learn"],
                "education": "M.S. in Data Analytics",
                "project_summaries": "Implemented predictive algorithms for customer churn models and engineered text classification pipelines.",
                "preferences": {"location": "San Francisco", "role_type": "Full-time", "domain_interest": "Data Science"}
            },
            {
                "name": "Charlie FrontEnd",
                "email": "charlie@test.com",
                "password": "candidate123",
                "skills": ["React", "TypeScript", "Tailwind CSS", "Next.js", "HTML5", "Vite"],
                "education": "Self-taught Developer",
                "project_summaries": "Developed responsive, premium user interfaces with custom HSL theme parameters and state hooks.",
                "preferences": {"location": "New York", "role_type": "Contract", "domain_interest": "Frontend"}
            }
        ]

        candidates = []
        for c in candidate_data:
            user = User(
                name=c["name"],
                email=c["email"],
                hashed_password=hash_password(c["password"]),
                role=UserRole.candidate
            )
            db.add(user)
            db.commit()

            profile = CandidateProfile(
                user_id=user.id,
                skills=c["skills"],
                education=c["education"],
                project_summaries=c["project_summaries"],
                preferences=c["preferences"]
            )
            db.add(profile)
            db.commit()
            candidates.append(profile)

        # 4. Add Job Listings
        print("Creating job listings...")
        jobs_data = [
            {
                "title": "Backend Software Engineer (FastAPI)",
                "description": "Looking for a backend specialist to optimize API endpoints and model PostgreSQL tables. Required to write robust Python and Docker pipelines.",
                "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "experience_level": "Mid-Level",
                "location": "Remote"
            },
            {
                "title": "Senior AI / Machine Learning Architect",
                "description": "Lead the design of predictive pipelines. Apply deep learning techniques using TensorFlow or PyTorch. Knowledge of Pandas, Scikit-Learn, and Python is essential.",
                "required_skills": ["Python", "Machine Learning", "TensorFlow", "SQL"],
                "experience_level": "Senior",
                "location": "San Francisco"
            },
            {
                "title": "Frontend Engineer (React + TypeScript)",
                "description": "Join our product team to build stunning web interfaces. Experience with React hooks, responsive Tailwind CSS layouts, and Vite builds is highly valued.",
                "required_skills": ["React", "TypeScript", "Tailwind CSS", "HTML5"],
                "experience_level": "Junior-Mid",
                "location": "New York"
            },
            {
                "title": "Full Stack Cloud Developer",
                "description": "Develop and deploy scalable serverless applications. Needs solid React frontend experience combined with Python backend services and PostgreSQL storage.",
                "required_skills": ["Python", "React", "PostgreSQL", "Git"],
                "experience_level": "Mid-Level",
                "location": "Remote"
            },
            {
                "title": "Junior Python Developer",
                "description": "Perfect opportunity for junior engineers to learn database design, RESTful routing, and backend systems writing clean Python, git, and SQL.",
                "required_skills": ["Python", "SQL", "Git"],
                "experience_level": "Junior",
                "location": "Chicago"
            },
            {
                "title": "Data Scientist",
                "description": "Mine large database systems for insights. Train machine learning classification modules using Pandas, SQL, and Scikit-Learn libraries.",
                "required_skills": ["Python", "Machine Learning", "Pandas", "SQL"],
                "experience_level": "Mid-Level",
                "location": "Remote"
            },
            {
                "title": "Lead UI Developer",
                "description": "Design glassmorphism layouts and interactive design guidelines. Expert knowledge in HTML5, Tailwind CSS, TypeScript, and React frameworks required.",
                "required_skills": ["React", "TypeScript", "Tailwind CSS", "Next.js"],
                "experience_level": "Senior",
                "location": "New York"
            },
            {
                "title": "DevOps / Infrastructure Engineer",
                "description": "Automate continuous integration servers, manage postgres servers, containerize microservices using Docker, and configure cloud firewalls.",
                "required_skills": ["Docker", "Git", "PostgreSQL"],
                "experience_level": "Mid-Level",
                "location": "Seattle"
            },
            {
                "title": "Python Scripting Contractor",
                "description": "Short-term contractor role to automate parsing data exports and load them into relational PostgreSQL warehouses using Python scripts.",
                "required_skills": ["Python", "PostgreSQL"],
                "experience_level": "Junior",
                "location": "Remote"
            },
            {
                "title": "Data Engineer",
                "description": "Maintain big data pipelines. Build complex SQL views, configure Docker deployments, and ingest databases with Python orchestration.",
                "required_skills": ["Python", "SQL", "Docker", "PostgreSQL"],
                "experience_level": "Senior",
                "location": "Austin"
            }
        ]

        jobs = []
        for j in jobs_data:
            job = JobListing(
                title=j["title"],
                description=j["description"],
                required_skills=j["required_skills"],
                experience_level=j["experience_level"],
                location=j["location"],
                status=JobStatus.open
            )
            db.add(job)
            db.commit()
            jobs.append(job)

        # 5. Add Sample Applications
        print("Creating sample job applications...")
        # Alice applies to FastAPI Job
        app_alice = Application(
            job_id=jobs[0].id,
            candidate_id=candidates[0].id,
            status=ApplicationStatus.shortlisted,
            profile_snapshot={
                "skills": candidates[0].skills,
                "education": candidates[0].education,
                "project_summaries": candidates[0].project_summaries,
                "preferences": candidates[0].preferences
            }
        )
        db.add(app_alice)

        # Bob applies to AI Job
        app_bob = Application(
            job_id=jobs[1].id,
            candidate_id=candidates[1].id,
            status=ApplicationStatus.applied,
            profile_snapshot={
                "skills": candidates[1].skills,
                "education": candidates[1].education,
                "project_summaries": candidates[1].project_summaries,
                "preferences": candidates[1].preferences
            }
        )
        db.add(app_bob)

        db.commit()
        print("Database successfully seeded!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
