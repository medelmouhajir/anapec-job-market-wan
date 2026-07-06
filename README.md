# ANAPEC Job Market Scraper (ISLI AI Skill)

This repository contains the `anapec-job-market-wan` skill for the ISLI AI system. It is a Universal Skill Runtime (USR) compatible microservice that acts as a job market and recruitment signal scraper targeting ANAPEC (anapec.ma / anapec.org).

## Features
- **Live Scrape**: Retrieves real-time job listings directly from the public ANAPEC jobs directory.
- **Data Extracted**: Job Title, Company, Location, Date Posted.
- **Filtering**: Supports basic keyword and region filtering.
- **ISLI v2.0 Compatible**: Built as a Dockerized HTTP microservice using FastAPI and complies with ISLI's internal JWT authentication scheme.

## Installation

This skill is designed to be installed by the ISLI Core. However, you can run it locally for testing.

### Prerequisites
- Python 3.11+
- Docker (optional)

### Running Locally (Without Docker)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the required environment variable:
   ```bash
   export JWT_SECRET="your_test_secret"
   ```
3. Run the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Running Locally (With Docker)
```bash
docker build -t anapec-job-market-wan .
docker run -p 8000:8000 -e JWT_SECRET="your_test_secret" anapec-job-market-wan
```

## API Endpoints
- `GET /health`: Health check endpoint.
- `GET /.well-known/isli-manifest`: Returns the skill manifest.
- `POST /scrape-jobs`: Initiates a scrape. Requires `X-Internal-Auth` header.

## Manifest
See [`isli-skill.yaml`](isli-skill.yaml) for the full skill configuration and tool definitions.
