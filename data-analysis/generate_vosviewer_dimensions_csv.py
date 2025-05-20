import requests
import json
import csv
import os
from time import sleep

# Constants
RAW_DATA_DIR = "data-extraction/raw_data"
OUTPUT_CSV = "data-analysis/vosviewer_dimensions_data.csv"
CONCEPT_IDS = {
    "AI": "C154945302",
    "Deep Learning": "C108583219"
}
YEARS = list(range(2010, 2021))
PER_PAGE = 200
MAX_PAGES = 5  # adjust based on your quota and need

# Ensure folders exist
os.makedirs("data-analysis", exist_ok=True)


def fetch_works(concept_id, year):
    all_results = []
    for page in range(1, MAX_PAGES + 1):
        url = f"https://api.openalex.org/works?filter=concepts.id:{concept_id},publication_year:{year}&per-page={PER_PAGE}&page={page}"
        print(f"Fetching: {url}")
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Failed on page {page}: {res.status_code}")
            break

        data = res.json()
        results = data.get("results", [])
        if not results:
            break

        all_results.extend(results)
        sleep(1)  # Be polite to API
    return all_results


def extract_csv_data(raw_data, field_label):
    rows = []
    for item in raw_data:
        title = item.get("title", "No Title")
        pub_year = item.get("publication_year", "Unknown")
        if not isinstance(pub_year, int):
            pub_year = "Unknown"

        citation_count = item.get("cited_by_count", 0)

        # Authors
        authorships = item.get("authorships", [])
        authors = [auth.get("author", {}).get("display_name", "Unknown") for auth in authorships]
        authors_joined = "; ".join(authors) if authors else "Unknown"

        # Affiliations
        affiliations = []
        for auth in authorships:
            for inst in auth.get("institutions", []):
                name = inst.get("display_name")
                if name:
                    affiliations.append(name)
        affiliations_joined = "; ".join(set(affiliations)) if affiliations else "Unknown"

        # Country
        countries = []
        for auth in authorships:
            for inst in auth.get("institutions", []):
                country = inst.get("country_code")
                if country:
                    countries.append(country)
        countries_joined = ", ".join(set(countries)) or "Unknown"

        row = [
            title,
            pub_year,
            authors_joined,
            "Unknown",  # Source title
            "",  # Volume
            "",  # Issue
            "",  # Pages
            item.get("doi", ""),
            affiliations_joined,
            citation_count,
            field_label,
            countries_joined
        ]
        rows.append(row)
    return rows


def main():
    all_rows = []
    for label, concept_id in CONCEPT_IDS.items():
        for year in YEARS:
            raw = fetch_works(concept_id, year)
            print(f"Year {year} | {label} | {len(raw)} records")
            extracted = extract_csv_data(raw, label)
            all_rows.extend(extracted)

    # Write CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Year", "Authors", "Source title", "Volume", "Issue", "Pages", "DOI", "Affiliations", "Citations", "Field of study", "Country"])
        writer.writerows(all_rows)

    print(f"✅ CSV export successfully to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
