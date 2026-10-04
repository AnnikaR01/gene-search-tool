import streamlit as st
from main import search_gene_id, get_candidates, get_gene_summary, fetch_gene_sequence

st.title("Gene Search Tool")

symbol = st.text_input("Enter a gene symbol (e.g. BRCA1)")

if symbol:
    id_list = search_gene_id(symbol, "Homo sapiens")

    if len(id_list) == 1:
        gene_id = id_list[0]
    else:
        docs = get_candidates(id_list)
        options = [f"{doc['Name']} - {doc['Description']} (chromosome {doc.get('Chromosome', 'unknown')})" for doc in docs]
        choice = st.selectbox("Multiple matches found — which one did you mean?", options)
        gene_id = id_list[options.index(choice)]

    result = get_gene_summary(gene_id)
    st.write(f"**Symbol:** {result['symbol']}")
    st.write(f"**Description:** {result['description']}")
    st.write(f"**Chromosome:** {result['chromosome']}")
    st.write(f"**Map location:** {result['map_location']}")
    st.write(f"**Summary:** {result['summary']}")

    if st.checkbox("Also fetch reference mRNA sequence"):
        seq_record = fetch_gene_sequence(gene_id)
        fasta_text = seq_record.format("fasta")
        st.write(f"Sequence length: {len(seq_record.seq)} bases")
        st.download_button("Download FASTA", data=fasta_text, file_name=f"{symbol}.fasta", mime="text/plain")
