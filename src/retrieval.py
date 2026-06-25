"""Local corpus retrieval for RAG (no vector DB required for demo)."""

from __future__ import annotations

import json
import re
from pathlib import Path

_DEMO_CORPUS = Path(__file__).resolve().parents[1] / "data" / "sample_corpus.json"


def load_corpus() -> list[dict]:
    if _DEMO_CORPUS.exists():
        return json.loads(_DEMO_CORPUS.read_text(encoding="utf-8"))
    return []


def search_corpus(question: str, docs: list[dict] | None = None, top_k: int = 5) -> list[dict]:
    docs = docs if docs is not None else load_corpus()
    if not docs:
        return []

    tokens = set(re.findall(r"[a-z0-9]+", question.lower()))
    scored: list[tuple[int, dict]] = []
    for doc in docs:
        text = doc.get("text", "").lower()
        tag_text = " ".join(doc.get("tags", [])).lower()
        score = sum(1 for t in tokens if t in text or t in tag_text)
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    hits = [d for s, d in scored[:top_k] if s > 0]
    return hits or [d for _, d in scored[:top_k]]


def format_context(hits: list[dict]) -> str:
    return "\n".join(f"- {h['text']}" for h in hits)
