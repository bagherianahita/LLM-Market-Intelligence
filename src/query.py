"""RAG query pipeline — Ollama, OpenAI+Pinecone, or local corpus synthesis."""

from __future__ import annotations

from src.llm_backends import active_backend, query_with_backend


def query_rag(question: str) -> str:
    """Answer a market intelligence question using the best available backend."""
    return query_with_backend(question, active_backend())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    args = parser.parse_args()
    print(query_rag(args.question))
