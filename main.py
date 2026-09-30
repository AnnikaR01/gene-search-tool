from Bio import Entrez, SeqIO
import json

Entrez.email = "2ezfried@gmail.com"
CACHE_FILE = "gene_cache.json"

def search_gene_id(symbol, organism="Homo sapiens"):
    term = f"{symbol}[sym] AND {organism}[orgn]"
    handle = Entrez.esearch(db="gene", term=term)
    record = Entrez.read(handle)
    if len(record["IdList"])== 0:
        raise ValueError(f"No gene found for symbol '{symbol}' in {organism}")
    return record["IdList"]

def choose_gene_id(id_list, symbol):
    if len(id_list) == 1:
        return id_list[0]

    handle = Entrez.esummary(db="gene", id=",".join(id_list))
    record = Entrez.read(handle)
    docs = record["DocumentSummarySet"]["DocumentSummary"]

    print(f"Multiple matches found for '{symbol}':")
    for i , doc in enumerate(docs, start=1):
        print(f"{i}. {doc['Name']} - {doc['Description']} (chromosome {doc.get('Chromosome', 'unknown')})")

    choice = input("Which one did you mean? Enter a number: ")
    return id_list[int(choice) - 1]

def get_gene_summary(gene_id):
    handle = Entrez.esummary(db="gene", id=gene_id)
    record = Entrez.read(handle)
    doc = record["DocumentSummarySet"]["DocumentSummary"][0]
    return {
        "gene_id": gene_id,
        "symbol": doc["Name"],
        "description": doc["Description"],
        "chromosome": doc.get("Chromosome", "unknown"),
        "map_location": doc.get("MapLocation", "unknown"),
        "summary": doc.get("Summary", ""),
    }
def fetch_gene_sequence(gene_id):
    link_handle = Entrez.elink(dbfrom="gene", db="nucleotide", id=gene_id, linkname="gene_nuccore_refseqrna")
    link_record = Entrez.read(link_handle)
    nuc_id = link_record[0]["LinkSetDb"][0]["Link"][0]["Id"]

    seq_handle = Entrez.efetch(db="nucleotide", id=nuc_id, rettype="fasta", retmode="text")
    seq_record = SeqIO.read(seq_handle, "fasta")
    seq_handle.close()
    return seq_record

def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

import time 

def search_gene(symbol, organism="Homo sapiens"):
    cache = load_cache()
    cache_key = f"{symbol}_{organism}"
    if cache_key in cache:
        print("(from cache)")
        return cache[cache_key]

    id_list = search_gene_id(symbol, organism)
    gene_id = choose_gene_id(id_list, symbol)
    time.sleep(0.34)
    summary = get_gene_summary(gene_id)

    cache[cache_key] = summary
    save_cache(cache)
    print("(fresh API call)")
    return summary
def print_report(gene):
    print(f"Symbol: {gene['symbol']}")
    print(f"Description: {gene['description']}")
    print(f"Chromosome: {gene['chromosome']}")
    print(f"Map location: {gene['map_location']}")
    print(f"Summary: {gene['summary']}")

if __name__ == "__main__":
    import argparse
    import urllib.error

    parser = argparse.ArgumentParser(description="Look up a gene from NCBI")
    parser.add_argument("symbol", help="Gene symbol to search for, e.g. BRCA1")
    parser.add_argument("--organism", default="Homo sapiens", help="Organism to search, e.g. 'Mus musculus'")
    parser.add_argument("--sequence", action="store_true", help="Also fetch and save the gene's reference mRNA sequence as FASTA")
    args = parser.parse_args()

    try:
        result = search_gene(args.symbol,args.organism)
        print_report(result)
        if args.sequence:
            seq_record = fetch_gene_sequence(result["gene_id"])
            filename = f"{args.symbol}.fasta"
            SeqIO.write(seq_record, filename, "fasta")
            print(f"Sequence saved to {filename} ({len(seq_record.seq)} bases)")
    except ValueError as e:
        print(f"Error: {e}")
    except urllib.error.URLError as e:
        print(f"Network error reaching NCBI: {e}")