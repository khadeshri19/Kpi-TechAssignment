from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.Modules.Auth import router as auth
from src.Modules.Job import router as jobs
from src.Modules.Candidate import router as candidates
from src.Modules.Application import router as applications
from src.Modules.Dashboard import router as dashboard
from src.Modules.Analytics import router as analytics

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
app.include_router(auth)
app.include_router(jobs)
app.include_router(candidates)
app.include_router(applications)
app.include_router(dashboard)
app.include_router(analytics)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Job Board API"}
