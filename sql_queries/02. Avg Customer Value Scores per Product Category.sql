/* 2. Product categories with the highest average customer value */

SELECT
    category,
    COUNT(*) AS customers,
    AVG(customer_value_score)::NUMERIC(5,2) AS avg_customer_value_score
FROM customer_features
GROUP BY category
ORDER BY avg_customer_value_score DESC;
