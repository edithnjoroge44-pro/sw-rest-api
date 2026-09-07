import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import app.server as server
from app.db import TaskRepository, get_conn


def make_client():
    # use a throwaway DB for tests
    tmp = os.path.join(tempfile.mkdtemp(), "test.db")
    server.repo = TaskRepository(get_conn(tmp))
    app = server.app
    app.config["TESTING"] = True
    return app.test_client()


def test_create_and_list():
    c = make_client()
    r = c.post("/tasks", json={"title": "Fix bug"})
    assert r.status_code == 201
    assert r.get_json()["title"] == "Fix bug"
    assert len(c.get("/tasks").get_json()) == 1


def test_blank_title_rejected():
    c = make_client()
    r = c.post("/tasks", json={"title": "   "})
    assert r.status_code == 400
    assert r.get_json()["error"]


def test_missing_title_rejected():
    c = make_client()
    assert c.post("/tasks", json={}).status_code == 400


def test_get_404():
    c = make_client()
    assert c.get("/tasks/9999").status_code == 404


def test_update_toggle_done():
    c = make_client()
    tid = c.post("/tasks", json={"title": "Ship it"}).get_json()["id"]
    r = c.put(f"/tasks/{tid}", json={"done": True})
    assert r.status_code == 200
    assert r.get_json()["done"] is True


def test_delete():
    c = make_client()
    tid = c.post("/tasks", json={"title": "Temp"}).get_json()["id"]
    assert c.delete(f"/tasks/{tid}").status_code == 200
    assert c.get(f"/tasks/{tid}").status_code == 404
