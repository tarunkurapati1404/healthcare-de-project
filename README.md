\# 🏥 End-to-End Healthcare Data Engineering Pipeline



!\[Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)

!\[PySpark](https://img.shields.io/badge/PySpark-3.4-orange?logo=apache-spark)

!\[dbt](https://img.shields.io/badge/dbt-1.6-orange?logo=dbt)

!\[Snowflake](https://img.shields.io/badge/Snowflake-Data\_warehouse-blue?logo=snowflake)

!\[PowerBI](https://img.shields.io/badge/Power\_BI-Visualizations-yellow?logo=power-bi)

!\[Airflow](https://img.shields.io/badge/Apache\_Airflow-Orchestration-black?logo=apache-airflow)



\## 📖 Project Overview

This project automates the ingestion, cleaning, and transformation of healthcare patient data to identify key revenue drivers by medical condition. By building a modern \*\*Medallion Architecture\*\* (Bronze ➔ Silver ➔ Gold), this pipeline processes raw CSV data and delivers actionable business insights directly to a Power BI dashboard.



\## 🏗️ Architecture Diagram



```mermaid

graph TD

&#x20;   A\[📥 Raw CSV Data] -->|Upload| B\[(AWS S3 - Bronze Layer)]

&#x20;   B -->|PySpark Read \& Clean| C\[⚙️ Databricks Serverless]

&#x20;   C -->|Write Parquet| D\[(AWS S3 - Silver Layer)]

&#x20;   D -->|COPY INTO| E\[(Snowflake - RAW Schema)]

&#x20;   E -->|dbt Source| F\[🔄 dbt Cloud - Staging]

&#x20;   F -->|dbt Ref| G\[🏆 dbt Cloud - Gold Model]

&#x20;   G -->|Connect| H\[📊 Power BI Dashboard]

&#x20;   

&#x20;   I\[⏰ Apache Airflow DAG] -.->|Orchestrates| C

&#x20;   I -.->|Orchestrates| F



🛠️ Tech Stack



Cloud Storage: AWS S3 (Data Lake)

Compute \& Processing: Databricks (PySpark on Serverless)

Data Warehousing: Snowflake

Transformation: dbt (data build tool)

Orchestration: Apache Airflow

Visualization: Microsoft Power BI



📂 Project Structure



Healthcare\_DE\_Project/

│

├── dags/                       # Apache Airflow DAGs

│   ── healthcare\_pipeline\_dag.py

│

├── dbt\_project/                # dbt models and configurations

│   ├── models/

│   │   ├── staging/

│   │   │   └── stg\_patients.sql

│   │   ├── gold\_diagnosis\_summary.sql

│   │   └── sources.yml

│   └── dbt\_project.yml

│

── power\_bi/                   # Power BI .pbix dashboard file

│   └── healthcare\_dashboard.pbix

│

├── .gitignore

├── LICENSE

└── README.md



🚀 How It Works



1. Ingestion: Raw patients.csv is uploaded to the AWS S3 bronze/ folder.

2\. Processing (Silver): A Databricks PySpark notebook reads the CSV, drops null values, and writes the clean data as compressed Parquet files to the S3 silver/ folder.

3\. Loading: The Parquet data is loaded into Snowflake's HEALTHCARE\_DB.RAW schema.

4\. Transformation (Gold): dbt Cloud is triggered to run a staging model (stg\_patients) and a Gold aggregation model (gold\_diagnosis\_summary), which calculates total revenue per medical condition.

5\. Visualization: Power BI connects directly to the Snowflake Gold table to render interactive charts.



🐛 Challenges \& Solutions (Real-World Troubleshooting)



1. Databricks Serverless S3 Access:

&#x09;Issue: SparkContext is not supported in Databricks Serverless, causing JVM\_ATTRIBUTE\_NOT\_SUPPORTED errors when trying to set global Hadoop configurations.

&#x09;Solution: Refactored the PySpark code to use the .option() method chained directly to the .read and .write operations. This passes credentials per-action and is 100% Serverless-		  compatible.

2\. dbt ref() vs source():

&#x09;Issue: Attempting to use {{ ref('patients') }} directly on a raw Snowflake table failed because ref() only links dbt models.

&#x09;Solution: Implemented a proper dbt workflow by defining a sources.yml file to map the raw Snowflake table, creating a stg\_patients staging model using {{ source() }}, and then 	          using {{ ref('stg\_patients') }} for the Gold model.



🚀 Future Enhancements



1. Implement Great Expectations or dbt tests to validate data quality before loading into Snowflake.

2\. Add CI/CD pipelines using GitHub Actions to automatically run dbt compile on pull requests.

3\. Containerize the Airflow environment using Docker Compose for local testing.

