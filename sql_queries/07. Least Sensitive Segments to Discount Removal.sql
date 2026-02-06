/* 7. Segments with lowest revenue risk if discounts were removed*/

WITH segment_summary AS (
    SELECT
        loyalty_tier,
        value_tier,
        AVG(customer_value_score)::NUMERIC(5,2) AS avg_value,
        AVG(discount_flag)::NUMERIC(5,2) AS discount_rate
    FROM customer_features
    GROUP BY loyalty_tier, value_tier
)
SELECT
    loyalty_tier,
    value_tier,
    avg_value,
    discount_rate
FROM segment_summary
WHERE discount_rate < 0.4
ORDER BY avg_value DESC;
