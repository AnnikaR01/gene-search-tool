from Bio import Entrez

Entrez.email = "2ezfried@gmail.com"

def search_gene_id(symbol, organism="Homo sapiens"):
    term = f"{symbol}[sym] AND {organism}[orgn]"
    handle = Entrez.esearch(db="gene", term=term)
    record = Entrez.read(handle)
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
def search_gene(symbol, organism="Homo sapiens"):
    gene_id = search_gene_id(symbol, organism)
    return get_gene_summary(gene_id)

def print_report(gene):
    print(f"Symbol: {gene['symbol']}")
    print(f"Description: {gene['description']}")
    print(f"Chromosome: {gene['chromosome']}")
    print(f"Map location: {gene['map_location']}")
    print(f"Summary: {gene['summary']}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Look up a gene from NCBI")
    parser.add_argument("symbol", help="Gene symbol to search for, e.g. BRCA1")
    args = parser.parse_args()

    result = search_gene(args.symbol)
    print_report(result)