import sys
import types
from pathlib import Path

# Stub optional OpenAI model to avoid heavy dependencies
openai_stub = types.ModuleType("openai_model")
openai_stub.get_default_model = lambda: None
openai_stub.openai_model = None
sys.modules["openai_model"] = openai_stub

# Ensure api module is importable
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[1] / "temporal"))
import api  # noqa: E402
from fastapi.testclient import TestClient
import pytest


class DummyHandle:
    def __init__(self, wid: str = "wf-id"):
        self.id = wid
        self.signals = []
        self.history = []

    async def signal(self, func, *args):
        self.signals.append((func.__name__, args))

    async def query(self, func, *args):
        if func.__name__ == "get_conversation_history":
            return self.history
        return None


dummy_handle = DummyHandle()


class DummyClient:
    async def start_workflow(self, wf, question, instructions, tools, mcp_endpoints, id, task_queue):
        dummy_handle.id = id
        return dummy_handle

    def get_workflow_handle(self, workflow_id):
        return dummy_handle


def make_client():
    return DummyClient()


@pytest.fixture(autouse=True)
def patch_client(monkeypatch):
    async def fake_get_client():
        return make_client()

    monkeypatch.setattr(api, "get_temporal_client", fake_get_client)
    yield


def test_workflow_endpoints():
    dummy_handle.history = [{"user": "hi"}, {"assistant": "hello"}]
    client = TestClient(api.app)

    resp = client.post("/workflow/start", json={"question": "hi", "workflow_id": "wf1"})
    assert resp.status_code == 200
    assert resp.json()["workflow_id"] == "wf1"

    resp = client.post("/workflow/wf1/prompt", json={"prompt": "next"})
    assert resp.status_code == 200

    resp = client.post("/workflow/wf1/confirm", json={"data": {"ok": True}})
    assert resp.status_code == 200

    resp = client.post("/workflow/wf1/end")
    assert resp.status_code == 200

    resp = client.get("/workflow/wf1/history")
    assert resp.status_code == 200
    assert resp.json()["history"] == dummy_handle.history

    names = [n for n, _ in dummy_handle.signals]
    assert names == ["user_prompt", "confirm", "end_chat"]


def test_prompt_validation():
    client = TestClient(api.app)
    resp = client.post("/workflow/wf1/prompt", json={})
    assert resp.status_code == 422
