# LLM-Driven Market Intelligence Tool

A market insights generator for a fintech startup that analyzes competitor **press releases, news, and filings** in near real-time.  
Built with **OpenAI GPT-4, LangChain, Pinecone, and Streamlit**.

---

##  Features
- Automated **scraping** of competitor press releases and news.
- **Vector embeddings** stored in Pinecone for fast similarity search.
- **Retrieval-Augmented Generation (RAG)** to ground GPT-4 outputs in verified sources.
- Interactive **Streamlit dashboard** for product & marketing teams.
- Automated synchronization jobs to ensure **fresh data**.

---

##  Project Structure
│── app.py # Streamlit dashboard
│── src/ # Pipeline modules
│── requirements.txt # Python dependencies
│── config.yaml # Config (API keys, Pinecone index, etc.)

LangChain: A framework designed to help developers build applications using Large Language Models. It provides tools to connect LLMs to other data sources and services.
Pinecone: A specialized database designed for storing and searching vector embeddings. It is optimized for finding similar data points very quickly.
Streamlit: An open-source framework for building interactive web applications for data science and machine learning.
