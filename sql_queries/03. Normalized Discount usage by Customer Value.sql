/* 3. Are loyal customers receiving more promotions relative to their value? */

WITH tier_metrics AS (
    SELECT
        loyalty_tier,
        AVG(customer_value_score)::NUMERIC(5,2) AS avg_value,
        AVG(discount_flag)::NUMERIC(5,2) AS discount_rate
    FROM customer_features
    GROUP BY loyalty_tier
)
SELECT
    loyalty_tier,
    avg_value,
    discount_rate,
    (discount_rate / NULLIF(avg_value, 0))::NUMERIC(5,3) AS discount_per_value_unit
FROM tier_metrics
ORDER BY discount_per_value_unit DESC;
