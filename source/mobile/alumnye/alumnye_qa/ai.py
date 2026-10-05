"""AI backends. `claude` (default) calls the Claude Code CLI in headless mode with the account that is already logged in
on this machine - no API key. `qwen` calls a local Ollama model. Both return one parsed JSON object.
Used only when the deterministic recovery cannot move on - never during a normal passing run."""
import json
import re
import shutil
import subprocess
import tempfile

import requests

SYSTEM = ("You are the recovery assistant of a mobile UI test runner. Answer with ONE JSON object and nothing else - "
          "no prose, no markdown fences.")


def backend(cfg: dict) -> str:
    return cfg["ai"].get("backend", "claude")


def model(cfg: dict) -> str:
    ai = cfg["ai"]
    return ai.get("claude_model", "haiku") if backend(cfg) == "claude" else ai.get("model", "qwen3:4b")


def label(cfg: dict) -> str:
    return f"{backend(cfg)} ({model(cfg)})"


def _json_from(text: str) -> dict:
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        raise ValueError(f"no JSON in AI reply: {(text or '')[:120]!r}")
    return json.loads(m.group(0))


def ask_json(cfg: dict, prompt: str) -> dict:
    if backend(cfg) == "claude":
        exe = shutil.which("claude")
        if not exe:
            raise RuntimeError("Claude Code CLI ('claude') not found on PATH")
        r = subprocess.run(
            [exe, "-p", "--model", model(cfg), "--tools", "", "--no-session-persistence", "--disable-slash-commands",
             "--system-prompt", SYSTEM],
            input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=150,
            cwd=tempfile.gettempdir())          # neutral folder: no project files / CLAUDE.md are picked up
        if r.returncode != 0 and not r.stdout.strip():
            raise RuntimeError(f"claude CLI failed: {(r.stderr or '').strip()[:200]}")
        return _json_from(r.stdout)
    ai = cfg["ai"]
    body = {"model": ai["model"], "stream": False, "think": False, "format": "json", "keep_alive": "30m",
            "options": {"temperature": 0, "num_ctx": 2048, "num_predict": 120},
            "messages": [{"role": "user", "content": prompt}]}
    resp = requests.post(ai["url"].rstrip("/") + "/api/chat", json=body, timeout=180)
    resp.raise_for_status()
    return _json_from(resp.json()["message"]["content"])


def available(cfg: dict) -> bool:
    if backend(cfg) == "claude":
        return shutil.which("claude") is not None
    try:
        r = requests.get(cfg["ai"]["url"].rstrip("/") + "/api/tags", timeout=3)
        return r.ok and any(m["name"].startswith(cfg["ai"]["model"].split(":")[0]) for m in r.json().get("models", []))
    except Exception:
        return False


def warm_up(cfg: dict):
    """Only the local model benefits from pre-loading."""
    if backend(cfg) != "qwen":
        return
    import threading

    def _go():
        try:
            requests.post(cfg["ai"]["url"].rstrip("/") + "/api/generate",
                          json={"model": cfg["ai"]["model"], "prompt": "ok", "stream": False, "keep_alive": "30m",
                                "options": {"num_predict": 1}}, timeout=180)
        except Exception:
            pass
    threading.Thread(target=_go, daemon=True).start()
