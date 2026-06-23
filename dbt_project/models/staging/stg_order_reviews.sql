WITH source AS (
    SELECT * FROM {{ source('raw', 'order_reviews') }}
),

renamed AS (
    SELECT
        review_id,
        order_id,
        review_score,
        review_comment_title,
        review_comment_message,
        TIMESTAMP(review_creation_date)    AS review_created_at,
        TIMESTAMP(review_answer_timestamp) AS review_answered_at
    FROM source
)

SELECT * FROM renamed