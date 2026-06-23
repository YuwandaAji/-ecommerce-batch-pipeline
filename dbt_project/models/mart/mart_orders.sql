WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

order_items AS (
    SELECT
        order_id,
        COUNT(order_item_id)  AS total_items,
        SUM(price)            AS total_revenue,
        SUM(freight_value)    AS total_freight
    FROM {{ ref('stg_order_items') }}
    GROUP BY order_id
),

payments AS (
    SELECT
        order_id,
        SUM(payment_value)        AS total_payment,
        MAX(payment_type)         AS payment_type,
        MAX(payment_installments) AS payment_installments
    FROM {{ ref('stg_order_payments') }}
    GROUP BY order_id
),

reviews AS (
    SELECT
        order_id,
        MAX(review_score) AS review_score
    FROM {{ ref('stg_order_reviews') }}
    GROUP BY order_id
),

order_items_with_category AS (
    SELECT
        oi.order_id,
        pc.category_name_english
    FROM {{ ref('stg_order_items') }} oi
    LEFT JOIN {{ ref('stg_products') }} p
        ON oi.product_id = p.product_id
    LEFT JOIN {{ ref('stg_product_category') }} pc
        ON p.category_name = pc.category_name
    QUALIFY ROW_NUMBER() OVER (PARTITION BY oi.order_id ORDER BY oi.order_item_id) = 1
),

final AS (
    SELECT
        o.order_id,
        o.customer_id,
        c.city                                          AS customer_city,
        c.state                                         AS customer_state,
        o.order_status,
        o.purchased_at,
        o.approved_at,
        o.delivered_to_customer_at,
        o.estimated_delivery_at,
        DATE_DIFF(
            DATE(o.delivered_to_customer_at),
            DATE(o.estimated_delivery_at),
            DAY
        )                                               AS delivery_delay_days,
        oi.total_items,
        oi.total_revenue,
        oi.total_freight,
        p.total_payment,
        p.payment_type,
        p.payment_installments,
        r.review_score,
        oic.category_name_english
    FROM orders o
    LEFT JOIN customers c
        ON o.customer_id = c.customer_id
    LEFT JOIN order_items oi
        ON o.order_id = oi.order_id
    LEFT JOIN payments p
        ON o.order_id = p.order_id
    LEFT JOIN reviews r
        ON o.order_id = r.order_id
    LEFT JOIN order_items_with_category oic
        ON o.order_id = oic.order_id
)

SELECT * FROM final