# E-Commerce Batch Data Pipeline

End-to-end batch data pipeline for the Brazilian E-Commerce (Olist) dataset, simulating a real-world OLTP → OLAP architecture using PostgreSQL, Apache Airflow, dbt, and Google BigQuery.

## Dashboard
🔗 [View Live Dashboard](https://datastudio.google.com/reporting/4349e496-6a9e-40db-a1a5-384647c182e1)

## Architecture

Olist Dataset (CSV)

↓

PostgreSQL (Source / OLTP layer)

↓

Apache Airflow (Orchestration & Scheduling)

↓

Google BigQuery - Raw Layer (OLAP)

↓

dbt (Transformation)

├── Staging Layer (Views) — clean & standardize

└── Mart Layer (Tables) — analytics-ready

↓

Looker Studio (Dashboard & Visualization)

## Tech Stack

| Tool | Purpose |
|------|---------|
| PostgreSQL | Source database (OLTP simulation) |
| Apache Airflow | Pipeline orchestration & scheduling |
| Google BigQuery | Cloud data warehouse (OLAP) |
| dbt | Data transformation & testing |
| Looker Studio | Data visualization & dashboard |
| Docker | Containerized Airflow + PostgreSQL |
| Python | DAG scripting & data loading |

## Project Structure

ecommerce-batch-pipeline/

├── dags/

│   ├── load_csv_to_bq.py              # DAG v1: CSV → BigQuery

│   └── extract_postgres_to_bq.py      # DAG v2: PostgreSQL → BigQuery

├── dbt_project/

│   ├── models/

│   │   ├── staging/                   # Staging views (1 per raw table)

│   │   │   ├── sources.yml

│   │   │   ├── schema.yml

│   │   │   ├── stg_orders.sql

│   │   │   ├── stg_customers.sql

│   │   │   ├── stg_order_items.sql

│   │   │   ├── stg_order_payments.sql

│   │   │   ├── stg_order_reviews.sql

│   │   │   ├── stg_products.sql

│   │   │   ├── stg_sellers.sql

│   │   │   └── stg_product_category.sql

│   │   └── mart/                      # Mart tables (analytics-ready)

│   │       └── mart_orders.sql

│   └── dbt_project.yml

├── docker-compose.yml

└── README.md

## Dataset

[Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — 100k+ real orders from 2016-2018, consisting of 9 relational tables covering orders, customers, products, sellers, payments, and reviews.

## Pipeline Flow

### 1. Source Database (PostgreSQL)
- Olist dataset loaded into PostgreSQL container simulating a real OLTP database
- Represents the operational database that an e-commerce backend would write to in production

### 2. Extract & Load (Airflow)
- Airflow DAG (`extract_postgres_to_bigquery`) runs on `@daily` schedule
- Extracts all 9 tables from PostgreSQL using chunked reads (50k rows/chunk)
- Loads into BigQuery `raw` dataset
- Credentials managed via Airflow Connections (not hardcoded)
- Runs with `LocalExecutor` on Docker, max 2 parallel tasks (RAM-optimized)

### 3. Transform (dbt)
- **Staging layer**: Cleans and standardizes raw tables (rename columns, cast data types)
- **Mart layer**: Joins staging models into analytics-ready `mart_orders` table with derived metrics:
  - `delivery_delay_days` — actual vs estimated delivery difference
  - `total_revenue`, `total_freight`, `total_payment` — aggregated per order
- dbt tests validate data quality (unique, not_null constraints)
- Auto-generated documentation with lineage graph

### 4. Visualize (Looker Studio)
Dashboard includes:
- 📈 Total Revenue Time Series
- 🏆 Top 10 Product Categories by Revenue
- 🥧 Order Status Distribution
- 💳 Payment Method Distribution
- ⭐ Avg Review Score by State
- 4 KPI Scorecards (Revenue, Orders, Avg Rating, Avg Delivery Delay)
- Interactive filters (Date Range, Order Status, Customer State)

## Key Insights
- **96.2%** of orders were successfully delivered
- **73.7%** of payments made via credit card
- Average delivery was **12 days faster** than estimated
- Revenue peaked in **late 2017** (Black Friday period)

## How to Run

### Prerequisites
- Docker Desktop
- Python 3.10+
- Google Cloud account (BigQuery Sandbox)
- dbt-bigquery

### Steps
1. Clone this repo
2. Add GCP service account key to `keys/` folder
3. Download [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place CSVs in `data/raw/`
4. Start all containers: `docker compose up -d`
5. Load data to PostgreSQL: `python load_to_postgres.py`
6. Register connections in Airflow UI (`localhost:8080`):
   - `postgres_source` — PostgreSQL source database
   - `google_cloud_default` — GCP service account
7. Trigger DAG `extract_postgres_to_bigquery`
8. Run dbt: `cd dbt_project && dbt run`
9. Run dbt tests: `dbt test`
10. View dashboard at the link above

## Author
**Yuwanda Aji Pangestu** — [GitHub](https://github.com/YuwandaAji)