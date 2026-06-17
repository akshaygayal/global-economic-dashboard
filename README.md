# Global Economic Intelligence Dashboard

## Project Overview

This project was developed for the MADSC301 Business Intelligence Final Assessment.

The objective is to build an end-to-end Business Intelligence pipeline that collects, processes, stores, analyzes, and visualizes global economic indicators from the World Bank API. The project also includes a machine learning component to forecast future GDP values.

---

## Business Case

Governments, economists, and businesses rely on economic indicators to understand the health of economies and make informed decisions.

This dashboard provides a centralized view of key economic metrics including:

* GDP (Current USD)
* Population
* Inflation Rate
* Unemployment Rate

The solution enables comparison of multiple countries and analysis of economic trends over time.

---

## Data Source

### World Bank API

Official source:

https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation

Countries analyzed:

* United States
* India
* China
* Japan
* United Kingdom
* Germany
* France
* Canada
* Australia
* Brazil

Indicators collected:

* GDP Current USD
* Population
* Inflation (%)
* Unemployment (%)

Data range:

2014–2024

---

## Technology Stack

### Data Collection

* Python
* Requests
* World Bank API

### Data Processing

* Pandas
* NumPy

### Database

* PostgreSQL

### API Layer

* FastAPI
* Uvicorn

### Visualization

* Power BI

### Machine Learning

* Scikit-Learn
* Linear Regression

### Development Environment

* Python Virtual Environment (venv)

---

## Project Architecture

World Bank API

↓

Python ETL Pipeline

↓

Data Cleaning & Transformation (Pandas)

↓

PostgreSQL Database

↓

FastAPI REST API

↓

Power BI Dashboard

↓

GDP Forecast Model (Machine Learning)

---

## ETL Process

### Extract

Data is collected from the World Bank API for multiple countries and economic indicators.

### Transform

Data cleaning steps include:

* Removing missing values
* Standardizing column names
* Pivoting indicators into analytical format
* Converting data types
* Preparing a clean dataset for analysis

### Load

The processed data is loaded into PostgreSQL for storage and querying.

---

## Database Design

### Table: economic_indicators

Main fields:

* id
* country_code
* country_name
* year
* gdp_current_usd
* population
* inflation_percent
* unemployment_percent

---

## SQL Analysis

Example analyses performed:

### GDP Ranking

Countries ranked by GDP for the latest available year.

### Population Ranking

Countries ranked by population.

### Economic Trend Analysis

Year-over-year comparison of:

* GDP
* Inflation
* Unemployment

---

## FastAPI Endpoints

### GET /countries

Returns all available countries.

### GET /latest

Returns the latest economic data.

### GET /country/{country_code}

Returns historical economic data for a selected country.

Interactive API documentation:

http://localhost:8000/docs

---

## Power BI Dashboard

Dashboard features:

* KPI Cards

  * Average GDP
  * Average Population
  * Average Inflation
  * Average Unemployment

* GDP by Country

* Population by Country

* GDP Growth Trend

* Inflation Trend

* Unemployment Trend

* Country Slicer for interactive filtering

---

## Machine Learning Forecast

A Linear Regression model was trained using historical GDP data.

### Forecast Example

USA GDP Forecast

| Year | Predicted GDP |
| ---- | ------------- |
| 2025 | 2.86E+13      |
| 2026 | 2.97E+13      |
| 2027 | 3.08E+13      |

The model demonstrates how historical economic data can be used to estimate future economic growth.

---

## Screenshots

The repository includes screenshots of:

* Data Collection
* Data Cleaning
* PostgreSQL Database
* SQL Analysis
* FastAPI Documentation
* API Responses
* Power BI Dashboard
* Machine Learning Forecast

---

## How to Run

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run ETL Pipeline

```bash
python scripts/etl_pipeline.py
```

### Start FastAPI

```bash
uvicorn api.main:app --reload
```

### Open API Documentation

```text
http://localhost:8000/docs
```

---

## Project Outcome

The project successfully demonstrates an end-to-end Business Intelligence workflow including:

* Data Acquisition
* Data Cleaning
* Data Storage
* Workflow Automation
* Data Analysis
* API Development
* Dashboard Visualization
* Machine Learning Forecasting

This solution provides a practical example of how Business Intelligence technologies can be combined to support economic analysis and decision-making.
