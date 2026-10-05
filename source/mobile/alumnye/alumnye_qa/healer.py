"""Tier 2 — deterministic self-heal. No AI. Reads the live page source and looks for the same
element moved / renamed / restructured, by label similarity and control kind."""
import difflib
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass

INPUT_CLASSES = ("EditText", "TextField", "SecureTextField", "TextView")  # TextView only on iOS inputs
THRESHOLD = 0.72


@dataclass
class Node:
    idx: int
    cls: str
    label: str
    rid: str
    clickable: bool
    enabled: bool
    is_input: bool
    ordinal: int  # nth node of the same class
    cx: int = 0
    cy: int = 0
    checked: bool = False
    hint: str = ""


def snapshot(page_source: str, platform: str) -> list:
    root = ET.fromstring(page_source)
    nodes, counts = [], {}
    for el in root.iter():
        a = el.attrib
        if platform == "android":
            cls = a.get("class", "")
            label = (a.get("text") or a.get("content-desc") or "").strip().lstrip(",").strip()
            rid = a.get("resource-id", "")
            clickable = a.get("clickable") == "true"
            is_input = cls.endswith("EditText")
        else:
            cls = el.tag
            label = (a.get("label") or a.get("name") or a.get("value") or "").strip()
            rid = a.get("name", "")
            clickable = cls.endswith("Button") or cls.endswith("Cell") or cls.endswith("Switch")
            is_input = cls.endswith(("TextField", "SecureTextField", "TextView"))
        if not cls or (platform == "android" and "bounds" not in a):
            continue
        counts[cls] = counts.get(cls, 0) + 1
        cx = cy = 0
        if platform == "android":
            m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", a.get("bounds", ""))
            if m:
                x1, y1, x2, y2 = map(int, m.groups())
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        else:
            try:
                cx = int(float(a.get("x", 0)) + float(a.get("width", 0)) / 2)
                cy = int(float(a.get("y", 0)) + float(a.get("height", 0)) / 2)
            except ValueError:
                pass
        nodes.append(Node(len(nodes), cls, label, rid, clickable, a.get("enabled", "true") == "true",
                          is_input, counts[cls], cx, cy, "true" in (a.get("checked"), a.get("selected")),
                          (a.get("hint") or a.get("placeholderValue") or "").strip()))
    return nodes


def _sim(a: str, b: str) -> float:
    a, b = a.lower().strip(), b.lower().strip()
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if a in b or b in a:  # containment counts only when the two are of similar size
        short, long_ = sorted((len(a), len(b)))
        return 0.6 + 0.35 * short / long_
    return difflib.SequenceMatcher(None, a, b).ratio()


def strategy_for(node: Node, kind: str, platform: str) -> str:
    """Turn a found node into a locator strategy string."""
    if kind == "input":
        if platform == "android":
            return f"xpath:(//{node.cls})[{node.ordinal}]"
        return f"xpath:(//{node.cls})[{node.ordinal}]"
    if kind == "button" and node.label:
        return f"btnx:{node.label}"
    if node.label:
        return f"text:{node.label}"
    return f"xpath:(//{node.cls})[{node.ordinal}]"


def heal(nodes: list, labels: list, kind: str, platform: str):
    """Return (strategy, reason) or None."""
    pool = [n for n in nodes if n.enabled]
    if kind == "input":
        inputs = [n for n in pool if n.is_input]
        if labels:
            scored = sorted(((max(_sim(l, n.label) for l in labels), n) for n in inputs), key=lambda t: -t[0])
            if scored and scored[0][0] >= THRESHOLD:
                n = scored[0][1]
                return strategy_for(n, kind, platform), f"input matched by hint '{n.label}'"
        if len(inputs) == 1:
            return strategy_for(inputs[0], kind, platform), "only one input on screen"
        return None
    if not labels:
        return None
    if kind == "button":
        pool = [n for n in pool if n.clickable or n.label]
    best, best_score = None, 0.0
    for n in pool:
        if not n.label:
            continue
        s = max(_sim(l, n.label) for l in labels)
        if kind == "button" and not n.clickable:
            s -= 0.05  # prefer real controls, still allow the label text node
        if s > best_score:
            best, best_score = n, s
    if best is not None and best_score >= THRESHOLD:
        return strategy_for(best, kind, platform), f"label '{best.label}' ~ {labels} (score {best_score:.2f})"
    return None


def ui_summary(nodes: list, limit: int = 60, near_text: str = None, radius: int = 130) -> str:
    """Compact screen description for the AI. With near_text, only the elements on the same row as that text
    are listed (a small model chooses far better from 3 candidates than from a whole screen)."""
    if near_text:
        anchor = next((n for n in nodes if near_text.lower() in n.label.lower()), None)
        if anchor is not None:
            nodes = [n for n in nodes if abs(n.cy - anchor.cy) <= radius and n is not anchor
                     and (n.clickable or n.label)]
    rows = []
    for n in nodes:
        if n.label or n.is_input or n.clickable:
            lab = n.label[:60]
            if lab and all(0xE000 <= ord(c) <= 0xF8FF or ord(c) >= 0xF0000 for c in lab):
                lab = "(icon U+%04X)" % ord(lab[0])
            flags = ("tap " if n.clickable else "") + ("input " if n.is_input else "") + ("DISABLED " if not n.enabled else "") \
                + ("checked " if n.checked else "")
            rows.append(f"{n.idx}|{n.cls.split('.')[-1]}|{lab}|{flags.strip()}|@{n.cx},{n.cy}")
        if len(rows) >= limit:
            break
    return "\n".join(rows)
