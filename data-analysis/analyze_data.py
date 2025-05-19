import os
import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Connect to PostgreSQL database
def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Fetch data from database
def fetch_data_by_year():
    conn = connect_db()
    cursor = conn.cursor()
    query = '''SELECT publication_date, COUNT(*) FROM publications GROUP BY publication_date ORDER BY publication_date ASC;'''
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Plot publication trends
def plot_publication_trends(data):
    years, counts = zip(*data)
    years = [str(year) for year in years]

    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, color='blue')
    plt.xlabel("Year")
    plt.ylabel("Number of Publications")
    plt.title("Research Publications Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("data-analysis/publication_trends.png")
    plt.show()

if __name__ == "__main__":
    data = fetch_data_by_year()
    if data:
        plot_publication_trends(data)
    else:
        print("No data available to plot.")