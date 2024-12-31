"""
=================================================
Milestone 3

Nama  : Serina Roihaanah Mulawati
Batch : FTDS-0036-RMT

Program ini dibuat untuk melakukan automatisasi transform dan load data dari PostgreSQL ke ElasticSearch. 
Adapun dataset yang dipakai adalah dataset mengenai penjualan di supermarket.
=================================================
"""

import pandas as pd
import psycopg2
from elasticsearch import Elasticsearch
from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime as dt
from datetime import timedelta, timedelta

# Temp Path
TEMP_CSV_PATH = "/opt/airflow/dags/data_clean.csv"

# Fetch Data from Postgre
def fetch_data():
    """
    Fungsi ini ditujukan untuk mengambil data dari PostgreSQL untuk selanjutnya dilakukan Data Cleaning.

    Return:
    data: DataFrame - daftar data yang ada di tabel PostgreSQL dalam format DataFrame

    Contoh penggunaan:
    data = fetch_data()
    """
    # Connect to Postgre
    conn = psycopg2.connect(
        host="postgres",        
        database="airflow",     
        user="airflow",         
        password="airflow",     
        port=5432
    )
    
    query = "SELECT * FROM table_m3"  # Mengambil semua data dari table_m3
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Save file to temp path
    df.to_csv(TEMP_CSV_PATH, index=False)

# Data Cleaning
def clean_data():
    """
    Fungsi ini digunakan untuk membersihkan data yang telah diambil dari PostgreSQL. 
    Membersihkan mencakup penghapusan duplikat, normalisasi nama kolom, 
    serta penanganan missing value.

    Return:
    - Fungsi ini menyimpan data yang telah dibersihkan ke file CSV sementara.

    Proses yang dilakukan:
    1. Menghapus duplikat data pada dataset.
    2. Melakukan normalisasi nama kolom dengan cara menjadikan semua nama kolom huruf kecil dan 
       mengganti spasi dengan underscore.
    3. Mengisi nilai yang hilang dengan nilai modus (nilai yang paling sering muncul) pada setiap kolom kategorik
       dan mengisi dengan nilai median untuk kolom numerik.
    
    Contoh penggunaan:
    clean_data()
    """

    # Load data
    df = pd.read_csv(TEMP_CSV_PATH)
    
    # Drop duplicate
    df = df.drop_duplicates()
    
    # Column Normalization
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('|', '')
    
    # Missing value handling for numerical columns
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    # Missing value handling for categorical columns
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    
    df.to_csv(TEMP_CSV_PATH, index=False)

# Send data to elasticsearch
def post_to_elasticsearch():
    """
    Fungsi ini digunakan untuk mengirimkan data yang telah dibersihkan ke Elasticsearch.

    Return:
    - Fungsi ini mengirim data ke Elasticsearch.

    Proses yang dilakukan:
    1. Menghubungkan ke server Elasticsearch yang ada pada host dan port yang telah ditentukan.
    2. Memuat data yang telah dibersihkan dari file CSV.
    3. Mengirim setiap baris data sebagai dokumen ke Elasticsearch untuk disimpan dalam indeks 'customer_data'.

    Contoh penggunaan:
    post_to_elasticsearch()
    """

    # Connect to elasticsearch
    es = Elasticsearch("http://elasticsearch:9200") 
    df=pd.read_csv(TEMP_CSV_PATH)
    index_name = "supermarket_data" 
 
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
 
    for i,row in df.iterrows():
        doc=row.to_json()
        unique_id = row['invoice_id'] 
        es.index(index=index_name, id=unique_id, body=doc)
      

default_args= {
    'owner': 'serina',
    'start_date': dt.datetime(2024, 11, 9),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}
 
# DAG Setup
with DAG(
        "MS_Pipeline",
        schedule_interval='30 6 * * *',
        default_args=default_args, 
        catchup=False) as dag:

        # Task 1: Fetch data from PostgreSQL
        t1 = PythonOperator(
                             task_id='fetch_from_postgresql', 
                             python_callable=fetch_data 
                            )
        
        # Task 2: Clean the data
        t2 = PythonOperator(
                             task_id='data_cleaning', 
                             python_callable=clean_data
                            )

        # Task 3: Post data to Elasticsearch
        t3 = PythonOperator(
                             task_id='post_to_elasticsearch', 
                             python_callable=post_to_elasticsearch
                            )

        t1 >> t2 >> t3
