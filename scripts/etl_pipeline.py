import os
import time
import requests
import pandas as pd
import psycopg2
from datetime import datetime

COUNTRIES = ["USA", "DEU", "FRA", "IND", "CHN", "JPN", "GBR", "CAN", "AUS", "BRA"]

INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "SP.POP.TOTL": "population",
    "FP.CPI.TOTL.ZG": "inflation_percent",
    "SL.UEM.TOTL.ZS": "unemployment_percent",
    "EN.ATM.CO2E.PC": "co2_emissions_per_capita"
}

START_YEAR = 2014
END_YEAR = datetime.now().year


def fetch_world_bank_indicator(country, indicator, retries=3):
    url = (
        f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
        f"?format=json&date={START_YEAR}:{END_YEAR}&per_page=100"
    )

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=60)

            if response.status_code == 200:
                data = response.json()
                if len(data) > 1:
                    return data[1]

            print(f"Failed request for {country}-{indicator}: HTTP {response.status_code}")
            return []

        except requests.exceptions.Timeout:
            print(f"Timeout for {country}-{indicator}. Retry {attempt + 1}/{retries}")
            time.sleep(5)

        except requests.exceptions.RequestException as e:
            print(f"Request error for {country}-{indicator}: {e}")
            time.sleep(5)

    print(f"Skipped {country}-{indicator} after {retries} retries.")
    return []


def extract():
    records = []

    for country in COUNTRIES:
        for indicator_code, indicator_name in INDICATORS.items():
            print(f"Fetching {indicator_name} for {country}")

            data = fetch_world_bank_indicator(country, indicator_code)

            for record in data:
                records.append({
                    "country_code": country,
                    "country_name": record["country"]["value"],
                    "indicator_code": indicator_code,
                    "indicator_name": indicator_name,
                    "year": record["date"],
                    "value": record["value"]
                })

            time.sleep(0.3)

    return pd.DataFrame(records)


def transform(df_raw):
    df_raw["year"] = df_raw["year"].astype(int)
    df_raw["value"] = pd.to_numeric(df_raw["value"], errors="coerce")
    df_raw = df_raw.dropna(subset=["value"])

    df_final = df_raw.pivot_table(
        index=["country_code", "country_name", "year"],
        columns="indicator_name",
        values="value",
        aggfunc="first"
    ).reset_index()

    return df_final


def load(df_final):
    conn = psycopg2.connect(
        dbname="GlobalEconomy",
        user="global_user",
        password="admin123",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute("DELETE FROM economic_indicators;")

    insert_query = """
    INSERT INTO economic_indicators (
        country_code,
        country_name,
        year,
        co2_emissions_per_capita,
        gdp_current_usd,
        inflation_percent,
        population,
        unemployment_percent
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df_final.iterrows():
        cur.execute(insert_query, (
            row["country_code"],
            row["country_name"],
            int(row["year"]),
            row.get("co2_emissions_per_capita"),
            row.get("gdp_current_usd"),
            row.get("inflation_percent"),
            row.get("population"),
            row.get("unemployment_percent")
        ))

    conn.commit()
    conn.close()

    print(f"Loaded {len(df_final)} records into PostgreSQL.")


def run_pipeline():
    print("ETL pipeline started")

    raw_df = extract()
    clean_df = transform(raw_df)
    load(clean_df)

    os.makedirs("data/processed", exist_ok=True)
    clean_df.to_csv("data/processed/global_economic_indicators.csv", index=False)

    print("ETL pipeline completed")


if __name__ == "__main__":
    run_pipeline()
