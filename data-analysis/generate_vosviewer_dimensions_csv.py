import csv
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB", "ai_research_db")
DB_USER = os.getenv("POSTGRES_USER", "ai_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

OUTPUT_PATH = "data-analysis/vosviewer_data_dimensions.csv"

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def fetch_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, publication_date, country, citation_count
        FROM publications
        WHERE publication_date IS NOT NULL AND publication_date != 'Unknown';
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def generate_csv(data):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Header: Dimensions-like format
        writer.writerow([
            "Title", "Authors", "Source title", "DOI", "Year", "Volume",
            "Issue", "Pages", "Citations", "Affiliations", "Abstract"
        ])

        for title, pub_date, country, citations in data:
            year = pub_date.year if hasattr(pub_date, 'year') else "Unknown"
            writer.writerow([
                title, "N/A", "N/A", "N/A", year, "", "", "", citations, country, ""
            ])

    print(f"✅ CSV saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    records = fetch_data()
    generate_csv(records)
