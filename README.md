# LLM-Driven Market Intelligence

**Real-time competitor and market insights** using RAG over press releases and news — built with OpenAI, Pinecone, and Streamlit.
<img width="1562" height="641" alt="image" src="https://github.com/user-attachments/assets/f08cc972-d6e7-4c81-96f9-0592b44d1e10" />
<img width="1562" height="641" alt="image" src="https://github.com/user-attachments/assets/2589b897-ee71-4a80-8772-7f6318dbec49" />

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
streamlit run app.py --server.port 8506
```

Default question is pre-filled. Click **Analyze** — works offline with demo corpus.

| | URL |
|---|-----|
| **Web UI** | http://localhost:8506 |

CLI:

```bash
python src/scrape.py --url "https://example.com/press-release"
python src/embed.py
python src/query.py --question "What are competitors doing in Q1?"
```

---

## License

MIT — see [LICENSE](LICENSE).
