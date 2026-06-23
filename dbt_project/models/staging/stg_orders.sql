WITH source AS (
    SELECT * FROM {{ source('raw', 'orders') }}
),

renamed AS (
    SELECT
        order_id,
        customer_id,
        order_status,
        TIMESTAMP(order_purchase_timestamp)     AS purchased_at,
        TIMESTAMP(order_approved_at)            AS approved_at,
        TIMESTAMP(order_delivered_carrier_date) AS delivered_to_carrier_at,
        TIMESTAMP(order_delivered_customer_date) AS delivered_to_customer_at,
        TIMESTAMP(order_estimated_delivery_date) AS estimated_delivery_at
    FROM source
)

SELECT * FROM renamed