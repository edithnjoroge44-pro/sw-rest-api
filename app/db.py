"""SQLite-backed repository layer, isolated from the HTTP layer."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.db")


def get_conn(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
    """)
    conn.commit()


class TaskRepository:
    def __init__(self, conn=None):
        self.conn = conn or get_conn()
        init_db(self.conn)

    def list(self):
        rows = self.conn.execute("SELECT id, title, done, created_at FROM tasks ORDER BY id").fetchall()
        return [self._row(r) for r in rows]

    def get(self, task_id):
        r = self.conn.execute("SELECT id, title, done, created_at FROM tasks WHERE id=?", (task_id,)).fetchone()
        return self._row(r) if r else None

    def create(self, title):
        cur = self.conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        self.conn.commit()
        return self.get(cur.lastrowid)

    def update(self, task_id, title, done):
        self.conn.execute("UPDATE tasks SET title=?, done=? WHERE id=?", (title, int(done), task_id))
        self.conn.commit()
        return self.get(task_id)

    def delete(self, task_id):
        cur = self.conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    @staticmethod
    def _row(r):
        return {"id": r["id"], "title": r["title"], "done": bool(r["done"]),
                "created_at": r["created_at"]}
