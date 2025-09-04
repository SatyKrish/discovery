# ──────────────────────────────────────────────────────────────────────────────
# File: src/tools/registry.py
# Generic MCP registry (stdio + HTTP) for tools & prompt packs
# ──────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
from typing import Any, Dict, List, Optional
import logging, subprocess, json, os
from src.config import settings
try:
    import requests
except Exception:
    requests = None

log = logging.getLogger(__name__)

class Provider:
    name: str
    def discover_tools(self) -> List[Dict[str, Any]]: ...
    def invoke(self, tool_name: str, args: Dict[str, Any]) -> Any: ...
    def list_prompts(self) -> List[str]: ...
    def get_prompt(self, prompt_id: str) -> Optional[Dict[str, Any]]: ...

# ------------------------------ stdio provider -------------------------------

class StdioProvider(Provider):
    def __init__(self, name: str, cmd: List[str], cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None):
        self.name, self.cmd, self.cwd, self.env = name, cmd, cwd, env or {}

    def _rpc(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        p = subprocess.Popen(self.cmd, cwd=self.cwd, env={**os.environ, **(self.env or {})},
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            p.stdin.write(json.dumps(payload) + "\n"); p.stdin.flush()
            line = p.stdout.readline()
            return json.loads(line.strip() or "{}")
        finally:
            try: p.terminate()
            except Exception: pass

    def discover_tools(self) -> List[Dict[str, Any]]:
        try:
            tools = self._rpc({"method":"tools.list"}).get("tools", []) or []
            for t in tools:
                t["name"] = f"{self.name}/{t['name']}"
            return tools
        except Exception as e:
            log.warning("stdio discover failed %s: %s", self.name, e); return []

    def invoke(self, tool_name: str, args: Dict[str, Any]) -> Any:
        local = tool_name.split("/",1)[1] if "/" in tool_name else tool_name
        resp = self._rpc({"method":"tools.invoke","name":local,"args":args})
        if "error" in resp: raise RuntimeError(resp["error"])
        return resp.get("data")

    def list_prompts(self) -> List[str]:
        try:
            ids = self._rpc({"method":"prompts.list"}).get("prompts", []) or []
            return [f"{self.name}/{pid}" for pid in ids]
        except Exception: return []

    def get_prompt(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        local = prompt_id.split("/",1)[1] if "/" in prompt_id else prompt_id
        try:
            js = self._rpc({"method":"prompts.get","id":local})
            # Expected: {"text": str, "tools": [str], "safety_notes": str, "best_practices": str}
            return js if isinstance(js, dict) else None
        except Exception: return None

# ------------------------------- http provider -------------------------------

class HttpProvider(Provider):
    def __init__(self, name: str, base_url: str, headers: Optional[Dict[str,str]] = None):
        if requests is None: raise RuntimeError("pip install requests")
        self.name, self.base, self.hdr = name, base_url.rstrip("/"), (headers or {})

    def discover_tools(self) -> List[Dict[str, Any]]:
        try:
            r = requests.get(f"{self.base}/tools", headers=self.hdr, timeout=15); r.raise_for_status()
            tools = r.json() or []
            for t in tools: t["name"] = f"{self.name}/{t['name']}"
            return tools
        except Exception as e:
            log.warning("http discover failed %s: %s", self.name, e); return []

    def invoke(self, tool_name: str, args: Dict[str, Any]) -> Any:
        local = tool_name.split("/",1)[1] if "/" in tool_name else tool_name
        r = requests.post(f"{self.base}/invoke", json={"name":local, "args":args}, headers=self.hdr, timeout=60)
        r.raise_for_status()
        js = r.json()
        if isinstance(js, dict) and js.get("error"): raise RuntimeError(js["error"])
        return js.get("data", js)

    def list_prompts(self) -> List[str]:
        try:
            r = requests.get(f"{self.base}/prompts", headers=self.hdr, timeout=15); r.raise_for_status()
            ids = r.json() or []
            return [f"{self.name}/{pid}" for pid in ids]
        except Exception: return []

    def get_prompt(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        local = prompt_id.split("/",1)[1] if "/" in prompt_id else prompt_id
        try:
            r = requests.get(f"{self.base}/prompts/{local}", headers=self.hdr, timeout=15); r.raise_for_status()
            js = r.json()
            return js if isinstance(js, dict) else None
        except Exception: return None

# ------------------------------- registry api --------------------------------

_PROVIDERS: Optional[List[Provider]] = None

def _providers() -> List[Provider]:
    global _PROVIDERS
    if _PROVIDERS is None:
        _PROVIDERS = []
        for cfg in settings.mcp_stdio:
            _PROVIDERS.append(StdioProvider(cfg["name"], cfg["cmd"], cfg.get("cwd"), cfg.get("env")))
        for cfg in settings.mcp_http:
            _PROVIDERS.append(HttpProvider(cfg["name"], cfg["base_url"], cfg.get("headers")))
    return _PROVIDERS

def mcp_discover_tools() -> List[Dict[str, Any]]:
    tools: List[Dict[str, Any]] = []
    for p in _providers(): tools.extend(p.discover_tools())
    seen=set(); out=[]
    for t in tools:
        if t["name"] in seen: continue
        seen.add(t["name"]); out.append(t)
    return out

def mcp_invoke_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if "/" in tool_name:
        prov,_ = tool_name.split("/",1)
        for p in _providers():
            if p.name == prov:
                try: return {"success": True, "data": p.invoke(tool_name, args)}
                except Exception as e: return {"success": False, "error": str(e)}
        return {"success": False, "error": f"Unknown provider {prov}"}
    for p in _providers():
        try: return {"success": True, "data": p.invoke(tool_name, args)}
        except Exception: continue
    return {"success": False, "error": f"Tool {tool_name} not found"}

def mcp_list_prompts() -> List[str]:
    ids: List[str] = []
    for p in _providers(): ids.extend(p.list_prompts())
    return sorted(set(ids))

def mcp_get_prompt(prompt_id: str) -> Dict[str, Any]:
    if "/" in prompt_id:
        prov,_ = prompt_id.split("/",1)
        for p in _providers():
            if p.name == prov:
                js = p.get_prompt(prompt_id)
                return {"success": bool(js), **({"text": js.get("text"),
                                                 "tools": js.get("tools", []),
                                                 "safety_notes": js.get("safety_notes",""),
                                                 "best_practices": js.get("best_practices","")}
                                                if js else {"error":"prompt not found"})}
        return {"success": False, "error": f"Unknown provider {prov}"}
    for p in _providers():
        js = p.get_prompt(prompt_id)
        if js:
            return {"success": True, "text": js.get("text"),
                    "tools": js.get("tools", []),
                    "safety_notes": js.get("safety_notes",""),
                    "best_practices": js.get("best_practices","")}
    return {"success": False, "error": f"prompt {prompt_id} not found"}
