# Job Board with AI-Powered Candidate Matching

An automated talent acquisition platform and job board that matches candidates to job opportunities using semantic search and AI matching algorithms.

## Tech Stack
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **Frontend**: React + TypeScript
- **AI Engine**: sentence-transformers (for semantic candidate matching)

## Architecture Overview
The application follows a clean, modular service-repository architecture. The backend is structured into clear directory domains (controllers, models, schemas, repositories, services, utils, and custom AI matcher logic), separating database-level models and raw queries from high-level business workflow services. The React frontend is modularized into dedicated components, state contexts, custom hooks, typings, and API-call service wrappers, ensuring high extensibility.

## Architecture Decisions
- **TODO**: Explain why repositories/ is separate from services/
- **TODO**: Explain the use of separate model and schema layers
- **TODO**: Detail sentence-transformers choice for localized semantic embeddings

## Setup Instructions
- **TODO**: Clone repository setup
- **TODO**: Configuration of environmental variables (`.env`)
- **TODO**: running local databases or using `docker-compose up`
- **TODO**: Executing initial database migrations
- **TODO**: Seeding test mock records
- **TODO**: Installing dependencies and launching the React frontend

## API Overview
- **TODO**: Document FastAPI endpoints once routes are implemented

## Known Limitations / Improvements
- **TODO**: Detail performance optimization points or improvements to be completed with more time

## Assumptions Made
- **TODO**: Outline product and data-modeling assumptions made during development
