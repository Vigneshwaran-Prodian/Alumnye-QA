"""Tier 3 - AI recovery prompts. (File name kept for history; the backend is chosen in config.json -> ai.backend:
'claude' = Claude Code CLI with the logged-in account, 'qwen' = local Ollama.) The AI advises; the runner performs
every action and validates the advice before using it."""
import datetime

from . import ai, config

PROMPT = """A mobile UI test runner is stuck. A required element was not found on screen.
Step intent: {intent}
Element wanted: "{key}" ({kind}) - {desc}
Expected labels: {labels}
Visible elements (index|class|label|flags):
{ui}

Decide ONE of:
- "found": one of the listed elements is clearly the wanted element (moved/renamed). Give its index.
- "bug": the wanted option is truly gone from this screen, so this is likely a real functionality defect.
- "human": you cannot tell.
Reply with JSON only: {{"verdict":"found|bug|human","node_index":<int or null>,"reason":"<one short sentence>"}}"""

ACTION_PROMPT = """A mobile UI test is stuck: an action had no visible effect.
Goal: {goal}
Already tried without effect: {tried}
{extra}
Screen elements (index|class|label|flags|@centreX,centreY):
{ui}

Choose ONE next action. Reply with JSON only:
{{"action":"tap|type|scroll_down|scroll_up|wait|back|give_up","node_index":<int or null>,"text":"<text to type, only for type>","reason":"<one short sentence>"}}
- type: set node_index to an input field and text to a realistic valid value for it (required fields marked * must be filled).
- tap: set node_index to the element to tap (an icon right next to a text such as 'I accept' is usually its checkbox).
- If the keyboard is visible, a tap on something else is usually swallowed: use back to close the keyboard first.
- Do NOT repeat an action that is already listed as tried.
- give_up: use this if the control looks present but unresponsive (a likely app defect).
Keep the reason under 15 words."""


FIX_PROMPT = """A mobile form field was rejected by the app's validation.
Field: {label}
Value that was entered: {value}
Error text shown by the app: {error}
Other values already tried for this field: {tried}

Interpret the error (what exactly is wrong) and give ONE new, different, realistic test value that should pass.
Rules: a phone number must be a 10-digit Indian mobile starting with 6, 7, 8 or 9; if the error says the value is already registered or taken, give a completely different unique value of the same format; never reuse a tried value.
Reply with JSON only: {{"understood":"<what the error means, under 15 words>","value":"<the new value>"}}"""


def ask_fix(cfg: dict, label: str, value: str, error: str, tried: list) -> dict:
    out = ai.ask_json(cfg, FIX_PROMPT.format(label=label or "unknown", value=value, error=error, tried=", ".join(tried) or "none"))
    if not isinstance(out.get("value"), (str, int)) or not str(out.get("value")).strip():
        out = {"understood": "unparseable AI reply", "value": ""}
    out["value"] = str(out["value"]).strip()
    return out


def ask(cfg: dict, intent: str, key: str, kind: str, desc: str, labels: list, ui: str) -> dict:
    out = ai.ask_json(cfg, PROMPT.format(intent=intent, key=key, kind=kind, desc=desc, labels=labels or "n/a", ui=ui))
    if out.get("verdict") not in ("found", "bug", "human"):
        out = {"verdict": "human", "node_index": None, "reason": "unparseable AI reply"}
    return out


def ask_action(cfg: dict, goal: str, tried: list, ui: str, extra: str = "") -> dict:
    out = ai.ask_json(cfg, ACTION_PROMPT.format(goal=goal, tried="; ".join(tried) or "nothing", ui=ui, extra=extra))
    if out.get("action") not in ("tap", "type", "scroll_down", "scroll_up", "wait", "back", "give_up"):
        out = {"action": "give_up", "node_index": None, "reason": "unparseable AI reply"}
    return out


def available(cfg: dict) -> bool:
    return ai.available(cfg)


def warm_up(cfg: dict):
    ai.warm_up(cfg)


def log_usage(run_id: str, scenario: str, trigger: str, outcome: str):
    """One line per real AI invocation (RULES section 4 / ai_usages)."""
    line = f"| {datetime.date.today()} | {run_id} | {scenario} | {trigger} | {outcome} |\n"
    with open(config.AI_LOG, "a", encoding="utf-8") as f:
        f.write(line)
