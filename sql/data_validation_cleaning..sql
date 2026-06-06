USE starbucks_project;
SET SQL_SAFE_UPDATES = 0;

SELECT COUNT(*) AS total_rows
FROM starbucks_customer_ordering_patterns;

SELECT order_id, COUNT(*) AS duplicate_count
FROM starbucks_customer_ordering_patterns
GROUP BY order_id
HAVING COUNT(*) > 1;

DROP TABLE IF EXISTS clean_orders;

CREATE TABLE clean_orders AS
SELECT DISTINCT *
FROM starbucks_customer_ordering_patterns;

SELECT
    SUM(customer_id          IS NULL) AS missing_customer_id,
    SUM(order_id             IS NULL) AS missing_order_id,
    SUM(total_spend          IS NULL) AS missing_spend,
    SUM(customer_satisfaction IS NULL) AS missing_satisfaction,
    SUM(fulfillment_time_min IS NULL) AS missing_fulfillment
FROM clean_orders;

UPDATE clean_orders
SET total_spend = 0
WHERE total_spend IS NULL;

UPDATE clean_orders
SET customer_satisfaction = 3
WHERE customer_satisfaction IS NULL;

ALTER TABLE clean_orders
ADD COLUMN order_timestamp DATETIME;

UPDATE clean_orders
SET order_timestamp = STR_TO_DATE(
    CONCAT(order_date, ' ', order_time),
    '%Y-%m-%d %H:%i:%s'
);

SELECT
    COUNT(*)                        AS total_orders,
    COUNT(DISTINCT customer_id)     AS unique_customers,
    ROUND(SUM(total_spend), 2)      AS total_revenue,
    ROUND(AVG(total_spend), 2)      AS avg_order_value,
    ROUND(AVG(customer_satisfaction), 2) AS avg_satisfaction,
    ROUND(AVG(fulfillment_time_min), 2)  AS avg_fulfillment_min
FROM clean_orders;

SELECT
    region,
    COUNT(*)                    AS total_orders,
    ROUND(SUM(total_spend), 2)  AS total_revenue,
    ROUND(AVG(total_spend), 2)  AS avg_order_value,
    ROUND(
        SUM(total_spend) * 100.0 / (SELECT SUM(total_spend) FROM clean_orders),
        1
    )                           AS revenue_share_pct
FROM clean_orders
GROUP BY region
ORDER BY total_revenue DESC;

SELECT
    drink_category,
    COUNT(*)                              AS total_orders,
    ROUND(AVG(total_spend), 2)            AS avg_spend,
    ROUND(AVG(customer_satisfaction), 2)  AS avg_satisfaction,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM clean_orders),
        1
    )                                     AS order_share_pct
FROM clean_orders
GROUP BY drink_category
ORDER BY total_orders DESC;

SELECT
    day_of_week,
    COUNT(*)                    AS total_orders,
    ROUND(AVG(total_spend), 2)  AS avg_spend
FROM clean_orders
GROUP BY day_of_week
ORDER BY FIELD(day_of_week, 'Mon','Tue','Wed','Thu','Fri','Sat','Sun');

SELECT
    HOUR(order_timestamp)   AS hour_of_day,
    COUNT(*)                AS total_orders,
    ROUND(AVG(total_spend), 2) AS avg_spend
FROM clean_orders
GROUP BY hour_of_day
ORDER BY total_orders DESC
LIMIT 10;

SELECT
    is_rewards_member,
    COUNT(*)                              AS total_orders,
    ROUND(AVG(total_spend), 2)            AS avg_spend,
    ROUND(AVG(customer_satisfaction), 2)  AS avg_satisfaction,
    ROUND(AVG(fulfillment_time_min), 2)   AS avg_fulfillment_min
FROM clean_orders
GROUP BY is_rewards_member;

SELECT
    store_location_type,
    COUNT(*)                    AS total_orders,
    ROUND(SUM(total_spend), 2)  AS total_revenue,
    ROUND(AVG(total_spend), 2)  AS avg_order_value
FROM clean_orders
GROUP BY store_location_type
ORDER BY total_revenue DESC;

SELECT
    order_channel,
    COUNT(*)                              AS total_orders,
    ROUND(AVG(total_spend), 2)            AS avg_spend,
    ROUND(AVG(fulfillment_time_min), 2)   AS avg_fulfillment_min,
    ROUND(AVG(customer_satisfaction), 2)  AS avg_satisfaction
FROM clean_orders
GROUP BY order_channel
ORDER BY total_orders DESC;

SELECT
AVG(fulfillment_time_min) AS avg_time,
MIN(fulfillment_time_min) AS min_time,
MAX(fulfillment_time_min) AS max_time
FROM clean_orders;

SELECT
    order_ahead,
    COUNT(*)                              AS total_orders,
    ROUND(AVG(total_spend), 2)            AS avg_spend,
    ROUND(AVG(fulfillment_time_min), 2)   AS avg_fulfillment_min,
    ROUND(AVG(customer_satisfaction), 2)  AS avg_satisfaction
FROM clean_orders
GROUP BY order_ahead;

SELECT
    cart_size,
    COUNT(*)                   AS total_orders,
    ROUND(AVG(total_spend), 2) AS avg_spend
FROM clean_orders
GROUP BY cart_size
ORDER BY cart_size ASC;

SELECT
    customer_age_group,
    COUNT(*)                              AS total_orders,
    ROUND(AVG(total_spend), 2)            AS avg_spend,
    ROUND(AVG(customer_satisfaction), 2)  AS avg_satisfaction,
    ROUND(AVG(num_customizations), 2)     AS avg_customizations
FROM clean_orders
GROUP BY customer_age_group
ORDER BY FIELD(customer_age_group, '18-24','25-34','35-44','45-54','55+');

SELECT
    day_of_week,
    HOUR(order_timestamp) AS hour_of_day,
    COUNT(*)              AS total_orders
FROM clean_orders
GROUP BY day_of_week, hour_of_day
ORDER BY total_orders DESC
LIMIT 10;

SELECT
    drink_category,
    SUM(region = 'West')      AS West,
    SUM(region = 'Northeast') AS Northeast,
    SUM(region = 'Midwest')   AS Midwest,
    SUM(region = 'Southeast') AS Southeast,
    SUM(region = 'Southwest') AS Southwest
FROM clean_orders
GROUP BY drink_category
ORDER BY (West + Northeast + Midwest + Southeast + Southwest) DESC;

SELECT
    customer_id,
    COUNT(*)                    AS total_orders,
    ROUND(SUM(total_spend), 2)  AS lifetime_value,
    ROUND(AVG(total_spend), 2)  AS avg_order_value,
    MAX(is_rewards_member)      AS is_rewards_member
FROM clean_orders
GROUP BY customer_id
ORDER BY lifetime_value DESC
LIMIT 20;


SELECT * FROM clean_orders;


SET SQL_SAFE_UPDATES = 1;
