USE star_bucks;

SET SESSION net_read_timeout    = 600;
SET SESSION net_write_timeout   = 600;
SET SESSION wait_timeout        = 600;
SET SESSION interactive_timeout = 600;

DROP TABLE IF EXISTS orders_overview;

CREATE TABLE orders_overview AS
SELECT
    COUNT(order_id)                                                                         AS total_orders,
    COUNT(DISTINCT customer_id)                                                             AS unique_customers,
    ROUND(SUM(total_spend), 2)                                                              AS total_revenue,
    ROUND(AVG(total_spend), 2)                                                              AS avg_order_value,
    ROUND(AVG(cart_size), 2)                                                                AS avg_cart_size,
    ROUND(AVG(fulfillment_time_min), 2)                                                     AS avg_fulfillment_time,
    ROUND(AVG(num_customizations), 2)                                                       AS avg_customizations,
    ROUND(AVG(customer_satisfaction), 2)                                                    AS avg_satisfaction_score,

    SUM(CASE WHEN LOWER(TRIM(has_food_item))     IN ('true','1','yes') THEN 1 ELSE 0 END)  AS food_item_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(has_food_item))     IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)  AS food_item_pct,

    SUM(CASE WHEN LOWER(TRIM(order_ahead))       IN ('true','1','yes') THEN 1 ELSE 0 END)  AS order_ahead_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(order_ahead))       IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)  AS order_ahead_pct,

    SUM(CASE WHEN LOWER(TRIM(is_rewards_member)) IN ('true','1','yes') THEN 1 ELSE 0 END)  AS rewards_member_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(is_rewards_member)) IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS rewards_member_pct,

    COUNT(DISTINCT store_id)                                                                AS total_stores,
    COUNT(DISTINCT region)                                                                  AS total_regions,
    ROUND(SUM(total_spend) / COUNT(DISTINCT customer_id), 2)                               AS customer_lifetime_value
FROM star_bucks_orders;

DROP TABLE IF EXISTS customer_insights;

CREATE TABLE customer_insights AS
SELECT
    customer_age_group,
    customer_gender,
    is_rewards_member,
    COUNT(DISTINCT customer_id)                                                                  AS unique_customers,
    COUNT(order_id)                                                                              AS total_orders,
    ROUND(SUM(total_spend), 2)                                                                   AS total_spend,
    ROUND(AVG(total_spend), 2)                                                                   AS avg_spend_per_order,
    ROUND(AVG(cart_size), 2)                                                                     AS avg_cart_size,
    ROUND(AVG(num_customizations), 2)                                                            AS avg_customizations,
    ROUND(AVG(customer_satisfaction), 2)                                                         AS avg_satisfaction,
    ROUND(AVG(fulfillment_time_min), 2)                                                          AS avg_fulfillment_time,

    SUM(CASE WHEN LOWER(TRIM(has_food_item)) IN ('true','1','yes') THEN 1 ELSE 0 END)            AS food_item_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(has_food_item)) IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)  AS food_item_pct,

    SUM(CASE WHEN LOWER(TRIM(order_ahead))   IN ('true','1','yes') THEN 1 ELSE 0 END)            AS order_ahead_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(order_ahead))   IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)  AS order_ahead_pct,

    ROUND(SUM(total_spend) / COUNT(DISTINCT customer_id), 2)                                     AS lifetime_value
FROM star_bucks_orders
GROUP BY customer_age_group, customer_gender, is_rewards_member
ORDER BY total_spend DESC;

DROP TABLE IF EXISTS duplicate_orders;

CREATE TABLE duplicate_orders AS
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM star_bucks_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

DROP TABLE IF EXISTS peak_order_time;

CREATE TABLE peak_order_time AS
SELECT
    HOUR(order_time)                     AS order_hour,
    day_of_week,
    order_channel,
    COUNT(order_id)                      AS total_orders,
    ROUND(SUM(total_spend), 2)           AS hourly_revenue,
    ROUND(AVG(total_spend), 2)           AS avg_order_value,
    ROUND(AVG(fulfillment_time_min), 2)  AS avg_fulfillment_time,
    ROUND(AVG(customer_satisfaction), 2) AS avg_satisfaction
FROM star_bucks_orders
GROUP BY order_hour, day_of_week, order_channel
ORDER BY total_orders DESC;

DROP TABLE IF EXISTS drink_performance;

CREATE TABLE drink_performance AS
SELECT
    drink_category,
    COUNT(order_id)                                                                              AS total_orders,
    ROUND(SUM(total_spend), 2)                                                                   AS total_revenue,
    ROUND(AVG(total_spend), 2)                                                                   AS avg_order_value,
    ROUND(AVG(num_customizations), 2)                                                            AS avg_customizations,
    ROUND(AVG(cart_size), 2)                                                                     AS avg_cart_size,

    SUM(CASE WHEN LOWER(TRIM(has_food_item)) IN ('true','1','yes') THEN 1 ELSE 0 END)            AS food_combo_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(has_food_item)) IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)  AS food_combo_pct,

    SUM(CASE WHEN LOWER(TRIM(order_ahead))   IN ('true','1','yes') THEN 1 ELSE 0 END)            AS order_ahead_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(order_ahead))   IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)  AS order_ahead_pct,

    ROUND(AVG(customer_satisfaction), 2)                                                         AS avg_satisfaction,
    ROUND(SUM(total_spend) / COUNT(order_id), 2)                                                 AS revenue_per_order
FROM star_bucks_orders
GROUP BY drink_category
ORDER BY total_orders DESC;

DROP TABLE IF EXISTS revenue_region_analysis;

CREATE TABLE revenue_region_analysis AS
SELECT
    region,
    order_ahead,
    order_channel,
    store_location_type,
    COUNT(order_id)                                                                              AS total_orders,
    COUNT(DISTINCT customer_id)                                                                  AS unique_customers,
    ROUND(SUM(total_spend), 2)                                                                   AS total_revenue,
    ROUND(AVG(total_spend), 2)                                                                   AS avg_order_value,
    ROUND(AVG(cart_size), 2)                                                                     AS avg_cart_size,
    ROUND(AVG(fulfillment_time_min), 2)                                                          AS avg_fulfillment_time,
    ROUND(AVG(customer_satisfaction), 2)                                                         AS avg_satisfaction,

    SUM(CASE WHEN LOWER(TRIM(has_food_item)) IN ('true','1','yes') THEN 1 ELSE 0 END)            AS food_item_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(has_food_item)) IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)  AS food_item_pct,

    ROUND(SUM(total_spend) / COUNT(DISTINCT customer_id), 2)                                     AS revenue_per_customer
FROM star_bucks_orders
GROUP BY region, order_ahead, order_channel, store_location_type
ORDER BY total_revenue DESC;

DROP TABLE IF EXISTS store_performance;

CREATE TABLE store_performance AS
SELECT
    store_id,
    region,
    store_location_type,
    COUNT(order_id)                                                                              AS total_orders,
    COUNT(DISTINCT customer_id)                                                                  AS unique_customers,
    ROUND(SUM(total_spend), 2)                                                                   AS total_revenue,
    ROUND(AVG(total_spend), 2)                                                                   AS avg_order_value,
    ROUND(AVG(cart_size), 2)                                                                     AS avg_cart_size,
    ROUND(AVG(num_customizations), 2)                                                            AS avg_customizations,
    ROUND(AVG(customer_satisfaction), 2)                                                         AS avg_satisfaction,
    ROUND(AVG(fulfillment_time_min), 2)                                                          AS avg_fulfillment_time,

    SUM(CASE WHEN LOWER(TRIM(order_ahead))       IN ('true','1','yes') THEN 1 ELSE 0 END)        AS order_ahead_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(order_ahead))       IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)  AS order_ahead_pct,

    SUM(CASE WHEN LOWER(TRIM(has_food_item))     IN ('true','1','yes') THEN 1 ELSE 0 END)        AS food_item_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(has_food_item))     IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)  AS food_item_pct,

    SUM(CASE WHEN LOWER(TRIM(is_rewards_member)) IN ('true','1','yes') THEN 1 ELSE 0 END)        AS rewards_orders,
    ROUND(SUM(CASE WHEN LOWER(TRIM(is_rewards_member)) IN ('true','1','yes') THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS rewards_pct,

    RANK() OVER (ORDER BY SUM(total_spend) DESC)            AS revenue_rank,
    RANK() OVER (ORDER BY AVG(customer_satisfaction) DESC)  AS satisfaction_rank
FROM star_bucks_orders
GROUP BY store_id, region, store_location_type;

SELECT * FROM orders_overview;
SELECT * FROM customer_insights;
SELECT * FROM duplicate_orders;
SELECT * FROM peak_order_time;
SELECT * FROM drink_performance;
SELECT * FROM revenue_region_analysis;
SELECT * FROM store_performance;