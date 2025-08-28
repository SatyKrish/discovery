import sys
import types
from pathlib import Path

# Stub optional OpenAI model to avoid heavy dependencies
openai_stub = types.ModuleType("openai_model")
openai_stub.get_default_model = lambda: None
openai_stub.openai_model = None
sys.modules["openai_model"] = openai_stub

# Provide a minimal Temporal client stub to avoid heavy dependency
temporalio_stub = types.ModuleType("temporalio")
client_stub = types.ModuleType("temporalio.client")
client_stub.Client = object
temporalio_stub.client = client_stub
sys.modules["temporalio"] = temporalio_stub
sys.modules["temporalio.client"] = client_stub

# Stub the DeepAgentWorkflow module to prevent heavy Temporal imports
workflow_mod = types.ModuleType("temporal.temporal_workflow")

class StubWorkflow:
    @staticmethod
    async def run(*args, **kwargs):
        ...

    @staticmethod
    async def user_prompt(*args, **kwargs):
        ...

    @staticmethod
    async def confirm(*args, **kwargs):
        ...

    @staticmethod
    async def end_chat(*args, **kwargs):
        ...

    @staticmethod
    async def get_conversation_history(*args, **kwargs):
        ...

DeepAgentWorkflow = StubWorkflow
workflow_mod.DeepAgentWorkflow = DeepAgentWorkflow
sys.modules["temporal.temporal_workflow"] = workflow_mod

# Ensure api module is importable
sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[1] / "temporal"))
import api  # noqa: E402
from fastapi.testclient import TestClient
import pytest

# Remove stubs so other tests can import real modules
sys.modules.pop("temporalio", None)
sys.modules.pop("temporalio.client", None)
sys.modules.pop("temporal.temporal_workflow", None)


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
    async def start_workflow(self, wf, *args, **kwargs):
        # Support SDK style: start_workflow(wf, *, args=[...], id=..., task_queue=...)
        if 'args' in kwargs:
            _ = kwargs['args']  # unused, but mimics signature
        dummy_handle.id = kwargs.get('id', dummy_handle.id)
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
