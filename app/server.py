"""REST API service with validation, structured error handling, and a clean error contract."""
from flask import Flask, request, jsonify
from .db import TaskRepository

app = Flask(__name__)


def _err(message, status):
    return jsonify({"error": message}), status


@app.errorhandler(404)
def not_found(_):
    return _err("Not found", 404)


@app.errorhandler(405)
def method_not_allowed(_):
    return _err("Method not allowed", 405)


@app.get("/tasks")
def list_tasks():
    return jsonify(repo.list())


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return _err("Title is required and cannot be blank", 400)
    return jsonify(repo.create(title)), 201


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = repo.get(task_id)
    if not task:
        return _err("Task not found", 404)
    return jsonify(task)


@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    task = repo.get(task_id)
    if not task:
        return _err("Task not found", 404)
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or task["title"]).strip()
    done = bool(data.get("done", task["done"]))
    if not title:
        return _err("Title cannot be blank", 400)
    return jsonify(repo.update(task_id, title, done))


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    if not repo.delete(task_id):
        return _err("Task not found", 404)
    return jsonify({"deleted": True}), 200


# a small injectable repo so tests can use an in-memory DB
repo = TaskRepository()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
