"""Embedding generation and Pinecone upsert."""

import os

from openai import OpenAI
from pinecone import Pinecone

from src.scrape import scrape_url

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_index():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    return pc.Index(os.getenv("PINECONE_INDEX", "market-intel"))


def embed_text(text: str, doc_id: str = "doc1") -> None:
    """Generate embedding and store in Pinecone."""
    emb = client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding
    get_index().upsert(vectors=[{"id": doc_id, "values": emb, "metadata": {"text": text[:1000]}}])


if __name__ == "__main__":
    sample = "Competitor announces new payments product."
    embed_text(sample)
    print("Stored in Pinecone.")
