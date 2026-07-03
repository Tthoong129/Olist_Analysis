CREATE SCHEMA IF NOT EXISTS silver;

-- ============================================================
-- 1. Bảng Orders
-- ============================================================
DROP TABLE IF EXISTS silver.orders CASCADE;
CREATE TABLE silver.orders AS
SELECT
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp::timestamp          AS order_purchase_ts,
    order_approved_at::timestamp                 AS order_approved_ts,
    order_delivered_carrier_date::timestamp      AS delivered_carrier_ts,
    order_delivered_customer_date::timestamp     AS delivered_customer_ts,
    order_estimated_delivery_date::timestamp     AS estimated_delivery_ts,

    -- Tính chỉ số hiệu suất giao hàng
    CASE
        WHEN order_delivered_customer_date IS NOT NULL
         AND order_estimated_delivery_date IS NOT NULL
         AND order_delivered_customer_date > order_estimated_delivery_date
        THEN TRUE ELSE FALSE
    END AS is_late_delivery,

    ROUND(
        EXTRACT(EPOCH FROM (
            order_delivered_customer_date::timestamp
            - order_estimated_delivery_date::timestamp
        )) / 86400
    ) AS delivery_delay_days,

    ROUND(
        EXTRACT(EPOCH FROM (
            order_delivered_customer_date::timestamp
            - order_purchase_timestamp::timestamp
        )) / 86400
    ) AS actual_delivery_days

FROM bronze.orders
WHERE order_status NOT IN ('canceled', 'unavailable')
  AND order_purchase_timestamp IS NOT NULL;


-- ============================================================
-- 2. Bảng Order Items
-- ============================================================
DROP TABLE IF EXISTS silver.order_items CASCADE;
CREATE TABLE silver.order_items AS
WITH fx AS (
    SELECT rate FROM bronze.exchange_rates
    ORDER BY fetched_at DESC LIMIT 1
)
SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.shipping_limit_date::timestamp            AS shipping_limit_ts,
    oi.price,
    oi.freight_value,
    ROUND((oi.price       * fx.rate)::numeric, 2) AS price_usd,
    ROUND((oi.freight_value * fx.rate)::numeric, 2) AS freight_usd,
    ROUND(((oi.price + oi.freight_value) * fx.rate)::numeric, 2) AS total_value_usd
FROM bronze.order_items oi
CROSS JOIN fx;


-- ============================================================
-- 3. Bảng Reviews
-- ============================================================
DROP TABLE IF EXISTS silver.order_reviews CASCADE;
CREATE TABLE silver.order_reviews AS
SELECT
    review_id,
    order_id,
    review_score,
    COALESCE(review_comment_title,   '') AS comment_title,
    COALESCE(review_comment_message, '') AS comment_message,
    review_creation_date::timestamp      AS review_created_ts,
    review_answer_timestamp::timestamp   AS review_answered_ts
FROM bronze.order_reviews
WHERE review_id IS NOT NULL
  AND order_id  IS NOT NULL;


-- ============================================================
-- 4. Bảng Sellers
-- ============================================================
DROP TABLE IF EXISTS silver.sellers CASCADE;
CREATE TABLE silver.sellers AS
SELECT
    seller_id,
    seller_zip_code_prefix,
    TRIM(LOWER(seller_city))  AS seller_city,
    UPPER(TRIM(seller_state)) AS seller_state
FROM bronze.sellers
WHERE seller_id IS NOT NULL;


-- ============================================================
-- 5. Bảng Products
-- ============================================================
DROP TABLE IF EXISTS silver.products CASCADE;
CREATE TABLE silver.products AS
SELECT
    p.product_id,
    COALESCE(p.product_category_name, 'unknown')          AS category_pt,
    COALESCE(t.product_category_name_english, 'unknown')  AS category_en,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm,
    p.product_photos_qty
FROM bronze.products p
LEFT JOIN bronze.product_category_translation t
       ON p.product_category_name = t.product_category_name
WHERE p.product_id IS NOT NULL;


-- ============================================================
-- 6. Bảng Orders Master (Bảng tổng hợp chuẩn bị cho tầng Gold)
-- ============================================================
DROP TABLE IF EXISTS silver.orders_master CASCADE;
CREATE TABLE silver.orders_master AS
WITH latest_review AS (
    SELECT
        order_id,
        review_score,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY review_answered_ts DESC NULLS LAST
        ) AS rn
    FROM silver.order_reviews
)
SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_ts,
    o.estimated_delivery_ts,
    o.delivered_customer_ts,
    o.is_late_delivery,
    o.delivery_delay_days,
    o.actual_delivery_days,

    oi.order_item_id,
    oi.seller_id,
    oi.product_id,
    oi.price_usd,
    oi.freight_usd,
    oi.total_value_usd,

    s.seller_city,
    s.seller_state,

    p.category_en  AS product_category,
    p.product_weight_g,

    r.review_score,

    CURRENT_TIMESTAMP AS created_at

FROM silver.orders          o
JOIN silver.order_items     oi ON o.order_id    = oi.order_id
JOIN silver.sellers         s  ON oi.seller_id  = s.seller_id
JOIN silver.products        p  ON oi.product_id = p.product_id
LEFT JOIN latest_review     r  ON o.order_id    = r.order_id AND r.rn = 1;


-- ============================================================
-- Kiểm tra nhanh số lượng dòng (Sanity check)
-- ============================================================
SELECT
    (SELECT COUNT(*) FROM silver.orders)        AS orders,
    (SELECT COUNT(*) FROM silver.order_items)   AS items,
    (SELECT COUNT(*) FROM silver.order_reviews) AS reviews,
    (SELECT COUNT(*) FROM silver.sellers)       AS sellers,
    (SELECT COUNT(*) FROM silver.products)      AS products,
    (SELECT COUNT(*) FROM silver.orders_master) AS master;
