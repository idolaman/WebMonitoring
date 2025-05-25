# Request Monitoring API

Backend API for browser extension request monitoring with rules engine.

## Setup & Run

```bash
# Install dependencies
poetry install

# Run server
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

- `GET /api/v1/config` - Get domains to monitor
- `POST /api/v1/requests` - Ingest request for analysis

Server runs on `http://localhost:8000` 