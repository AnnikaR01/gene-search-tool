# Gene Search Tool — a command-line tool that takes a gene symbol and pulls back real biological data from NCBI

**Assumes:** Some prior Python exposure (variables, loops, conditionals, functions feel at least somewhat familiar from prior projects) — no separate fundamentals track, straight into domain phases.
**Structure:** 8 phases + capstone, strictly sequential — each phase's build is the starting point for the next phase's code, the same way the Flappy Bird project grew incrementally rather than being rewritten each time.

**The API:** [NCBI Entrez / E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) — the standard entry point into NCBI's databases (Gene, Nucleotide, Protein, PubMed, and more), free, no account required. Two real, verified constraints we'll actually respect in the code (not invented): NCBI asks that every request identify a contact email/tool name, and enforces a rate limit of **3 requests/second without an API key, 10/second with one** ([NCBI Insights](https://ncbiinsights.ncbi.nlm.nih.gov/2018/08/14/release-plan-for-e-utility-api-keys/)).

## Phase 0 — Setup + your first raw API call
**Question:** What does "calling an API" actually look like under the hood, before any library smooths it over?
**New skills:** `uv init`/`uv add`, making an HTTP GET request, reading a raw response body, why NCBI wants an email/tool name identifying your requests.
**Tools:** `requests` (`uv add requests` — already installed).
**Build:** A script that hits NCBI's `esearch` endpoint directly with a hardcoded gene symbol (e.g. `"BRCA1"`) using `requests.get()`, prints the raw response text, and pulls the gene ID out by hand (basic string work) — no XML parser yet.
**Stretch (optional):** Add `&retmode=json` to the request URL and compare how much easier `json.loads()` makes pulling out the ID versus the raw XML string.

## Phase 1 — A proper client: Biopython's Entrez module (extends Phase 0)
**Question:** Now that you've felt the raw HTTP call, what does a real domain-specific library actually save you from doing by hand?
**New skills:** installing and using a real bioinformatics library, `Entrez.esearch()`, `Entrez.read()`, writing a function with parameters and a return value.
**Tools:** `biopython` (`uv add biopython`).
**Build:** A function `search_gene_id(symbol, organism)` that uses `Entrez.esearch(db="gene", ...)` and `Entrez.read()` to return a real NCBI gene ID — replacing Phase 0's manual string parsing with something that actually works reliably.
**Stretch:** Also print the total `Count` of matches Entrez found, not just the first ID.

## Phase 2 — Pulling the real record: esummary (extends Phase 1)
**Question:** Once you have an ID, how do you get the actual, human-readable information about that gene?
**New skills:** `Entrez.esummary()`, navigating a nested dict/list structure, using `.get()` for safe access instead of assuming a key exists.
**Tools:** `Bio.Entrez` (same).
**Build:** A function `get_gene_summary(gene_id)` returning a dict with the official symbol, full name, chromosome location, and description. Combine Phase 1 + Phase 2 into one `search_gene("BRCA1")` pipeline function that goes symbol → ID → summary in one call.
**Stretch:** Also pull the `OtherAliases` field and display any known alternate names for the gene.

## Phase 3 — A real CLI (extends Phase 2)
**Question:** How does this go from "a script I edit every time" to "a tool I actually run with different input"?
**New skills:** command-line arguments (`argparse`), formatting a dict into readable multi-line output.
**Tools:** `argparse` (stdlib, no install needed).
**Build:** `uv run main.py TP53` prints a formatted report. Running with no arguments (or a `-h`) shows a clear usage message instead of crashing.
**Stretch:** Support multiple symbols in one call (`uv run main.py TP53 BRCA1 EGFR`), printing a report for each.

## Phase 4 — When things go wrong (extends Phase 3)
**Question:** Real users mistype things and networks fail — what should actually happen instead of a traceback?
**New skills:** `try`/`except`, catching specific exception types, validating input before it hits the network, basic retry/backoff reasoning.
**Tools:** same, plus respecting NCBI's real documented rate limit (3 req/sec without a key — this matters directly if Phase 3's stretch is in place, since several lookups in a row can trip it).
**Build:** Handle three real failure cases gracefully, each with a clear message instead of a crash: gene not found, ambiguous/misspelled symbol, and a simulated network failure. Add a small delay between requests so a multi-gene lookup stays under the rate limit.
**Stretch:** Read an NCBI API key from an environment variable if one is set, and use it to raise the allowed rate.

## Phase 5 — Caching results locally (extends Phase 4)
**Question:** Why hit the network again for a gene you already looked up five minutes ago?
**New skills:** file I/O, the `json` module for structured storage, handling "this file doesn't exist yet" (first run).
**Tools:** `json` (stdlib).
**Build:** Before calling the API, check a local `gene_cache.json`; if the gene's already there, use it — if not, fetch it and save it. Print whether a result came from cache or a fresh API call.
**Stretch:** Add a `--refresh` flag that forces a fresh API call even when a cached result exists.

## Phase 6 — Handling ambiguous, multi-result searches (extends Phase 5)
**Question:** What happens when a gene symbol matches more than one real thing (different species, deprecated names, etc.)?
**New skills:** working with a list of results instead of assuming one, filtering by a field, simple interactive selection with `input()`.
**Tools:** same.
**Build:** When `esearch` returns multiple gene IDs, show a short numbered list (symbol + organism) and let the user pick one, instead of silently grabbing the first result.
**Stretch:** Add a `--organism` flag (e.g. `"human"`, `"mouse"`) that filters results automatically instead of asking interactively.

## Phase 7 — Real sequence data (extends Phase 6)
**Question:** A gene record so far is metadata — where's the actual biology?
**New skills:** `efetch` against a different database (nucleotide/protein), the FASTA format, writing a `.fasta` file.
**Tools:** `Bio.Entrez.efetch(db="nucleotide", rettype="fasta", ...)`, `Bio.SeqIO` (given directly — real, specific Biopython API).
**Build:** Add a `--sequence` flag that fetches the gene's reference mRNA sequence, saves it as a real `.fasta` file, and prints its length.
**Stretch:** Compute and print the sequence's %GC content — a real, checkable biology metric — from the fetched sequence.

## Capstone — pick one (each combines Phases 3–7)
1. **Gene Report Card** — the "do it really well" option: a polished CLI with robust error handling, caching, sequence fetch, and a clean, multi-section formatted report.
2. **Gene Knowledge Base** — swap the JSON cache for a small local SQLite database of every gene you've ever looked up, plus a `--list` command to browse your search history.
3. **Mini Web Front-End** — wrap the whole tool in a simple [Streamlit](https://streamlit.io/) app: a text box, a search button, and a laid-out results page instead of a terminal report.

## Pacing

| Phase | Focus | Depends on |
|---|---|---|
| 0 | Raw API call | — |
| 1 | Biopython Entrez client | 0 |
| 2 | Parsing the real record | 1 |
| 3 | CLI | 2 |
| 4 | Error handling + rate limits | 3 |
| 5 | Local caching | 4 |
| 6 | Ambiguous results | 5 |
| 7 | Sequence data | 6 |
| Capstone | Pick one | 3, 4, 5, 6, 7 |

## Review

One comprehensive review happens after the capstone, not after each phase — grouped by topic (HTTP/requests basics, the Entrez search → summary → fetch workflow, error handling, caching, sequence data), starting with concrete "what does this code do" questions before any abstract ones. Any real gaps it uncovers get short, targeted hands-on practice — not a generic re-teach of everything.
