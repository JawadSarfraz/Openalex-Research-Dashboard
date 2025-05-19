import sqlite3
import os

DB_PATH = "data-processing/research_data.db"

def create_database():
    os.makedirs("data-processing", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS publications (
        id TEXT PRIMARY KEY,
        title TEXT,
        publication_date TEXT,
        country TEXT,
        field TEXT,
        citation_count INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS countries (
        country_code TEXT PRIMARY KEY,
        country_name TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    create_database()
