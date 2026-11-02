import os
import tempfile

os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mkdtemp()}/test.db"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def test_full_crud_flow():
    with TestClient(app) as c:
        r = c.post("/tasks", json={"title": "  Learn FastAPI ", "description": "demo"})
        assert r.status_code == 201
        t = r.json()
        assert t["title"] == "Learn FastAPI" and t["completed"] is False

        assert c.get(f"/tasks/{t['id']}").status_code == 200
        assert c.put(f"/tasks/{t['id']}", json={"title": "Edited"}).json()["title"] == "Edited"
        assert c.patch(f"/tasks/{t['id']}/toggle").json()["completed"] is True

        assert len(c.get("/tasks?status=completed").json()) == 1
        assert len(c.get("/tasks?status=pending").json()) == 0

        assert c.delete(f"/tasks/{t['id']}").status_code == 204
        assert c.get(f"/tasks/{t['id']}").status_code == 404


def test_validation_errors():
    with TestClient(app) as c:
        assert c.post("/tasks", json={"title": "   "}).status_code == 422
        assert c.post("/tasks", json={}).status_code == 422
        assert c.get("/tasks?status=bogus").status_code == 422
        assert c.delete("/tasks/9999").status_code == 404
