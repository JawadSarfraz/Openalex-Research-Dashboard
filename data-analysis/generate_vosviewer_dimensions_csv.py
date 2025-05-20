import requests
import csv
import os
from time import sleep

# Constants
OUTPUT_CSV = "data-analysis/vosviewer_dimensions_data.csv"
CONCEPT_IDS = {
    "AI": "C154945302",
    "Deep Learning": "C108583219"
}
YEARS = list(range(2010, 2021))
PER_PAGE = 200
MAX_PAGES = 5  # Limit pages to avoid huge API load

# Ensure output directory exists
os.makedirs("data-analysis", exist_ok=True)


def fetch_works(concept_id, year):
    all_results = []
    for page in range(1, MAX_PAGES + 1):
        url = (
            f"https://api.openalex.org/works?"
            f"filter=concepts.id:{concept_id},publication_year:{year}"
            f"&per-page={PER_PAGE}&page={page}"
        )
        print(f"Fetching: {url}")
        try:
            res = requests.get(url, timeout=30)
            res.raise_for_status()
        except Exception as e:
            print(f"⚠️ Request failed: {e}")
            break

        data = res.json()
        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)
        sleep(1)
    return all_results


def extract_record(item, label):
    title = item.get("title", "No Title")
    year = item.get("publication_year", "Unknown")
    cited_by = item.get("cited_by_count", 0)
    doi = item.get("doi", "")
    source_title = item.get("host_venue", {}).get("display_name", "")
    volume = item.get("biblio", {}).get("volume", "")
    issue = item.get("biblio", {}).get("issue", "")
    
    authors = []
    affiliations = []
    country = "Unknown"

    for auth in item.get("authorships", []):
        name = auth.get("author", {}).get("display_name", "")
        if name:
            authors.append(name)

        insts = auth.get("institutions", [])
        for inst in insts:
            affil = inst.get("display_name", "")
            if affil:
                affiliations.append(affil)
            if inst.get("country_code"):
                country = inst["country_code"]

    return [
        title,
        year,
        ", ".join(authors),
        source_title,
        volume,
        issue,
        doi,
        ", ".join(affiliations),
        cited_by,
        label,
        country
    ]


def generate_csv():
    records = []
    for label, concept_id in CONCEPT_IDS.items():
        for year in YEARS:
            raw_data = fetch_works(concept_id, year)
            print(f"✅ {year} - {label}: {len(raw_data)} records")
            for item in raw_data:
                record = extract_record(item, label)
                records.append(record)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Title", "Year", "Authors", "Source title", "Volume",
            "Issue", "DOI", "Affiliations", "Citations",
            "Field of study", "Country"
        ])
        writer.writerows(records)
    print(f"\n✅ CSV export done: {OUTPUT_CSV}")


if __name__ == "__main__":
    generate_csv()
