{{ config(materialized='table') }}

SELECT
    medical_condition,
    COUNT(*) AS total_patients,
    ROUND(AVG(billing_amount), 2) AS avg_bill_amount,
    SUM(billing_amount) AS total_revenue
FROM {{ ref('stg_patients') }}
WHERE medical_condition IS NOT NULL
GROUP BY medical_condition
ORDER BY total_revenue DESC