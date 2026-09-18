import requests

def main():
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    gene_symbol = "BRCA1"

    params = {
        "db": "gene",
        "term": gene_symbol,
    }

    response = requests.get(base_url, params=params)
    print(response.text)

    chunks = response.text.split("<Id>")
    print(chunks[1])
    clean_id = chunks[1].split("</Id>")[0]
    print(clean_id)
if __name__ == "__main__":
    main()
