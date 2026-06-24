"""RAG query pipeline for market intelligence."""

import os

from openai import OpenAI
from pinecone import Pinecone

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_index():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    return pc.Index(os.getenv("PINECONE_INDEX", "market-intel"))


def query_rag(question: str) -> str:
    """Retrieve similar docs and answer with GPT-4."""
    emb = client.embeddings.create(model="text-embedding-3-small", input=question).data[0].embedding
    results = get_index().query(vector=emb, top_k=3, include_metadata=True)

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
