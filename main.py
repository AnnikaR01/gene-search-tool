from Bio import Entrez

Entrez.email = "2ezfried@gmail.com"

def search_gene_id(symbol, organism="Homo sapiens"):
    term = f"{symbol}[sym] AND {organism}[orgn]"
    handle = Entrez.esearch(db="gene", term=term)
    record = Entrez.read(handle)
    return record["IdList"][0]
if __name__ == "__main__":
    gene_id = search_gene_id("BRCA1")
    print(gene_id)