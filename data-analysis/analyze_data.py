import os
import psycopg2
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def connect_db():
    """ Establish connection to the PostgreSQL database """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def fetch_data_by_year():
    """ Fetch publication count per year from the database """
    conn = connect_db()
    cursor = conn.cursor()

    query = '''
        SELECT 
            EXTRACT(YEAR FROM publication_date) AS year, 
            COUNT(*) 
        FROM publications 
        WHERE publication_date IS NOT NULL
        GROUP BY year 
        ORDER BY year ASC;
    '''

    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    
    return data

def plot_publication_trends(data):
    """ Plot the publication trends """
    years, counts = zip(*data) if data else ([], [])
    
    plt.figure(figsize=(12, 6))
    plt.bar(years, counts, color='blue')
    plt.xlabel("Year")
    plt.ylabel("Number of Publications")
    plt.title("Research Publications Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    output_path = "data-analysis/publication_trends.png"
    plt.savefig(output_path)
    plt.show()
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    data = fetch_data_by_year()
    plot_publication_trends(data)
