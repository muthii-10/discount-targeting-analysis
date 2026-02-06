/* 1. Average customer value score and discount usage by loyalty tier */

SELECT
    loyalty_tier,
    COUNT(*) AS customers,
    AVG(customer_value_score)::NUMERIC(5,2) AS avg_customer_value_score,
    AVG(discount_flag)::NUMERIC(5,2) AS discount_usage_rate
FROM customer_features
GROUP BY loyalty_tier
ORDER BY avg_customer_value_score DESC;
