/* 5. Distribution of value tiers within each loyalty tier */

SELECT
    loyalty_tier,
    value_tier,
    COUNT(*) AS customers,
    (COUNT(*) * 1.0 /
        SUM(COUNT(*)) OVER (PARTITION BY loyalty_tier))::NUMERIC(5,3) AS pct_within_loyalty
FROM customer_features
GROUP BY loyalty_tier, value_tier
ORDER BY loyalty_tier, pct_within_loyalty DESC;
