import os
import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, abort


app = Flask(__name__)

# Database utilities
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "todo.db")


def get_db():
    """Get a per-request SQLite connection."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database with the tasks table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK (length(trim(title)) > 0),
                completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0,1)),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


# Routes
@app.route("/", methods=["GET"])
def index():
    db = get_db()
    tasks = db.execute(
        "SELECT id, title, completed FROM tasks ORDER BY id DESC"
    ).fetchall()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = (request.form.get("title") or "").strip()
    if title:
        db = get_db()
        db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        db.commit()
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id: int):
    db = get_db()
    row = db.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        abort(404)
    new_val = 0 if row["completed"] else 1
    db.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_val, task_id))
    db.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id: int):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Initialize DB and start the Flask dev server
    init_db()
    port = int(os.getenv("MY_APP_PORT") or os.getenv("PORT") or 8000)
    app.run(host="0.0.0.0", port=port)