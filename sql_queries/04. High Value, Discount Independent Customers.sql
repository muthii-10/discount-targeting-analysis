/* 4. Segments with above-average value but below-average promotion usage */

WITH benchmarks AS (
    SELECT
        AVG(customer_value_score) AS overall_avg_value,
        AVG(discount_flag) AS overall_avg_discount
    FROM customer_features
)
SELECT
    loyalty_tier,
    value_tier,
    COUNT(*) AS customers,
    AVG(customer_value_score)::NUMERIC(5,2) AS avg_value,
    AVG(discount_flag)::NUMERIC(5,2) AS discount_rate
FROM customer_features, benchmarks
GROUP BY loyalty_tier, value_tier, overall_avg_value, overall_avg_discount
HAVING
    AVG(customer_value_score) > overall_avg_value
    AND AVG(discount_flag) < overall_avg_discount
ORDER BY avg_value DESC;
