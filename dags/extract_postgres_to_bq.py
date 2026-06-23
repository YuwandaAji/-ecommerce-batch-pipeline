from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime
from google.cloud import bigquery
import pandas as pd
from sqlalchemy import create_engine

PROJECT_ID = 'rosy-timer-500113-u0'
DATASET_ID = 'raw'
KEY_PATH = '/opt/airflow/keys/rosy-timer-500113-u0-4b2da759baec.json'

TABLES = [
    'customers',
    'geolocation',
    'order_items',
    'order_payments',
    'order_reviews',
    'orders',
    'products',
    'sellers',
    'product_category_name_translation',
]

def extract_postgres_to_bq(table_name):
    # Ambil koneksi dari Airflow connection
    conn = BaseHook.get_connection('postgres_source')
    engine = create_engine(
        f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}'
    )

    bq_client = bigquery.Client.from_service_account_json(
        KEY_PATH, project=PROJECT_ID
    )

    table_id = f'{PROJECT_ID}.{DATASET_ID}.{table_name}'
    first_chunk = True
    total_rows = 0

    # Baca dari PostgreSQL pakai chunked query
    for chunk in pd.read_sql(
        f'SELECT * FROM {table_name}',
        engine,
        chunksize=50000
    ):
        if first_chunk:
            job_config = bigquery.LoadJobConfig(
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                autodetect=True,
            )
            first_chunk = False
        else:
            job_config = bigquery.LoadJobConfig(
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
                autodetect=True,
            )

        job = bq_client.load_table_from_dataframe(chunk, table_id, job_config=job_config)
        job.result()
        total_rows += len(chunk)
        print(f'  [{table_name}] Loaded {total_rows} rows so far...')

    print(f'Done! Total {total_rows} rows loaded into {table_id}')

with DAG(
    dag_id='extract_postgres_to_bigquery',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    max_active_tasks=2,
    tags=['ecommerce', 'raw', 'bigquery', 'postgres'],
) as dag:

    for table_name in TABLES:
        PythonOperator(
            task_id=f'extract_{table_name}',
            python_callable=extract_postgres_to_bq,
            op_kwargs={'table_name': table_name},
        )