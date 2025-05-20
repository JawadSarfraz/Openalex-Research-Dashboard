import csv
import psycopg2
from datetime import datetime

DB_NAME = "ai_research_db"
DB_USER = "ai_user"
DB_PASSWORD = "your_password"  # Optional if .pgpass or ident is set
DB_HOST = "localhost"

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

def fetch_data():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, publication_date, country, citation_count
        FROM publications
        WHERE publication_date IS NOT NULL
        AND publication_date::text != 'Unknown'
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def generate_csv(records):
    output_file = "data-analysis/vosviewer_dimensions_data.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Write header as per Dimensions format
        writer.writerow(["Title", "Year", "Authors", "Source title", "Volume", "Issue", "Pages", "DOI", "Affiliations", "Citations", "Field of study", "Country"])

        for title, pub_date, country, citations in records:
            try:
                # Extract year only
                year = pub_date.year if hasattr(pub_date, "year") else datetime.strptime(pub_date, "%Y-%m-%d").year
            except Exception:
                continue  # Skip rows with bad date formats

            # Fill with dummy or unknowns for unused columns
            writer.writerow([
                title,
                year,
                "Unknown",     # Authors
                "Unknown",     # Source title
                "", "", "",    # Volume, Issue, Pages
                "",            # DOI
                "",            # Affiliations
                citations,
                "AI",          # Field of study (optional customization)
                country
            ])

    print(f"✅ CSV exported successfully to {output_file}")

if __name__ == "__main__":
    records = fetch_data()
    generate_csv(records)
