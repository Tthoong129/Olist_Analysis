DROP TABLE IF EXISTS gold.tmp_review_trends CASCADE;
CREATE TABLE gold.tmp_review_trends AS
WITH seller_dates AS (
    SELECT seller_id, MAX(order_purchase_ts) as last_order_date
    FROM silver.orders_master
    GROUP BY seller_id
)
SELECT 
    m.seller_id,
    ROUND(AVG(m.review_score) FILTER (WHERE m.order_purchase_ts >= d.last_order_date - INTERVAL '90 days'), 2) AS recent_avg_review,
    ROUND(AVG(m.review_score) FILTER (WHERE m.order_purchase_ts < d.last_order_date - INTERVAL '90 days'), 2) AS historical_avg_review
FROM silver.orders_master m
JOIN seller_dates d ON m.seller_id = d.seller_id
GROUP BY m.seller_id;
