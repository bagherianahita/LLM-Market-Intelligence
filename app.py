import streamlit as st

from src.query import query_rag

st.set_page_config(page_title="Market Intelligence", layout="wide")
st.title("LLM-Driven Market Intelligence")
st.caption("Demo mode works without API keys — try the default question below.")

DEFAULT_QUESTION = "What are competitors doing in payments and fraud detection in Q1 2026?"

question = st.text_input("Ask a market intelligence question:", value=DEFAULT_QUESTION)
if st.button("Analyze", type="primary"):
    with st.spinner("Fetching insights..."):
        st.markdown(query_rag(question))
