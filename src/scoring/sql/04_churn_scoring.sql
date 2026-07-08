DROP TABLE IF EXISTS gold.seller_churn CASCADE;

CREATE TABLE gold.seller_churn AS
WITH metrics_joined AS (
    SELECT 
        b.seller_id,
        b.total_orders,
        b.total_revenue_usd,
        b.avg_review_score,
        b.late_delivery_rate,
        b.last_order_date,
        t.consecutive_decline_months,
        COALESCE(r.recent_avg_review, b.avg_review_score) AS recent_avg_review,
        COALESCE(r.historical_avg_review, b.avg_review_score) AS historical_avg_review,
        -- LƯU Ý: Dùng max date của tập dữ liệu vì đây là data lịch sử tĩnh (2016-2018).
        -- Đổi sang CURRENT_TIMESTAMP nếu chạy pipeline realtime.
        ROUND(EXTRACT(EPOCH FROM ((SELECT MAX(order_purchase_ts) FROM silver.orders_master) - b.last_order_date))/86400) AS recency_days,
        s.seller_state,
        s.seller_city
    FROM gold.tmp_base_metrics b
    JOIN gold.tmp_monthly_trends t ON b.seller_id = t.seller_id
    JOIN gold.tmp_review_trends r ON b.seller_id = r.seller_id
    JOIN silver.sellers s ON b.seller_id = s.seller_id
),
thresholds AS (
    SELECT 
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY late_delivery_rate) AS p75_late_delivery,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY avg_review_score) AS p25_review,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY recency_days) AS p75_recency
    FROM metrics_joined
),
scored AS (
    SELECT 
        m.*,
        (
            CASE WHEN m.late_delivery_rate >= t.p75_late_delivery THEN 20 ELSE 0 END +
            CASE WHEN m.consecutive_decline_months >= 2 THEN 20 
                 WHEN m.consecutive_decline_months = 1 THEN 10 ELSE 0 END +
            CASE WHEN m.recent_avg_review < m.historical_avg_review THEN 15 ELSE 0 END +
            CASE WHEN m.recent_avg_review <= t.p25_review THEN 20 ELSE 0 END +
            CASE WHEN m.recency_days >= t.p75_recency THEN 25 ELSE 0 END
        ) AS churn_risk_score
    FROM metrics_joined m
    CROSS JOIN thresholds t
)
SELECT 
    *,
    CASE 
        WHEN churn_risk_score >= 80 THEN 'Critical'
        WHEN churn_risk_score >= 50 THEN 'High'
        WHEN churn_risk_score >= 30 THEN 'Medium'
        ELSE 'Low'
    END AS risk_label,
    CASE 
        WHEN churn_risk_score >= 80 THEN 'Gọi ngay lập tức. Đề xuất giảm chiết khấu.'
        WHEN churn_risk_score >= 50 THEN 'Gửi email hướng dẫn tăng doanh số.'
        WHEN churn_risk_score >= 30 THEN 'Theo dõi chặt chẽ. Gửi báo cáo định kỳ.'
        ELSE 'Không cần hành động. Seller khỏe mạnh.'
    END AS recommendation,
    CURRENT_TIMESTAMP AS calculated_at
FROM scored;
