from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import jobs, candidates, applications

app = FastAPI(
    title="AI Job Board API",
    description="Backend API for Job Board and AI-Powered Candidate Matching Service.",
    version="1.0.0"
)

# Enable CORS for frontend localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(jobs.router)
app.include_router(candidates.router)
app.include_router(applications.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Job Board API"}
