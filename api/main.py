from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Global Economic Intelligence API")

def get_connection():
    return psycopg2.connect(
        dbname="GlobalEconomy",
        user="global_user",
        password="admin123",
        host="localhost",
        port="5432"
    )

@app.get("/")
def home():
    return {"message": "Global Economic Intelligence API is running"}

@app.get("/countries")
def get_countries():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT DISTINCT country_code, country_name
        FROM economic_indicators
        ORDER BY country_name;
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

@app.get("/country/{country_code}")
def get_country_data(country_code: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT *
        FROM economic_indicators
        WHERE country_code = %s
        ORDER BY year;
    """, (country_code.upper(),))

    rows = cur.fetchall()
    conn.close()
    return rows

@app.get("/latest")
def get_latest_data():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT *
        FROM economic_indicators
        WHERE year = (
            SELECT MAX(year)
            FROM economic_indicators
        )
        ORDER BY gdp_current_usd DESC;
    """)

    rows = cur.fetchall()
    conn.close()
    return rows
