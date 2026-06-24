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

## Quick start (employers — no API keys)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Default question is pre-filled. Click **Analyze** — works offline with demo corpus.

| | URL |
|---|-----|
| **Web UI** | http://localhost:8501 |

CLI:

```bash
python src/scrape.py --url "https://example.com/press-release"
python src/embed.py
python src/query.py --question "What are competitors doing in Q1?"
```

---

## License

MIT — see [LICENSE](LICENSE).
