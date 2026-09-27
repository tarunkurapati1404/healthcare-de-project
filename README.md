# 🏥 End-to-End Healthcare Data Engineering Pipeline

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PySpark-3.4-orange?style=for-the-badge&logo=apache-spark&logoColor=white" />
  <img src="https://img.shields.io/badge/dbt-1.6-orange?style=for-the-badge&logo=dbt&logoColor=white" />
  <img src="https://img.shields.io/badge/Snowflake-Data_Warehouse-blue?style=for-the-badge&logo=snowflake&logoColor=white" />
  <img src="https://img.shields.io/badge/Power_BI-Visualizations-yellow?style=for-the-badge&logo=power-bi&logoColor=black" />
  <img src="https://img.shields.io/badge/Apache_Airflow-Orchestration-black?style=for-the-badge&logo=apache-airflow&logoColor=white" />
</p>

---

## 📖 Project Overview

This project automates the ingestion, cleaning, and transformation of healthcare patient data to identify key revenue drivers by medical condition. By building a modern **Medallion Architecture** (Bronze ➔ Silver ➔ Gold), this pipeline processes raw CSV data and delivers actionable business insights directly to an interactive Power BI dashboard.

---

## 🏗️ Architecture Diagram

```text
[ Raw CSV Data ] 
        │
        ▼ (Upload)
[ AWS S3 - Bronze Layer ] 
        │
        ▼ (PySpark Read & Clean)
[ Databricks Serverless ] 
        │
        ▼ (Write Parquet)
[ AWS S3 - Silver Layer ] 
        │
        ▼ (COPY INTO)
[ Snowflake - RAW Schema ] 
        │
        ▼ (dbt Source)
[ dbt Cloud - Staging (stg_patients) ] 
        │
        ▼ (dbt Ref)
[ dbt Cloud - Gold Model (gold_diagnosis_summary) ] 
        │
        ▼ (Connect)
[ 📊 Power BI Dashboard ]

* Orchestrated by: Apache Airflow DAG
```

---

## 🛠️ Tech Stack

| Category | Technology Used |
| :--- | :--- |
| **Cloud Storage** | AWS S3 (Data Lake) |
| **Compute & Processing** | Databricks (PySpark on Serverless) |
| **Data Warehousing** | Snowflake |
| **Transformation** | dbt (data build tool) |
| **Orchestration** | Apache Airflow |
| **Visualization** | Microsoft Power BI |

---

## 📂 Project Structure

```text
Healthcare_DE_Project/
│
├── dags/                        # Apache Airflow DAGs
│   └── healthcare_pipeline_dag.py
│
├── dbt_project/                 # dbt models and configurations
│   ├── dbt_project.yml
│   └── models/
│       ├── gold_diagnosis_summary.sql
│       └── staging/
│           ├── sources.yml
│           └── stg_patients.sql
│
├── power_bi/                    # Power BI .pbix dashboard file
│   └── healthcare_dashboard.pbix
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ How It Works

1. **Ingestion:** Raw `patients.csv` is uploaded to the AWS `s3://bronze/` folder.
2. **Processing (Silver):** A Databricks PySpark notebook reads the CSV, drops null values, and writes the clean data as compressed Parquet files to the `s3://silver/` folder.
3. **Loading:** The Parquet data is loaded into Snowflake's `HEALTHCARE_DB.RAW` schema.
4. **Transformation (Gold):** dbt Cloud is triggered to run a staging model (`stg_patients`) and a Gold aggregation model (`gold_diagnosis_summary`), which calculates total revenue per medical condition.
5. **Visualization:** Power BI connects directly to the Snowflake Gold table to render interactive charts.

---

## 🚨 Challenges & Solutions (Real-World Troubleshooting)

| Challenge Encountered | Root Cause | Solution Implemented |
| :--- | :--- | :--- |
| **Databricks Serverless S3 Access** | `SparkContext` is not supported in Databricks Serverless, causing `JVM_ATTRIBUTE_NOT_SUPPORTED` errors when setting global Hadoop configs. | Refactored PySpark code to use the `.option()` method chained directly to `.read` and `.write` operations. This passes credentials per-action and is 100% Serverless-compatible. |
| **dbt `ref()` vs `source()`** | Attempting to use `{{ ref('patients') }}` directly on a raw Snowflake table failed because `ref()` only links dbt models. | Implemented a proper dbt workflow by defining a `sources.yml` file to map the raw Snowflake table, creating a `stg_patients` staging model using `{{ source() }}` and then using `{{ ref('stg_patients') }}` for the Gold model. |

---

## 🚀 Future Enhancements

* Implement Great Expectations or dbt tests to validate data quality before loading into Snowflake.
* Add CI/CD pipelines using GitHub Actions to automatically run `dbt compile` on pull requests.
* Containerize the Airflow environment using Docker Compose for local testing.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.