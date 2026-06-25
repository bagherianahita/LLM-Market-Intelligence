"""LLM backends: Ollama (free OSS), OpenAI+Pinecone, or local synthesis fallback."""

from __future__ import annotations

import os
import re
from typing import Literal

import requests

from src.retrieval import format_context, search_corpus

Backend = Literal["ollama", "openai", "local"]


def detect_ollama(base_url: str | None = None) -> tuple[bool, str | None]:
    base = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
    preferred = os.getenv("OLLAMA_MODEL", "llama3.2")
    try:
        resp = requests.get(f"{base}/api/tags", timeout=3)
        if not resp.ok:
            return False, None
        models = [m.get("name", "").split(":")[0] for m in resp.json().get("models", [])]
        if not models:
            return False, None
        if preferred in models or any(m.startswith(preferred) for m in models):
            return True, preferred
        return True, models[0]
    except (requests.RequestException, ValueError, KeyError):
        return False, None


def active_backend() -> Backend:
    if os.getenv("OPENAI_API_KEY") and os.getenv("PINECONE_API_KEY"):
        return "openai"
    ok, _ = detect_ollama()
    if ok:
        return "ollama"
    return "local"


def _build_prompt(question: str, context: str) -> str:
    return (
        "You are a market intelligence analyst. Answer using ONLY the evidence below.\n\n"
        f"Evidence:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Respond in markdown with exactly these sections:\n"
        "**Relevant market signals** — bullet list grounded in the evidence\n"
        "**Insight** — 2-3 actionable sentences for a product or strategy team\n"
        "Do not invent companies or facts beyond the evidence."
    )


def query_ollama(question: str, hits: list[dict]) -> str:
    base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    ok, model = detect_ollama(base)
    if not ok or not model:
        raise RuntimeError("Ollama is not running")

    context = format_context(hits)
    resp = requests.post(
        f"{base}/api/chat",
        json={
            "model": model,
            "messages": [{"role": "user", "content": _build_prompt(question, context)}],
            "stream": False,
        },
        timeout=120,
    )
    resp.raise_for_status()
    content = resp.json().get("message", {}).get("content", "").strip()
    if not content:
        raise RuntimeError("Empty response from Ollama")
    return f"**Powered by Ollama** (`{model}`)\n\n**Question:** {question}\n\n{content}"


def query_openai_pinecone(question: str) -> str:
    from openai import OpenAI
    from pinecone import Pinecone

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX", "market-intel"))

    emb = client.embeddings.create(model="text-embedding-3-small", input=question).data[0].embedding
    results = index.query(vector=emb, top_k=3, include_metadata=True)
    matches = results.get("matches") or []
    context = " ".join(m["metadata"].get("text", "") for m in matches if m.get("metadata"))
    prompt = f"Answer based only on context:\n\n{context}\n\nQ: {question}\nA:"
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
    )
    return f"**Powered by OpenAI + Pinecone**\n\n{resp.choices[0].message.content or ''}"


def query_local_synthesis(question: str, hits: list[dict]) -> str:
    """Dynamic offline synthesis from retrieved corpus (no LLM)."""
    bullets = format_context(hits)
    tags: set[str] = set()
    for hit in hits:
        tags.update(hit.get("tags", []))

    themes = ", ".join(sorted(tags)) if tags else "market activity"
    companies = []
    for hit in hits:
        text = hit.get("text", "")
        match = re.search(r"\b([A-Z][a-z]+(?:[A-Z][a-z]+)*)\b", text)
        if match:
            companies.append(match.group(1))

    company_line = ", ".join(dict.fromkeys(companies)) if companies else "Key competitors"
    q_lower = question.lower()

    if any(w in q_lower for w in ("fraud", "risk", "security")):
        angle = "fraud detection and risk controls"
    elif any(w in q_lower for w in ("payment", "pay", "settlement", "cross-border")):
        angle = "payments and settlement speed"
    elif any(w in q_lower for w in ("price", "pricing", "cost")):
        angle = "pricing and packaging"
    elif any(w in q_lower for w in ("payroll", "hr", "workforce")):
        angle = "payroll and workforce integrations"
    else:
        angle = themes

    insight = (
        f"Signals cluster around **{angle}**. {company_line} are moving quickly on "
        f"product launches and positioning. Prioritize messaging that contrasts your "
        f"strengths in {angle} and monitor follow-on announcements in the next quarter."
    )

    return (
        f"**Local RAG mode** (corpus search + synthesis — install [Ollama](https://ollama.com) for live LLM answers)\n\n"
        f"**Question:** {question}\n\n"
        f"**Relevant market signals:**\n{bullets}\n\n"
        f"**Insight:** {insight}"
    )


def query_with_backend(question: str, backend: Backend | Literal["auto"] | None = None) -> str:
    if backend in (None, "auto"):
        backend = active_backend()
    hits = search_corpus(question)

    if backend == "openai":
        return query_openai_pinecone(question)
    if backend == "ollama":
        return query_ollama(question, hits)
    return query_local_synthesis(question, hits)
