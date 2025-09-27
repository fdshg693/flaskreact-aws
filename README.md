# Flask version of the app

This replaces the previous Streamlit app with a minimal Flask app that renders a form and shows a greeting.

## What changed
- Switched from Streamlit to Flask (+ Gunicorn in Docker)
- Added HTML template under `templates/index.html`
- Updated `requirements.txt` to `flask` and `gunicorn`
- Updated `Dockerfile` to run Gunicorn on `${PORT:-8501}` and added `/healthz` check

## Run locally (no Docker)

Optional commands:

```bash
# create venv
python3 -m venv .venv
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# run
PORT=8501 python app.py
```

Open http://localhost:8501/

## Run with Docker

Optional commands:

```bash
docker build -t flaskreact-aws .
docker run --rm -p 8501:8501 flaskreact-aws
```

Open http://localhost:8501/

## Deploy on Fly.io

Your `fly.toml` keeps `internal_port = 8501`. Deploy as usual:

```bash
flyctl deploy
```

## Endpoints
- `/` form + greeting page
- `/healthz` simple health check returning `{ "status": "ok" }`
