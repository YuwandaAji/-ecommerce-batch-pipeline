from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from google.cloud import bigquery
import pandas as pd
import os

PROJECT_ID = 'rosy-timer-500113-u0'
DATASET_ID = 'raw'
KEY_PATH = '/opt/airflow/keys/rosy-timer-500113-u0-4b2da759baec.json'
DATA_PATH = '/opt/airflow/data/raw'

TABLES = {
    'olist_customers_dataset.csv': 'customers',
    'olist_geolocation_dataset.csv': 'geolocation',
    'olist_order_items_dataset.csv': 'order_items',
    'olist_order_payments_dataset.csv': 'order_payments',
    'olist_order_reviews_dataset.csv': 'order_reviews',
    'olist_orders_dataset.csv': 'orders',
    'olist_products_dataset.csv': 'products',
    'olist_sellers_dataset.csv': 'sellers',
    'product_category_name_translation.csv': 'product_category_name_translation',
}

def load_csv_to_bq(csv_file, table_name):
    client = bigquery.Client.from_service_account_json(
        KEY_PATH, project=PROJECT_ID
    )

    file_path = os.path.join(DATA_PATH, csv_file)
    table_id = f'{PROJECT_ID}.{DATASET_ID}.{table_name}'

    first_chunk = True
    total_rows = 0

    for chunk in pd.read_csv(file_path, chunksize=50000):
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

        job = client.load_table_from_dataframe(chunk, table_id, job_config=job_config)
        job.result()
        total_rows += len(chunk)
        print(f'  [{table_name}] Loaded {total_rows} rows so far...')

    print(f'Done! Total {total_rows} rows loaded into {table_id}')

with DAG(
    dag_id='load_csv_to_bigquery',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@once',
    catchup=False,
    max_active_tasks=2,
    tags=['ecommerce', 'raw', 'bigquery'],
) as dag:

    for csv_file, table_name in TABLES.items():
        PythonOperator(
            task_id=f'load_{table_name}',
            python_callable=load_csv_to_bq,
            op_kwargs={
                'csv_file': csv_file,
                'table_name': table_name,
            },
        )