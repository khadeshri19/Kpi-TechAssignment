# Job Board with AI-Powered Candidate Matching

An automated talent acquisition platform and job board that matches candidates to job opportunities using semantic search and local NLP matching algorithms.

---

## 1. System Architecture

The application is structured as a modern multi-tier web application consisting of a React Single-Page Application (SPA) frontend, a FastAPI backend REST server, and a PostgreSQL database.

```mermaid
graph TD
    Client[React Client SPA] <--> |REST API / JSON / JWT| Gateway[FastAPI Web Server]
    Gateway <--> |Controller -> Service -> Repo| DB[(PostgreSQL Database)]
    Gateway <--> |Local Vector Encoding| Matcher[AI Matching Engine]
    Matcher <--> |Lazy-loaded MiniLM Model| AI[Sentence-Transformers NLP]
```

### Key Components:
1. **Frontend React SPA**: Modularized into state layers, components, and service wrappers.
2. **FastAPI Web Server**: Built using a strict controller-service-repository architecture.
3. **Database (PostgreSQL)**: Handles persistent storage for users, profiles, jobs, and applications.
4. **Local Matcher Engine**: Computes similarity scores using a Sentence-Transformers NLP model.

---

## 2. Architecture Decisions

### 2.1 Separation of Services and Repositories
We separate the persistence operations from business domain operations by implementing the Service-Repository pattern:
- **Repositories** (e.g., [UserRepository](file:///c:/Drive/JobPortel/JobPortal.server/src/repositories/user.repository.py), [CandidateRepository](file:///c:/Drive/JobPortel/JobPortal.server/src/repositories/candidate.repository.py)) are solely responsible for database interactions, isolating SQLAlchemy query details from business rules.
- **Services** (e.g., [AuthService](file:///c:/Drive/JobPortel/JobPortal.server/src/Modules/Auth/auth.service.py), [CandidateService](file:///c:/Drive/JobPortel/JobPortal.server/src/Modules/Candidate/candidate.service.py)) encapsulate higher-level domain workflow coordination, transaction management, and business logic.
- **Benefits**: Simplifies unit testing, separates concerns, and makes it trivial to replace databases or mocking queries without changing core business logic.

### 2.2 Separate Model and Schema Layers
To prevent tight coupling between API boundaries and persistence layer details, we separate database models from Pydantic schemas:
- **Models** (e.g., [User Model](file:///c:/Drive/JobPortel/JobPortal.server/src/models/user.models.py), [CandidateProfile Model](file:///c:/Drive/JobPortel/JobPortal.server/src/models/candidate.models.py)) define physical tables, column constraints, database relations, and properties.
- **Schemas / Types** (e.g., [auth.types.py](file:///c:/Drive/JobPortel/JobPortal.server/src/Modules/Auth/auth.types.py), [candidate.types.py](file:///c:/Drive/JobPortel/JobPortal.server/src/Modules/Candidate/candidate.types.py)) handle request body deserialization validation and serialization of output responses.
- **Benefits**: Strict validation at the API edge, prevention of unintended data exposures (such as password hashes), and customization of serialization payloads.

### 2.3 Sentence-Transformers Choice for Local Embeddings
For semantic candidate-job matchmaking, the platform uses a local Sentence-Transformers model (`all-MiniLM-L6-v2`):
- **Local Inference**: Generating embeddings locally takes under 30ms, avoiding network latency bottlenecks and external API roundtrips.
- **Privacy & Security**: Candidate profile summaries, skill lists, and private descriptions never leave the hosting environment, preventing potential data leakage.
- **Cost**: Eliminates external token-based API costs associated with pay-per-call services.
- **Resilient Fallbacks**: If the Sentence-Transformers model is missing, the system automatically falls back to keyword overlaps and Jaccard similarity metrics.

---

## 3. API Overview

The backend API exposes the following endpoints (documented in [main.py](file:///c:/Drive/JobPortel/JobPortal.server/src/main.py)):

### 3.1 Authentication (`/auth`)
- `POST /auth/register` - Registers a new user ([auth.route.py](file:///c:/Drive/JobPortel/JobPortal.server/src/Modules/Auth/auth.route.py)). Accepts name, email, password, and role.
- `POST /auth/login` - Validates credentials and returns JWT bearer token, role, and details.

### 3.2 Candidate Profile (`/candidate`)
- `GET /candidate/profile` - Fetches the current logged-in candidate's profile ([candidate.route.py](file:///c:/Drive/JobPortel/JobPortal.server/src/Modules/Candidate/candidate.route.py)).
- `POST /candidate/profile` - Creates or updates a candidate's profile, parsing lists for skills and preferences.
- `POST /candidate/match` - Ranks available active job listings against the candidate's profile using the AI Matching Engine.

### 3.3 Job Listings (`/jobs`)
- `POST /jobs` - Creates a new job posting (HR Admin only, [job.route.py](file:///c:/Drive/JobPortel/JobPortal.server/src/Modules/Job/job.route.py)).
- `GET /jobs` - Lists jobs. Candidates see active listings; Admins see all. Supports filtering by skill, location, and experience.
- `PUT /jobs/{id}` - Updates a job listing (HR Admin only).

### 3.4 Applications (`/apply`)
- `POST /apply` - Submits a candidate application to a job ([application.route.py](file:///c:/Drive/JobPortel/JobPortal.server/src/Modules/Application/application.route.py)). Saves an immutable snapshot of the profile at application time.
- `GET /candidate/applications` - Lists applications submitted by the candidate.
- `GET /jobs/{id}/applications` - Lists job applications (HR Admin only).
- `GET /jobs/{id}/applications/details` - Lists detailed application profiles (HR Admin only).
- `PATCH /applications/{id}/status` - Advances application status: `applied`, `shortlisted`, or `rejected`.

### 3.5 Metrics & Analytics
- `GET /dashboard/metrics` - Retrieves application count per job, pipeline counts, and skills distribution ([dashboard.route.py](file:///c:/Drive/JobPortel/JobPortal.server/src/Modules/Dashboard/dashboard.route.py)).
- `GET /analytics/summary` - Retrieves summary metrics (HR Admin only, [analytics.route.py](file:///c:/Drive/JobPortel/JobPortal.server/src/Modules/Analytics/analytics.route.py)).

---

## 4. Setup Instructions

Follow these steps to run the complete environment locally:

### 4.1 Backend Environment Setup
1. Navigate to the backend directory:
   ```bash
   cd JobPortal.server
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 4.2 Configuration of Environment Variables (`.env`)
Create a `.env` file in the root of the `JobPortal.server` directory with the following variables:
```env
DATABASE_URL=postgresql://jobuser:jobpass@localhost:5432/jobportal
SECRET_KEY=b3d11b3ffbc96c73df89abdf02970a04dae7a467f33333333333333333333333
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4.3 Database Initialization
1. Spin up the PostgreSQL database container:
   ```bash
   docker-compose up -d db
   ```
2. Execute backend database migrations:
   ```bash
   alembic upgrade head
   ```
3. Seed the database with mock records (creates Admin `admin@test.com`/`admin123` and Candidate `alice@test.com`/`candidate123`):
   ```bash
   python seed.py
   ```
4. Launch the FastAPI server locally:
   ```bash
   uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
   ```

### 4.4 Frontend React SPA Setup
1. Navigate to the client directory:
   ```bash
   cd ../JobPortal.client
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the Vite local development server:
   ```bash
   npm run dev
   ```
4. Access the web app in your browser at `http://localhost:5173`.

---

## 5. Assumptions Made

1. **Role Separation**: A user's role (`candidate` or `admin`) is fixed upon registration and governs access boundaries across routes, dashboards, and features.
2. **Embedding Matching Content**: The AI Matching engine builds vector embeddings for candidates by combining their `skills`, `education`, and `project_summaries`. This single vector representation is compared with job vectors representing `title`, `description`, `required_skills`, and `experience_level`.
3. **Application Snapshotting**: Profile snapshots are created dynamically when a candidate applies to a job. Future modifications to the candidate's active profile will not affect the snapshot saved in the application log.

---

## 6. Known Limitations & Future Improvements

1. **Vector Search Scalability**: Cosine similarity is computed directly in Python arrays. While fast for small datasets (under 10,000 listings), large production workloads should offload index lookups to a vector search database extension (e.g., `pgvector` in PostgreSQL).
2. **Embedding Cache**: The sentence-transformer model is lazy-loaded and cached in memory. In multi-process server deployments, each worker initializes its own instance, increasing container RAM requirements. Standardizing an external microservice for vector inference would optimize server resource usage.
