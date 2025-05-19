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
    """ Establish connection to the PostgreSQL database. """
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def insert_publication(record):
    """ Insert a single publication record into the database """
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO publications (id, title, publication_date, country, field, citation_count)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """

    try:
        cursor.execute(query, record)
        conn.commit()
    except Exception as e:
        print(f"Error inserting record: {e}")
    finally:
        cursor.close()
        conn.close()

def process_file(file_path):
    """ Process JSON data file and insert records into the database """
    with open(file_path, "r") as file:
        data = json.load(file)
        for item in data.get("results", []):
            publication_id = item.get("id", "unknown")
            title = item.get("title", "No Title")
            publication_date = item.get("publication_date", "2000-01-01")
            country = item.get("host_institution", {}).get("country_code", "Unknown")
            field = item.get("concepts", [{}])[0].get("display_name", "Unknown")
            citation_count = item.get("cited_by_count", 0)

            # DEBUG: Print the extracted record before insertion
            print(f"Inserting: {publication_id}, {title}, {publication_date}, {country}, {field}, {citation_count}")

            record = (publication_id, title, publication_date, country, field, citation_count)
            insert_publication(record)

def process_all_files():
    """ Process all JSON files in the raw data directory """
    for filename in os.listdir(RAW_DATA_PATH):
        if filename.endswith(".json"):
            file_path = os.path.join(RAW_DATA_PATH, filename)
            print(f"Processing {filename}...")
            process_file(file_path)

if __name__ == "__main__":
    process_all_files()
