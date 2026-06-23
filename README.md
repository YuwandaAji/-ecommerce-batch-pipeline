\# E-Commerce Batch Data Pipeline



End-to-end batch data pipeline for the Brazilian E-Commerce (Olist) dataset, built with Apache Airflow, dbt, and Google BigQuery.



\## Dashboard

🔗 \[View Live Dashboard](https://datastudio.google.com/reporting/4349e496-6a9e-40db-a1a5-384647c182e1)



\## Architecture

CSV Files (Olist Dataset)



↓



Apache Airflow (Orchestration)



↓



Google BigQuery - Raw Layer



↓



dbt (Transformation)



↓



BigQuery - Staging Layer (Views)



↓



BigQuery - Mart Layer (Tables)



↓



Looker Studio (Dashboard)



\## Tech Stack



| Tool | Purpose |

|------|---------|

| Apache Airflow | Pipeline orchestration \& scheduling |

| Google BigQuery | Cloud data warehouse |

| dbt | Data transformation \& testing |

| Looker Studio | Data visualization \& dashboard |

| Docker | Containerized Airflow (LocalExecutor) |

| Python | DAG scripting \& data loading |



\## Project Structure



ecommerce-batch-pipeline/



├── dags/



│   └── load\_csv\_to\_bq.py      # Airflow DAG: load CSV to BigQuery



├── dbt\_project/



│   ├── models/



│   │   ├── staging/           # Staging views (1 per raw table)



│   │   │   ├── sources.yml



│   │   │   ├── schema.yml



│   │   │   ├── stg\_orders.sql



│   │   │   ├── stg\_customers.sql



│   │   │   ├── stg\_order\_items.sql



│   │   │   ├── stg\_order\_payments.sql



│   │   │   ├── stg\_order\_reviews.sql



│   │   │   ├── stg\_products.sql



│   │   │   ├── stg\_sellers.sql



│   │   │   └── stg\_product\_category.sql



│   │   └── mart/              # Mart tables (analytics-ready)



│   │       └── mart\_orders.sql



│   └── dbt\_project.yml



├── docker-compose.yml



└── README.md



\## Dataset



\[Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — 100k+ real orders from 2016-2018, consisting of 9 relational tables covering orders, customers, products, sellers, payments, and reviews.



\## Pipeline Flow



\### 1. Extract \& Load (Airflow)

\- Airflow DAG (`load\_csv\_to\_bigquery`) reads 9 CSV files from local storage

\- Loads each file into BigQuery `raw` dataset using chunked loading (50k rows/chunk) to handle memory constraints

\- Runs with `LocalExecutor` on Docker (2 containers: Airflow + PostgreSQL)



\### 2. Transform (dbt)

\- \*\*Staging layer\*\*: Cleans and standardizes raw tables (rename columns, cast data types)

\- \*\*Mart layer\*\*: Joins staging models into analytics-ready `mart\_orders` table with derived metrics (e.g. `delivery\_delay\_days`)

\- dbt tests validate data quality (unique, not\_null constraints)



\### 3. Visualize (Looker Studio)

Dashboard includes:

\- 📈 Total Revenue Time Series

\- 🏆 Top 10 Product Categories by Revenue

\- 🥧 Order Status Distribution

\- 💳 Payment Method Distribution

\- ⭐ Avg Review Score by State

\- 4 KPI Scorecards (Revenue, Orders, Avg Rating, Avg Delivery Delay)



\## Key Insights

\- \*\*96.2%\*\* of orders were successfully delivered

\- \*\*73.7%\*\* of payments made via credit card

\- Average delivery was \*\*12 days faster\*\* than estimated

\- Revenue peaked in \*\*late 2017\*\* (Black Friday period)



\## How to Run



\### Prerequisites

\- Docker Desktop

\- Python 3.10+

\- Google Cloud account (BigQuery Sandbox)

\- dbt-bigquery



\### Steps

1\. Clone this repo

2\. Add GCP service account key to `keys/` folder

3\. Start Airflow: `docker compose up -d`

4\. Trigger DAG `load\_csv\_to\_bigquery` from Airflow UI (`localhost:8080`)

5\. Run dbt: `cd dbt\_project \&\& dbt run`

6\. Run dbt tests: `dbt test`



\## Author

\*\*Yuwanda Aji Pangestu\*\* — \[GitHub](https://github.com/YuwandaAji)

