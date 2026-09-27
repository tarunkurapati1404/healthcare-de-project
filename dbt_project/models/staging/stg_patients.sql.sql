SELECT *
FROM {{ source('healthcare_raw', 'PATIENTS') }}