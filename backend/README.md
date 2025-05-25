# Request Monitoring API

Backend API for browser extension request monitoring with rules engine.

## Setup & Run

```bash
# Install dependencies
poetry install

# Run server
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Configuration

Currently configured domains and URL regexes:

- **www.facebook.com** - `.*facebook\.com/login.*` (high severity)
- **login.example.com** - `.*login\.example\.com/.*` (medium severity)  
- **api.payments.net** - `.*api\.payments\.net/.*` (medium severity)

## Endpoints

- `GET /api/v1/config` - Allows extension to pull domains to monitor
- `POST /api/v1/requests` - Receives requests from extension for analysis

Server runs on `http://localhost:8000` 