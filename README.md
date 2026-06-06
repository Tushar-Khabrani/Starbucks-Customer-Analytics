# ☕ Starbucks Customer Analytics

![Python](https://img.shields.io/badge/Python-3.x-blue) ![MySQL](https://img.shields.io/badge/MySQL-8.0-orange) ![Pandas](https://img.shields.io/badge/Pandas-green) ![Matplotlib](https://img.shields.io/badge/Matplotlib-red) ![Seaborn](https://img.shields.io/badge/Seaborn-purple)

A 3-phase end-to-end analytics project on **100,000 Starbucks orders** — progressing from data validation & cleaning → structured SQL analysis → deep-dive Python visualizations. Built to surface actionable business insights around customer behavior, revenue trends, and loyalty patterns.

---

## 🔄 Project Phases

| Phase | Focus | Tools |
|-------|-------|-------|
| Phase 1 | Data Validation & Cleaning | MySQL |
| Phase 2 | KPI Analysis & Structured Queries | MySQL + Python (4 dashboards) |
| Phase 3 | Advanced Analytics — RFM, CLV, Correlations | MySQL + Python (34 charts) |

---

## 📦 Dataset Overview

| Attribute | Value |
|-----------|-------|
| Total Orders | 100,000 |
| Unique Customers | 14,988 |
| Total Columns | 20 |
| Date Range | Jan 2024 – Jan 2026 |
| File | starbucks_orders.csv |

**Key columns:** order_id, customer_id, order_date, order_channel, region, drink_category, total_spend, customer_satisfaction, is_rewards_member, fulfillment_time_min

---

## 📊 Key KPIs

| Metric | Value |
|--------|-------|
| Total Revenue | $1,486,677 |
| Avg Order Value | $14.87 |
| Customer LTV | $99.19 |
| Avg Satisfaction | 3.69 / 5 |
| Avg Fulfillment Time | 4.55 min |
| Rewards Member % | 47.72% |
| Order Ahead % | 29.79% |
| Food Attach Rate | 31.58% |
| Peak Hour | 7 AM (10,200+ orders, ~$150K revenue) |
| Top Region by Revenue | West ($337.4K) |

---

## 💡 Key Insights

- **Peak window:** 7 AM daily — 10,200+ orders generating ~$150K revenue; Saturday peaks at $216.1K
- **Top channel:** Mobile App drives 42.5% of all orders; 25–34 age group most active with 16,368 Mobile App orders
- **Loyalty uplift:** Rewards members spend $15.72 vs $14.09 non-members — **+11.6% uplift** · total revenue nearly equal ($750K vs $737K)
- **Order Ahead premium:** Order Ahead customers spend $18.09 vs $13.50 walk-in — **+34% higher spend**
- **Suburban dominance:** Suburban stores lead with $531.8K revenue vs Urban $482.7K vs Rural $472.1K
- **Age spend pattern:** 18–24 and 25–34 highest spenders ($15.55/$15.54) — 55+ lowest at $13.06
- **Customization = revenue:** 0 customizations avg $12.14 → 8 customizations avg $22.89 — clear positive correlation
- **CLV tiers:** 11,660 Medium · 1,747 High · 1,580 Low · 1 VIP customer across 14,988 total
- **RFM segments:** K-Means clustering reveals Platinum, Gold, Silver, Bronze customer segments
- **Spend concentration:** 63,356 orders (63%) fall in $10–$20 bucket · only 1,065 above $30
- **Satisfaction by region:** Southeast leads (3.703) · Midwest lowest (3.670) — all tightly clustered
- **Correlation insight:** cart_size vs total_spend strongest correlation (0.90) · fulfillment_time has near-zero correlation with satisfaction

---

## 🗄️ SQL Analysis

### Phase 1 — Data Validation & Cleaning
- NULL checks across all 20 columns
- Duplicate order_id detection
- Data type validation
- Created `clean_orders` table

### Phase 2 — KPI & Aggregations
- Revenue, AOV, satisfaction, and fulfillment analysis across regions, channels, and store types
- Peak time analysis — hourly, daily, Morning/Afternoon/Evening/Night segments
- Order channel breakdown: Mobile App 42.5% · Drive-Thru 28% · In-Store 22.1% · Kiosk 7.4%
- Rewards member behavior analysis with RANK() window functions
- 6 structured output tables created

### Phase 3 — Advanced Analysis
- **RFM Analysis** — Recency, Frequency, Monetary scoring per customer → Platinum / Gold / Silver / Bronze segments
- **CLV Scoring** — tiered into Low / Medium / High / VIP (11,660 Medium · 1,747 High · 1,580 Low · 1 VIP)
- Food attach rate by drink category (Refresher leads at 32.19%)
- Loyalty spend uplift % calculation
- Cross-tab: Age Group × Order Channel heatmap
- Spend bucket distribution ($0–$10: 19,460 · $10–$20: 63,356 · $20–$30: 16,118)
- Weekly trend analysis using YEARWEEK · STDDEV of spend
- Fulfillment time by channel (Drive-Thru 5.80 min · In-Store fastest at 3.20 min)

---

## 📈 Python Visualizations

### Phase 2 — 4 Multi-Panel Dashboards

#### 📊 Dashboard 1 — Executive Overview
![Executive Dashboard](charts/phase1/01_executive_dashboard.png)
KPI cards (100K orders · $1.49M revenue · 14,988 customers · $14.87 AOV · 3.69★ · 47.7% rewards) | Revenue by Region — West leads $0.34M | Drink Category Mix — near-equal 6-way split | Order Volume by Hour — sharp peak at 7 AM (10,200+ orders)

#### 👥 Dashboard 2 — Customer Behaviour
![Customer Behaviour](charts/phase1/02_customer_behaviour.png)
Rewards vs Non-Rewards avg spend ($15.72 vs $14.09 · +11.6% uplift) | Orders by Channel — Mobile App 42,521 · Drive-Thru 27,996 · In-Store 22,063 · Kiosk 7,420 | Satisfaction by Drink (all ~3.69) | Age Group 25–34 leads 30K orders | Fulfillment Mean 4.5 min | Order Ahead vs Walk-in comparison

#### 🕐 Dashboard 3 — Time & Location Patterns
![Time Location](charts/phase1/03_time_location_patterns.png)
Avg Spend Heatmap Day×Hour | Orders by Day — Saturday peaks at 14,443 | Revenue by Store Type — Suburban $0.53M · Urban $0.48M · Rural $0.47M | Cart Size Distribution — avg 3.7 items

#### 🌍 Dashboard 4 — Regional & Demographic Breakdown
![Regional Demographic](charts/phase1/04_regional_demographic.png)
Drink Mix by Region % — near-equal across all 5 regions | Customizations vs Satisfaction bubble chart — more customizations = slightly higher satisfaction | Avg Spend by Gender & Rewards — Rewards members spend ~$2 more across all genders

---

### Phase 3 — 34 Individual Charts

**Drink & Revenue**
- `01_top_drink_categories_orders` — Refresher leads (16,808) in near-equal 6-category split
- `02_revenue_by_drink_category` — All categories tightly clustered $245.9K–$249.7K
- `03_daily_revenue_trend` — Consistent $1,600–$2,600/day across Jan 2024–Jan 2026
- `04_monthly_revenue_trend` — Stable $58K–$65K monthly over 24 months

**Time & Hour**
- `05_orders_by_hour` — Sharp 7 AM peak (10,200+ orders); secondary peaks at 12:00 and 16:00
- `06_revenue_by_hour` — Peak revenue at 7 AM (~$150K); mirrors order pattern
- `07_revenue_by_day_of_week` — Saturday leads $216.1K · Wednesday lowest $208.8K
- `08_orders_by_day_of_week` — Near-equal daily distribution ~14,120–14,443

**Regional & Store**
- `09_region_revenue` — West leads $337.4K · Northeast lowest $267.2K
- `10_store_location_revenue` — Suburban $531.8K · Urban $482.7K · Rural $472.1K
- `11_order_channel_distribution` — Mobile App 42.5% · Drive-Thru 28% · In-Store 22.1% · Kiosk 7.4%

**Loyalty & Demographics**
- `12_loyalty_analysis` — Rewards $15.72 vs Non-Rewards $14.09 · total revenue $750K vs $737K
- `13_age_group_orders` — 25–34 leads (29,782) · 55+ lowest (10,019)
- `14_avg_spend_by_age_group` — 18–24 highest ($15.55) · 55+ lowest ($13.06)
- `15_gender_analysis` — Female 45,306 · Male 44,767 · avg spend nearly equal $14.83–$14.96

**Cart & Customization**
- `16_cart_size_analysis` — Cart size 3–4 dominates (23,982/21,615 orders · $303.7K/$335.9K revenue)
- `17_customization_analysis` — Spend rises from $12.14 (0 customizations) → $22.89 (8 customizations)

**Satisfaction**
- `19_satisfaction_distribution` — Score 4 most common (35,001) · Score 1 lowest (6,294)
- `20_drink_satisfaction_ranking` — All categories 3.68–3.69 · Brewed Coffee leads (3.6922)
- `34_region_satisfaction` — Southeast leads (3.703) · Midwest lowest (3.670)

**Spend Distribution**
- `21_spend_distribution_histogram` — Near-normal · avg $14.87 · most orders $10–$18 · right-skewed tail
- `22_spend_boxplot` — IQR $11–$18 · outliers visible above $29 up to $40
- `23_spend_by_bucket` — $10–$20 dominates (63,356 orders · 63%) · only 1,065 above $30

**Advanced Analytics**
- `25_top10_customers` — Top customer CUST_08642 at $301.68 lifetime spend
- `26_top10_stores` — Top store STR_240 at $3,541 · top 10 tightly clustered $3,407–$3,541
- `27_rfm_customer_segments` — K-Means: Platinum (high frequency/spend) · Gold · Silver · Bronze
- `28_clv_tier_distribution` — Medium 11,660 · High 1,747 · Low 1,580 · VIP 1
- `29_food_attach_rate_by_drink` — Refresher 32.19% · Tea lowest 31.07% · all categories ~31–32%
- `30_channel_fulfillment_time` — Drive-Thru slowest (5.80 min) · In-Store fastest (3.20 min)
- `31_order_ahead_analysis` — Order Ahead: 29,793 orders · avg spend $18.09 vs Walk-in $13.50 (+34%)
- `32_age_channel_heatmap` — 25–34 × Mobile App highest (16,368) · 55+ × Mobile App lowest (981)
- `33_correlation_heatmap` — cart_size↔total_spend strongest (0.90) · order_ahead↔total_spend (0.38) · fulfillment_time near-zero correlation with satisfaction

---

## 📁 Project Structure

    starbucks-customer-analytics/
    ├── data/
    │   └── starbucks_orders.csv
    ├── sql/
    │   ├── 01_data_validation_cleaning.sql
    │   ├── 02_kpi_and_aggregations.sql
    │   └── 03_advanced_analysis.sql
    ├── python/
    │   ├── analysis_phase1.py
    │   ├── analysis_phase2.py
    │   └── analysis_phase3.py
    ├── charts/
    │   ├── phase2/  (4 dashboard PNGs)
    │   └── phase3/  (34 chart PNGs)
    └── README.md

---

## ▶️ How to Run

1. Clone: `git clone https://github.com/tushar-khabrani/starbucks-customer-analytics`
2. Import SQL files into MySQL in order: Phase 1 → Phase 2 → Phase 3
3. Install dependencies: `pip install pandas matplotlib seaborn scikit-learn`
4. Run scripts: `python python/analysis_phase2.py` or `python python/analysis_phase3.py`

---

## 🤖 AI Integration
Applied AI-assisted scripting to accelerate plotting templates — all SQL logic, business analysis, and insight interpretation independently developed and validated.

---

## 👤 Author
**Tushar Khabrani** — [LinkedIn](https://www.linkedin.com/in/tusharkhabrani104) · [GitHub](https://github.com/tushar-khabrani)
