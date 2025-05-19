import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

RAW_DATA_PATH = "data-extraction/raw_data/"

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def process_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    records = []
    for item in data.get("results", []):
        publication_id = item.get("id")
        title = item.get("title", "No Title")
        publication_date = item.get("publication_date", "Unknown")
        country = item.get("host_institution", {}).get("country_code", "Unknown")
        field = item.get("concepts", [{}])[0].get("display_name", "Unknown")
        citation_count = item.get("cited_by_count", 0)

        records.append((publication_id, title, publication_date, country, field, citation_count))

    return records

def insert_data(records):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.executemany("""
    INSERT INTO publications (id, title, publication_date, country, field, citation_count)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """, records)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {len(records)} records into the database.")

def process_all_files():
    for filename in os.listdir(RAW_DATA_PATH):
        file_path = os.path.join(RAW_DATA_PATH, filename)
        if filename.endswith(".json"):
            print(f"Processing {filename}...")
            records = process_file(file_path)
            insert_data(records)

if __name__ == "__main__":
    process_all_files()
