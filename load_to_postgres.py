import pandas as pd
from sqlalchemy import create_engine
import os

# Koneksi ke postgres-source
engine = create_engine('postgresql://olist:olist123@localhost:5433/olist_db')

raw_path = r'D:\Project-Portofolio\Mix\ecommerce-batch-pipeline\data\raw'

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

for csv_file, table_name in TABLES.items():
    file_path = os.path.join(raw_path, csv_file)
    print(f'Loading {csv_file} → {table_name}...')
    
    for chunk in pd.read_csv(file_path, chunksize=50000):
        chunk.to_sql(
            table_name,
            engine,
            if_exists='append',
            index=False
        )
    
    print(f'  ✓ {table_name} done')

print('Semua tabel berhasil dimuat ke PostgreSQL!')