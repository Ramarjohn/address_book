# Address Book API (FastAPI + SQLite)

Minimal address book API to create, update, delete, list, and query addresses within a given distance from coordinates.

## Features
- FastAPI with OpenAPI/Swagger UI at `/docs`
- SQLite persistence via SQLAlchemy
- Pydantic validation
- Centralized logging config
- Distance query using the Haversine formula (km)

## Requirements
- Python 3.10+ (works on 3.9+ as well)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Open:
- Swagger UI: http://127.0.0.1:8000/docs

## API

### Create
`POST /addresses`
```json
{
  "latitude": 12.9716,
  "longitude": 77.5946,
  "label": "optional label"
}
```

The address details (postal_code, country, state, city, district, street) are auto-derived from latitude and longitude.

### Update
`PUT /addresses/{postal_code}`

### Delete
`DELETE /addresses/{postal_code}`

### List
`GET /addresses`

### Nearby
`GET /addresses/nearby?latitude=12.97&longitude=77.59&distance_km=5`

Returns addresses within `distance_km` kilometers of the given coordinates.

## Notes
- The DB file is created at `./app.db` by default (configurable via `DATABASE_URL`).
