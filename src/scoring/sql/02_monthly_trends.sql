DROP TABLE IF EXISTS gold.tmp_monthly_trends CASCADE;
CREATE TABLE gold.tmp_monthly_trends AS
WITH monthly_revenue AS (
    SELECT 
        seller_id,
        DATE_TRUNC('month', order_purchase_ts) AS order_month,
        SUM(total_value_usd) AS monthly_revenue
    FROM silver.orders_master
    GROUP BY seller_id, DATE_TRUNC('month', order_purchase_ts)
),
flagged AS (
    SELECT 
        seller_id,
        order_month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (PARTITION BY seller_id ORDER BY order_month) AS prev_revenue,
        ROW_NUMBER() OVER (PARTITION BY seller_id ORDER BY order_month DESC) AS rn_desc
    FROM monthly_revenue
),
decline_groups AS (
    SELECT 
        seller_id,
        order_month,
        CASE WHEN monthly_revenue < prev_revenue THEN 1 ELSE 0 END AS is_decline,
        rn_desc
    FROM flagged
),
first_non_decline AS (
    SELECT 
        seller_id,
        MIN(rn_desc) AS first_non_decline_rn
    FROM decline_groups
    WHERE is_decline = 0
    GROUP BY seller_id
)
SELECT 
    d.seller_id,
    COALESCE(
        SUM(d.is_decline) FILTER (WHERE d.rn_desc < f.first_non_decline_rn),
        CASE WHEN f.first_non_decline_rn IS NULL THEN SUM(d.is_decline) ELSE 0 END
    ) AS consecutive_decline_months
FROM decline_groups d
LEFT JOIN first_non_decline f ON d.seller_id = f.seller_id
GROUP BY d.seller_id, f.first_non_decline_rn;
