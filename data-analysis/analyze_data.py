import os
import psycopg2
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def connect_db():
    """ Establish connection to the PostgreSQL database. """
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def fetch_data_by_year(field, country):
    """ Fetch publication counts by year for a specific field and country. """
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT 
        EXTRACT(YEAR FROM publication_date) AS year,
        COUNT(*) AS publication_count
    FROM publications
    WHERE field = %s AND country = %s
    GROUP BY year
    ORDER BY year;
    """

    cursor.execute(query, (field, country))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def plot_trend(data, country, field):
    """ Plot the publication trend over time for a specific country and field. """
    years = [int(row[0]) for row in data]
    counts = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    plt.plot(years, counts, marker='o', linestyle='-', label=f"{country} - {field}")
    plt.xlabel("Year")
    plt.ylabel("Publication Count")
    plt.title(f"Research Output Trend in {field} ({country})")
    plt.grid(alpha=0.3)
    plt.legend()
    os.makedirs("data-analysis/output", exist_ok=True)
    output_path = f"data-analysis/output/{country}_{field}_trend.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Trend plot saved as {output_path}")

def main():
    # Example Analysis for AI and Deep Learning
    fields = ["AI", "Deep Learning"]
    countries = ["US", "CN", "DE"]

    for field in fields:
        for country in countries:
            print(f"Analyzing {field} in {country}...")
            data = fetch_data_by_year(field, country)
            if data:
                plot_trend(data, country, field)
            else:
                print(f"No data found for {field} in {country}")

if __name__ == "__main__":
    main()
