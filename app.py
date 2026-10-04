import streamlit as st
from main import search_gene
st.title("Gene Search Tool")

symbol = st.text_input("Enter a gene symbol (e.g. BRCA1)")

if st.button("Search"):
    result = search_gene(symbol)
    st.write(f"**Symbol:** {result['symbol']}")
    st.write(f"**Description:** {result['description']}")
    st.write(f"**Chromosome:** {result['chromosome']}")
    st.write(f"**Map location:** {result['map_location']}")
    st.write(f"**Summary:** {result['summary']}")