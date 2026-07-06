CREATE SCHEMA IF NOT EXISTS gold;

DROP TABLE IF EXISTS gold.tmp_base_metrics CASCADE;
CREATE TABLE gold.tmp_base_metrics AS
SELECT 
    seller_id,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_value_usd) AS total_revenue_usd,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(
        COUNT(DISTINCT CASE WHEN is_late_delivery THEN order_id END)::numeric / COUNT(DISTINCT order_id)
    , 4) AS late_delivery_rate,
    MAX(order_purchase_ts) AS last_order_date
FROM silver.orders_master
GROUP BY seller_id;
