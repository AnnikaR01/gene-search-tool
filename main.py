from Bio import Entrez

Entrez.email = "2ezfried@gmail.com"

def search_gene_id(symbol, organism="Homo sapiens"):
    term = f"{symbol}[sym] AND {organism}[orgn]"
    handle = Entrez.esearch(db="gene", term=term)
    record = Entrez.read(handle)
    if len(record["IdList"])== 0:
        raise ValueError(f"No gene found for symbol '{symbol}' in {organism}")
    return record["IdList"][0]

def get_gene_summary(gene_id):
    handle = Entrez.esummary(db="gene", id=gene_id)
    record = Entrez.read(handle)
    doc = record["DocumentSummarySet"]["DocumentSummary"][0]
    return {
        "symbol": doc["Name"],
        "description": doc["Description"],
        "chromosome": doc.get("Chromosome", "unknown"),
        "map_location": doc.get("MapLocation", "unknown"),
        "summary": doc.get("Summary", ""),
    }

import time 

def search_gene(symbol, organism="Homo sapiens"):
    gene_id = search_gene_id(symbol, organism)
    time.sleep(0.34)
    return get_gene_summary(gene_id)

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
    args = parser.parse_args()

    try:
        result = search_gene(args.symbol)
        print_report(result)
    except ValueError as e:
        print(f"Error: {e}")
    except urllib.error.URLError as e:
        print(f"Network error reaching NCBI: {e}")