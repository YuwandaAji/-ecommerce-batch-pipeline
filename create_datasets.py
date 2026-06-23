from google.cloud import bigquery

client = bigquery.Client.from_service_account_json(
    '/opt/airflow/keys/rosy-timer-500113-u0-4b2da759baec.json',
    project='rosy-timer-500113-u0'
)

for dataset_id in ['raw', 'dbt_ecommerce']:
    dataset = bigquery.Dataset(f'rosy-timer-500113-u0.{dataset_id}')
    dataset.location = 'US'
    client.create_dataset(dataset, exists_ok=True)
    print(f'Dataset {dataset_id} siap')