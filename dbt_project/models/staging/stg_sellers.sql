WITH source AS (
    SELECT * FROM {{ source('raw', 'sellers') }}
),

renamed AS (
    SELECT
        seller_id,
        seller_zip_code_prefix AS zip_code,
        seller_city            AS city,
        seller_state           AS state
    FROM source
)

SELECT * FROM renamed