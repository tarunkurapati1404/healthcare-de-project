# 1. Import necessary tools from Airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# 2. Define default settings for our pipeline
default_args = {
    'owner': 'tarun',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 3. Define the DAG itself
with DAG(
    dag_id='healthcare_etl_pipeline',
    default_args=default_args,
    description='End-to-end Healthcare Data Pipeline',
    schedule_interval='@daily', # Runs every day at midnight
    start_date=datetime(2026, 9, 24), # Start date (today/yesterday)
    catchup=False, # Don't run for past dates
    tags=['healthcare', 'de_project'],
) as dag:

    # --- TASK 1: Ingest Data (Simulated) ---
    # In a real job, this would be an S3 sensor waiting for new files.
    ingest_data = BashOperator(
        task_id='check_s3_for_new_patients_csv',
        bash_command='echo "Checking S3 Bronze layer for new patients.csv..."'
    )

    # --- TASK 2: Clean Data with Databricks (Simulated) ---
    # In a real job, this would use the 'DatabricksSubmitRunOperator' 
    # to trigger your PySpark notebook we wrote on Day 2.
    clean_data_databricks = BashOperator(
        task_id='run_databricks_pyspark_cleaning',
        bash_command='echo "Triggering Databricks Serverless to clean data and move to Silver layer..."'
    )

    # --- TASK 3: Load to Snowflake (Simulated) ---
    # In a real job, this would use the 'SnowflakeOperator' to run a COPY INTO command.
    load_to_snowflake = BashOperator(
        task_id='load_silver_data_to_snowflake_raw',
        bash_command='echo "Loading Parquet data from S3 Silver into HEALTHCARE_DB.RAW.PATIENTS..."'
    )

    # --- TASK 4: Transform with dbt (Simulated) ---
    # In a real job, this would use the 'DbtCloudRunJobOperator' to trigger your dbt Cloud job.
    transform_with_dbt = BashOperator(
        task_id='run_dbt_cloud_job',
        bash_command='echo "Triggering dbt Cloud to run stg_patients and gold_diagnosis_summary..."'
    )

    # --- DEFINE THE ORDER (The Arrows!) ---
    # This tells Airflow the exact sequence of events.
    ingest_data >> clean_data_databricks >> load_to_snowflake >> transform_with_dbt