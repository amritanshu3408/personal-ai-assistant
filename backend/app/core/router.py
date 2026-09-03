"""Simple intent router – can be expanded with embeddings later."""

from typing import Literal

Intent = Literal["chat", "pc_control", "browser", "memory", "system"]


def classify_intent(text: str) -> Intent:
    t = text.lower()
    if any(w in t for w in ["open ", "launch ", "start ", "type ", "clipboard", "run command"]):
        return "pc_control"
    if any(w in t for w in ["search ", "browse ", "website", "url ", "google "]):
        return "browser"
    if any(w in t for w in ["remember ", "recall ", "what did i", "my preference"]):
        return "memory"
    if any(w in t for w in ["cpu", "memory usage", "disk", "system info", "processes"]):
        return "system"
    return "chat"
