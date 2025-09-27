# Flask + SQLite TODO App

A minimal TODO application using Flask and SQLite. Designed to run locally and on AWS App Runner.

## Features
- List tasks
- Add a task
- Toggle complete/incomplete
- Delete a task

## Run locally

Prereqs: Python 3.11+

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The app runs on http://localhost:8000 by default. Use env vars to change the port:

- `MY_APP_PORT` or `PORT` (e.g., `PORT=9000 python app.py`)

## Deploy notes (App Runner)
- `apprunner.yaml` installs requirements and runs `python3 app.py`
- Network port is 8000 and is mapped via `MY_APP_PORT` env var as configured

## Project layout
- `app.py` – Flask app and DB setup
- `templates/index.html` – HTML template
- `requirements.txt` – Python dependencies
- `apprunner.yaml` – App Runner configuration
