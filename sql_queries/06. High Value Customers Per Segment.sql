/* 6. Top 10% most valuable customers within each loyalty tier */

WITH ranked_customers AS (
    SELECT
        customer_id,
        loyalty_tier,
        customer_value_score,
        NTILE(10) OVER (
            PARTITION BY loyalty_tier
            ORDER BY customer_value_score DESC
        ) AS value_decile
    FROM customer_features
)
SELECT
    customer_id,
    loyalty_tier,
    customer_value_score
FROM ranked_customers
WHERE value_decile = 1
ORDER BY loyalty_tier, customer_value_score DESC;
