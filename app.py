import streamlit as st

from src.query import query_rag

st.set_page_config(page_title="Market Intelligence", layout="wide")
st.title("LLM-Driven Market Intelligence")

question = st.text_input("Ask a market intelligence question:")
if question and st.button("Analyze"):
    with st.spinner("Fetching insights..."):
        st.success(query_rag(question))
