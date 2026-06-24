"""RAG query pipeline — live APIs or offline demo corpus."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

_DEMO_CORPUS = Path(__file__).resolve().parents[1] / "data" / "sample_corpus.json"


def _load_corpus() -> list[dict]:
    if _DEMO_CORPUS.exists():
        return json.loads(_DEMO_CORPUS.read_text(encoding="utf-8"))
    return [
        {
            "id": "1",
            "text": "Competitor FinPay launched instant cross-border settlements in Q1 2026.",
            "tags": ["payments", "launch"],
        },
        {
            "id": "2",
            "text": "Rival BankCo announced AI fraud detection for SMB accounts in March 2026.",
            "tags": ["fraud", "AI", "SMB"],
        },
        {
            "id": "3",
            "text": "Market leader PaySphere expanded into Canadian payroll integrations.",
            "tags": ["payroll", "expansion"],
        },
    ]


def _demo_search(question: str, docs: list[dict], top_k: int = 3) -> list[dict]:
    tokens = set(re.findall(r"[a-z0-9]+", question.lower()))
    scored = []
    for doc in docs:
        text = doc.get("text", "").lower()
        score = sum(1 for t in tokens if t in text)
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for s, d in scored[:top_k] if s > 0] or [d for _, d in scored[:top_k]]


def _demo_answer(question: str) -> str:
    docs = _load_corpus()
    hits = _demo_search(question, docs)
    bullets = "\n".join(f"- {h['text']}" for h in hits)
    return (
        f"**Demo mode** (no API keys required)\n\n"
        f"**Question:** {question}\n\n"
        f"**Relevant market signals:**\n{bullets}\n\n"
        f"**Insight:** Competitors are accelerating AI-powered payments and fraud features. "
        f"Consider highlighting your differentiation in cross-border speed and SMB onboarding."
    )


def query_rag(question: str) -> str:
    """Answer a market intelligence question (live RAG or demo fallback)."""
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("PINECONE_API_KEY"):
        return _demo_answer(question)

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
    return resp.choices[0].message.content or ""


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    args = parser.parse_args()
    print(query_rag(args.question))
