CREATE DATABASE IF NOT EXISTS starbucks_analysis;
USE starbucks_analysis;

SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT customer_id) AS unique_customers,
       COUNT(DISTINCT order_id) AS unique_orders,
       COUNT(DISTINCT store_id) AS unique_stores,
       COUNT(DISTINCT drink_category) AS drink_categories,
       COUNT(DISTINCT region) AS regions
FROM starbucks_orders;

SELECT
  SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END)          AS customer_id_nulls,
  SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END)             AS order_id_nulls,
  SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END)           AS order_date_nulls,
  SUM(CASE WHEN order_time IS NULL THEN 1 ELSE 0 END)           AS order_time_nulls,
  SUM(CASE WHEN day_of_week IS NULL THEN 1 ELSE 0 END)          AS day_of_week_nulls,
  SUM(CASE WHEN order_channel IS NULL THEN 1 ELSE 0 END)        AS order_channel_nulls,
  SUM(CASE WHEN store_id IS NULL THEN 1 ELSE 0 END)             AS store_id_nulls,
  SUM(CASE WHEN store_location_type IS NULL THEN 1 ELSE 0 END)  AS store_location_nulls,
  SUM(CASE WHEN region IS NULL THEN 1 ELSE 0 END)               AS region_nulls,
  SUM(CASE WHEN customer_age_group IS NULL THEN 1 ELSE 0 END)   AS age_group_nulls,
  SUM(CASE WHEN customer_gender IS NULL THEN 1 ELSE 0 END)      AS gender_nulls,
  SUM(CASE WHEN is_rewards_member IS NULL THEN 1 ELSE 0 END)    AS rewards_nulls,
  SUM(CASE WHEN cart_size IS NULL THEN 1 ELSE 0 END)            AS cart_size_nulls,
  SUM(CASE WHEN num_customizations IS NULL THEN 1 ELSE 0 END)   AS customizations_nulls,
  SUM(CASE WHEN total_spend IS NULL THEN 1 ELSE 0 END)          AS total_spend_nulls,
  SUM(CASE WHEN fulfillment_time_min IS NULL THEN 1 ELSE 0 END) AS fulfillment_nulls,
  SUM(CASE WHEN drink_category IS NULL THEN 1 ELSE 0 END)       AS drink_category_nulls,
  SUM(CASE WHEN has_food_item IS NULL THEN 1 ELSE 0 END)        AS food_item_nulls,
  SUM(CASE WHEN order_ahead IS NULL THEN 1 ELSE 0 END)          AS order_ahead_nulls,
  SUM(CASE WHEN customer_satisfaction IS NULL THEN 1 ELSE 0 END) AS satisfaction_nulls
FROM starbucks_orders;

SELECT COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_order_ids
FROM starbucks_orders;

SELECT order_id, COUNT(*) AS occurrences
FROM starbucks_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT
  COUNT(order_id)                                            AS total_orders,
  COUNT(DISTINCT customer_id)                               AS unique_customers,
  ROUND(SUM(total_spend), 2)                                AS total_revenue,
  ROUND(AVG(total_spend), 2)                                AS avg_order_value,
  MAX(total_spend)                                          AS max_spend,
  MIN(total_spend)                                          AS min_spend,
  ROUND(AVG(fulfillment_time_min), 2)                       AS avg_fulfillment_min,
  ROUND(AVG(customer_satisfaction), 2)                      AS avg_satisfaction,
  ROUND(AVG(cart_size), 2)                                  AS avg_cart_size,
  ROUND(AVG(num_customizations), 2)                         AS avg_customizations,
  ROUND(SUM(CASE WHEN is_rewards_member = 'True' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS rewards_member_pct,
  ROUND(SUM(CASE WHEN has_food_item = 'True' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1)     AS food_attach_rate_pct,
  ROUND(SUM(CASE WHEN order_ahead = 'True' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1)       AS order_ahead_rate_pct
FROM starbucks_orders;

SELECT
  drink_category,
  COUNT(order_id)                     AS total_orders,
  ROUND(SUM(total_spend), 2)          AS total_revenue,
  ROUND(AVG(total_spend), 2)          AS avg_spend,
  ROUND(AVG(fulfillment_time_min), 2) AS avg_fulfillment_min,
  ROUND(AVG(customer_satisfaction), 2) AS avg_satisfaction,
  ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM starbucks_orders), 2) AS order_share_pct
FROM starbucks_orders
GROUP BY drink_category
ORDER BY total_revenue DESC;

SELECT
  ROUND(SUM(total_spend), 2)   AS total_revenue,
  ROUND(AVG(total_spend), 2)   AS avg_spend,
  MAX(total_spend)              AS max_spend,
  MIN(total_spend)              AS min_spend,
  ROUND(STDDEV(total_spend), 2) AS stddev_spend
FROM starbucks_orders;

SELECT
  day_of_week,
  COUNT(order_id)           AS total_orders,
  ROUND(SUM(total_spend), 2) AS revenue,
  ROUND(AVG(total_spend), 2) AS avg_spend
FROM starbucks_orders
GROUP BY day_of_week
ORDER BY FIELD(day_of_week, 'Mon','Tue','Wed','Thu','Fri','Sat','Sun');

SELECT
  DATE_FORMAT(order_date, '%Y-%m') AS month,
  COUNT(order_id)                  AS orders,
  ROUND(SUM(total_spend), 2)       AS revenue
FROM starbucks_orders
GROUP BY month
ORDER BY month;

SELECT
  CASE
    WHEN total_spend < 10 THEN '$0-10'
    WHEN total_spend < 20 THEN '$10-20'
    WHEN total_spend < 30 THEN '$20-30'
    WHEN total_spend < 40 THEN '$30-40'
    ELSE '$40+'
  END AS spend_bucket,
  COUNT(*) AS orders,
  ROUND(SUM(total_spend), 2) AS revenue
FROM starbucks_orders
GROUP BY spend_bucket
ORDER BY MIN(total_spend);

SELECT
  HOUR(order_time)           AS order_hour,
  COUNT(order_id)            AS total_orders,
  ROUND(SUM(total_spend), 2) AS revenue,
  ROUND(AVG(total_spend), 2) AS avg_spend
FROM starbucks_orders
GROUP BY order_hour
ORDER BY total_orders DESC;

SELECT HOUR(order_time) AS peak_order_hour, COUNT(*) AS orders
FROM starbucks_orders
GROUP BY peak_order_hour
ORDER BY orders DESC
LIMIT 1;

SELECT HOUR(order_time) AS peak_revenue_hour, ROUND(SUM(total_spend),2) AS revenue
FROM starbucks_orders
GROUP BY peak_revenue_hour
ORDER BY revenue DESC
LIMIT 1;

SELECT
  CASE
    WHEN HOUR(order_time) BETWEEN 5 AND 11  THEN 'Morning (5-11)'
    WHEN HOUR(order_time) BETWEEN 12 AND 16 THEN 'Afternoon (12-16)'
    WHEN HOUR(order_time) BETWEEN 17 AND 21 THEN 'Evening (17-21)'
    ELSE 'Night (22-4)'
  END AS time_segment,
  COUNT(*) AS orders,
  ROUND(SUM(total_spend), 2) AS revenue
FROM starbucks_orders
GROUP BY time_segment
ORDER BY orders DESC;

SELECT
  order_channel,
  COUNT(order_id)                     AS total_orders,
  ROUND(SUM(total_spend), 2)          AS revenue,
  ROUND(AVG(total_spend), 2)          AS avg_spend,
  ROUND(AVG(fulfillment_time_min), 2) AS avg_fulfillment_min,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM starbucks_orders), 1) AS share_pct
FROM starbucks_orders
GROUP BY order_channel
ORDER BY total_orders DESC;

SELECT
  order_ahead,
  COUNT(order_id)            AS orders,
  ROUND(SUM(total_spend), 2) AS revenue,
  ROUND(AVG(total_spend), 2) AS avg_spend,
  ROUND(AVG(fulfillment_time_min), 2) AS avg_fulfillment_min
FROM starbucks_orders
GROUP BY order_ahead;

SELECT
  has_food_item,
  COUNT(order_id)            AS orders,
  ROUND(SUM(total_spend), 2) AS revenue,
  ROUND(AVG(total_spend), 2) AS avg_spend
FROM starbucks_orders
GROUP BY has_food_item;

SELECT
  customer_age_group,
  COUNT(order_id)                     AS total_orders,
  ROUND(SUM(total_spend), 2)          AS total_revenue,
  ROUND(AVG(total_spend), 2)          AS avg_spend,
  ROUND(AVG(customer_satisfaction), 2) AS avg_satisfaction,
  ROUND(AVG(cart_size), 2)            AS avg_cart_size
FROM starbucks_orders
GROUP BY customer_age_group
ORDER BY total_orders DESC;

SELECT
  customer_gender,
  COUNT(order_id)                     AS total_orders,
  ROUND(AVG(total_spend), 2)          AS avg_spend,
  ROUND(AVG(customer_satisfaction), 2) AS avg_satisfaction
FROM starbucks_orders
GROUP BY customer_gender
ORDER BY total_orders DESC;

SELECT
  cart_size,
  COUNT(order_id)            AS orders,
  ROUND(SUM(total_spend), 2) AS revenue,
  ROUND(AVG(total_spend), 2) AS avg_spend
FROM starbucks_orders
GROUP BY cart_size
ORDER BY cart_size;

SELECT
  num_customizations,
  COUNT(order_id)            AS orders,
  ROUND(AVG(total_spend), 2) AS avg_spend,
  ROUND(AVG(customer_satisfaction), 2) AS avg_satisfaction
FROM starbucks_orders
GROUP BY num_customizations
ORDER BY num_customizations;

SELECT
  customer_age_group,
  SUM(CASE WHEN order_channel = 'Mobile App' THEN 1 ELSE 0 END)          AS mobile_app,
  SUM(CASE WHEN order_channel = 'Drive-Thru' THEN 1 ELSE 0 END)          AS drive_thru,
  SUM(CASE WHEN order_channel = 'In-Store Cashier' THEN 1 ELSE 0 END)    AS in_store,
  SUM(CASE WHEN order_channel = 'Kiosk' THEN 1 ELSE 0 END)               AS kiosk
FROM starbucks_orders
GROUP BY customer_age_group
ORDER BY customer_age_group;

SELECT
  is_rewards_member,
  COUNT(order_id)                     AS total_orders,
  ROUND(SUM(total_spend), 2)          AS total_revenue,
  ROUND(AVG(total_spend), 2)          AS avg_spend,
  ROUND(AVG(customer_satisfaction), 2) AS avg_satisfaction,
  ROUND(AVG(num_customizations), 2)   AS avg_customizations,
  ROUND(AVG(cart_size), 2)            AS avg_cart_size,
  ROUND(SUM(CASE WHEN has_food_item='True' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS food_attach_pct
FROM starbucks_orders
GROUP BY is_rewards_member;

SELECT
  ROUND(
    (MAX(CASE WHEN is_rewards_member='True' THEN avg_spend END) -
     MAX(CASE WHEN is_rewards_member='False' THEN avg_spend END)) /
     MAX(CASE WHEN is_rewards_member='False' THEN avg_spend END) * 100, 2
  ) AS loyalty_spend_uplift_pct
FROM (
  SELECT is_rewards_member, AVG(total_spend) AS avg_spend
  FROM starbucks_orders
  GROUP BY is_rewards_member
) t;

SELECT
  region,
  COUNT(order_id)                     AS total_orders,
  ROUND(SUM(total_spend), 2)          AS total_revenue,
  ROUND(AVG(total_spend), 2)          AS avg_spend,
  ROUND(AVG(customer_satisfaction), 2) AS avg_satisfaction,
  COUNT(DISTINCT store_id)            AS num_stores
FROM starbucks_orders
GROUP BY region
ORDER BY total_revenue DESC;

SELECT
  store_location_type,
  COUNT(order_id)            AS total_orders,
  ROUND(SUM(total_spend), 2) AS total_revenue,
  ROUND(AVG(total_spend), 2) AS avg_spend,
  ROUND(AVG(fulfillment_time_min), 2) AS avg_fulfillment_min
FROM starbucks_orders
GROUP BY store_location_type
ORDER BY total_revenue DESC;

SELECT
  store_id,
  store_location_type,
  region,
  COUNT(order_id)            AS total_orders,
  ROUND(SUM(total_spend), 2) AS total_revenue
FROM starbucks_orders
GROUP BY store_id, store_location_type, region
ORDER BY total_revenue DESC
LIMIT 10;

SELECT
  CASE WHEN order_count = 1 THEN 'New Customer' ELSE 'Repeat Customer' END AS customer_type,
  COUNT(*) AS customers,
  ROUND(AVG(total_spent), 2) AS avg_lifetime_spend
FROM (
  SELECT customer_id,
         COUNT(order_id) AS order_count,
         SUM(total_spend) AS total_spent
  FROM starbucks_orders
  GROUP BY customer_id
) t
GROUP BY customer_type;

SELECT
  customer_id,
  COUNT(order_id)            AS total_orders,
  ROUND(SUM(total_spend), 2) AS total_spent,
  ROUND(AVG(total_spend), 2) AS avg_spend,
  ROUND(AVG(customer_satisfaction), 2) AS avg_satisfaction,
  MAX(order_date)            AS last_order_date
FROM starbucks_orders
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

SELECT
  customer_id,
  DATEDIFF(MAX(order_date), MIN(order_date))  AS recency_days,
  COUNT(order_id)                             AS frequency,
  ROUND(SUM(total_spend), 2)                  AS monetary
FROM starbucks_orders
GROUP BY customer_id
ORDER BY monetary DESC
LIMIT 20;

SELECT
  CASE
    WHEN clv_score < 50  THEN 'Low'
    WHEN clv_score < 150 THEN 'Medium'
    WHEN clv_score < 300 THEN 'High'
    ELSE 'VIP'
  END AS clv_tier,
  COUNT(*) AS customers,
  ROUND(AVG(clv_score), 2) AS avg_clv_score,
  ROUND(AVG(total_spent), 2) AS avg_total_spent
FROM (
  SELECT customer_id,
         SUM(total_spend) AS total_spent,
         COUNT(order_id) AS freq,
         AVG(total_spend) * COUNT(order_id) AS clv_score
  FROM starbucks_orders
  GROUP BY customer_id
) t
GROUP BY clv_tier
ORDER BY avg_clv_score DESC;

SELECT
  drink_category,
  COUNT(*) AS total_orders,
  SUM(CASE WHEN has_food_item='True' THEN 1 ELSE 0 END) AS with_food,
  ROUND(SUM(CASE WHEN has_food_item='True' THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS food_attach_pct,
  ROUND(AVG(CASE WHEN has_food_item='True' THEN total_spend END), 2) AS avg_spend_with_food,
  ROUND(AVG(CASE WHEN has_food_item='False' THEN total_spend END), 2) AS avg_spend_without_food
FROM starbucks_orders
GROUP BY drink_category
ORDER BY food_attach_pct DESC;

SELECT
  order_channel,
  drink_category,
  COUNT(*) AS orders,
  ROUND(AVG(total_spend), 2) AS avg_spend
FROM starbucks_orders
GROUP BY order_channel, drink_category
ORDER BY orders DESC
LIMIT 20;

SELECT
  customer_satisfaction,
  COUNT(*) AS orders,
  ROUND(AVG(total_spend), 2) AS avg_spend,
  ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM starbucks_orders), 1) AS pct_of_orders
FROM starbucks_orders
GROUP BY customer_satisfaction
ORDER BY customer_satisfaction DESC;

SELECT
  drink_category,
  ROUND(AVG(customer_satisfaction), 3) AS avg_satisfaction,
  COUNT(*) AS orders
FROM starbucks_orders
GROUP BY drink_category
ORDER BY avg_satisfaction DESC;

SELECT
  region,
  ROUND(AVG(customer_satisfaction), 3) AS avg_satisfaction
FROM starbucks_orders
GROUP BY region
ORDER BY avg_satisfaction DESC;

SELECT
  day_of_week,
  ROUND(AVG(customer_satisfaction), 3) AS avg_satisfaction,
  COUNT(*) AS orders
FROM starbucks_orders
GROUP BY day_of_week
ORDER BY avg_satisfaction DESC;

SELECT
  ROUND(MIN(total_spend), 2)  AS min_spend,
  ROUND(AVG(total_spend), 2)  AS avg_spend,
  ROUND(MAX(total_spend), 2)  AS max_spend,
  ROUND(STDDEV(total_spend), 2) AS std_dev
FROM starbucks_orders;

SELECT COUNT(*) AS high_value_orders,
       ROUND(SUM(total_spend), 2) AS high_value_revenue
FROM starbucks_orders
WHERE total_spend > 18.18;

SELECT
  cart_size,
  num_customizations,
  ROUND(AVG(total_spend), 2) AS avg_spend,
  COUNT(*) AS orders
FROM starbucks_orders
GROUP BY cart_size, num_customizations
ORDER BY avg_spend DESC
LIMIT 15;

SELECT
  YEARWEEK(order_date, 1) AS year_week,
  COUNT(order_id)          AS orders,
  ROUND(SUM(total_spend), 2) AS revenue
FROM starbucks_orders
GROUP BY year_week
ORDER BY year_week;

SELECT
  order_channel,
  COUNT(DISTINCT customer_id)    AS unique_customers,
  COUNT(order_id)                AS total_orders,
  ROUND(SUM(total_spend), 2)     AS revenue,
  ROUND(SUM(total_spend)/COUNT(DISTINCT customer_id), 2) AS revenue_per_customer
FROM starbucks_orders
GROUP BY order_channel
ORDER BY revenue_per_customer DESC;

SELECT
  order_channel,
  store_location_type,
  ROUND(AVG(fulfillment_time_min), 2) AS avg_fulfillment_min,
  COUNT(*) AS orders
FROM starbucks_orders
GROUP BY order_channel, store_location_type
ORDER BY avg_fulfillment_min;
