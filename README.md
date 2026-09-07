# Production REST API Service (Python + Flask)

> **Stack:** Python · Flask · SQLite · structured error handling · request validation · pytest · Docker · GitHub Actions CI/CD
> **Proves:** hands-on **software engineering** — designing, building, testing, and shipping a real HTTP service with validation, error handling, and CI. This is the core deliverable for a SWE role.

A small but production-shaped REST service (a task/inventory API) demonstrating the engineering practices a senior SWE is expected to enforce: separation of concerns, input validation, consistent error responses, a data layer, automated tests, containerization, and continuous integration.

---

## What it demonstrates
- **REST design** — clean CRUD endpoints (`GET/POST/PUT/DELETE`) with proper status codes (200/201/204/400/404/409).
- **Validation & error handling** — invalid and duplicate inputs return structured JSON errors with a consistent shape, not raw exceptions.
- **Data layer** — an SQLite-backed repository, isolated from the HTTP layer (testable).
- **Automated tests** — unit + integration tests (pytest) covering happy paths, validation failures, 404s and duplicates.
- **Docker** — a `Dockerfile` to run it anywhere.
- **CI/CD** — a GitHub Actions workflow that runs tests and lints on every push.

## Endpoints
| Method | Path | Behaviour |
|---|---|---|
| GET | `/tasks` | list tasks |
| POST | `/tasks` | create a task (validates title) |
| GET | `/tasks/<id>` | fetch one task |
| PUT | `/tasks/<id>` | update a task |
| DELETE | `/tasks/<id>` | delete a task |

## Run it
```bash
pip install -r requirements.txt
python -m app.server           # serves on http://127.0.0.1:5000
pytest tests/ -v               # run the suite
```

## Why it's a strong SWE portfolio piece
Any engineering team wants proof you can build and **test** a service, not just notebooks. This repo shows the end-to-end discipline — routes, validation, errors, DB layer, tests, Docker, CI — in a small, readable, verifiable package.
