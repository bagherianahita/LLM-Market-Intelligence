# LLM-Driven Market Intelligence

**Real-time competitor and market insights** using RAG over press releases and news — built with OpenAI, Pinecone, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.37-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

---

## Architecture

```
┌──────────────┐   scrape    ┌──────────────┐   embed     ┌─────────────┐
│ News / PR    │ ──────────► │  src/scrape  │ ──────────► │ Pinecone    │
│ URLs         │             └──────────────┘             │ vector index│
└──────────────┘                                          └──────┬──────┘
                                                                 │ top-k
┌──────────────┐   Streamlit  ┌──────────────┐   RAG          │
│ Analyst UI   │ ◄─────────── │  app.py      │ ◄──────────────┘
└──────────────┘              │  src/query   │
                              └──────────────┘
```

---

## Project structure

```
LLM-Market-Intelligence/
├── app.py                 # Streamlit dashboard
├── src/
│   ├── scrape.py          # Web scraping
│   ├── embed.py           # Embeddings + Pinecone
│   └── query.py           # RAG pipeline
├── config.yaml.example
└── requirements.txt
```

---

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp config.yaml.example config.yaml   # add API keys via env vars
set OPENAI_API_KEY=sk-...
set PINECONE_API_KEY=...
streamlit run app.py
```

CLI:

```bash
python src/scrape.py --url "https://example.com/press-release"
python src/embed.py
python src/query.py --question "What are competitors doing in Q1?"
```

---

## License

MIT — see [LICENSE](LICENSE).
