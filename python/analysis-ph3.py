import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os
import warnings
warnings.filterwarnings("ignore")

os.makedirs("charts", exist_ok=True)

COLORS = {
    "primary":   "#00704A",
    "secondary": "#1E3932",
    "accent":    "#CBA258",
    "light":     "#D4E9E2",
    "bg":        "#F9F6EF",
    "text":      "#1E3932",
    "muted":     "#6B7280",
}
PALETTE = ["#00704A","#1E3932","#CBA258","#2DD4BF","#F97316","#6366F1"]

plt.rcParams.update({
    "figure.facecolor": COLORS["bg"],
    "axes.facecolor":   COLORS["bg"],
    "axes.edgecolor":   "#E5E7EB",
    "axes.labelcolor":  COLORS["text"],
    "text.color":       COLORS["text"],
    "xtick.color":      COLORS["muted"],
    "ytick.color":      COLORS["muted"],
    "font.family":      "DejaVu Sans",
    "figure.dpi":       130,
})

def save(name):
    plt.tight_layout()
    plt.savefig(f"charts/{name}.png", dpi=150, bbox_inches="tight", facecolor=COLORS["bg"])
    plt.close()
    print(f"  chart saved -> {name}.png")

df = pd.read_csv("starbucks_orders.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df["order_time"] = pd.to_datetime(df["order_time"], format="%H:%M", errors="coerce")
df["hour"]       = df["order_time"].dt.hour
df["month"]      = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%b-%Y")
df["week"]       = df["order_date"].dt.isocalendar().week.astype(int)
day_order        = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

print("=" * 60)
print("SECTION 1 — DATASET OVERVIEW")
print("=" * 60)
print(f"Shape              : {df.shape}")
print(f"Columns            : {list(df.columns)}")
print()
print("NULL VALUES:")
print(df.isnull().sum())
print()
print(f"Duplicate rows     : {df.duplicated().sum()}")
print()

print("=" * 60)
print("SECTION 2 — KPI CARDS")
print("=" * 60)
total_orders      = df["order_id"].count()
unique_customers  = df["customer_id"].nunique()
total_revenue     = df["total_spend"].sum()
avg_order_value   = df["total_spend"].mean()
max_spend         = df["total_spend"].max()
min_spend         = df["total_spend"].min()
avg_fulfillment   = df["fulfillment_time_min"].mean()
rewards_pct       = (df["is_rewards_member"] == True).mean() * 100
food_attach_rate  = (df["has_food_item"] == True).mean() * 100
order_ahead_rate  = (df["order_ahead"] == True).mean() * 100
avg_satisfaction  = df["customer_satisfaction"].mean()
avg_cart_size     = df["cart_size"].mean()

kpis = {
    "Total Orders":        f"{total_orders:,}",
    "Unique Customers":    f"{unique_customers:,}",
    "Total Revenue":       f"${total_revenue:,.2f}",
    "Avg Order Value":     f"${avg_order_value:.2f}",
    "Max Spend":           f"${max_spend:.2f}",
    "Min Spend":           f"${min_spend:.2f}",
    "Avg Fulfillment Min": f"{avg_fulfillment:.2f}",
    "Rewards Member %":    f"{rewards_pct:.1f}%",
    "Food Attach Rate":    f"{food_attach_rate:.1f}%",
    "Order Ahead Rate":    f"{order_ahead_rate:.1f}%",
    "Avg Satisfaction":    f"{avg_satisfaction:.2f} / 5",
    "Avg Cart Size":       f"{avg_cart_size:.2f}",
}
for k, v in kpis.items():
    print(f"  {k:<25} : {v}")
print()

print("=" * 60)
print("SECTION 3 — DRINK CATEGORY ANALYSIS")
print("=" * 60)
drink_sales = df["drink_category"].value_counts()
category_perf = df.groupby("drink_category").agg(
    orders=("order_id","count"),
    revenue=("total_spend","sum"),
    avg_spend=("total_spend","mean"),
    avg_fulfillment=("fulfillment_time_min","mean"),
    avg_satisfaction=("customer_satisfaction","mean")
).sort_values("revenue", ascending=False)
most_profitable = category_perf.index[0]
print(category_perf.round(2))
print(f"\nMost Profitable Category : {most_profitable}")
print()

print("=" * 60)
print("SECTION 4 — REVENUE ANALYSIS")
print("=" * 60)
print(df["total_spend"].describe().round(2))
revenue_trend   = df.groupby("order_date")["total_spend"].sum()
monthly_revenue = df.groupby(df["order_date"].dt.to_period("M"))["total_spend"].sum()
day_revenue     = df.groupby("day_of_week")["total_spend"].sum().reindex(day_order)
day_orders_cnt  = df.groupby("day_of_week")["order_id"].count().reindex(day_order)
print()

print("=" * 60)
print("SECTION 5 — PEAK ORDER TIME")
print("=" * 60)
hourly_orders  = df.groupby("hour")["order_id"].count()
hourly_revenue = df.groupby("hour")["total_spend"].sum()
peak_order_hour   = hourly_orders.idxmax()
peak_revenue_hour = hourly_revenue.idxmax()
print(f"Peak Order Hour   : {peak_order_hour}:00")
print(f"Peak Revenue Hour : {peak_revenue_hour}:00")
print()
print("Hourly Orders:")
print(hourly_orders)
print()

print("=" * 60)
print("SECTION 6 — ORDER PREFERENCE INSIGHTS")
print("=" * 60)
channel_perf = df.groupby("order_channel").agg(
    orders=("order_id","count"),
    revenue=("total_spend","sum"),
    avg_spend=("total_spend","mean"),
    avg_fulfillment=("fulfillment_time_min","mean")
).sort_values("orders", ascending=False)
print("Order Channel:")
print(channel_perf.round(2))
print()
print("Order Ahead:")
print(df.groupby("order_ahead").agg(orders=("order_id","count"), avg_spend=("total_spend","mean")).round(2))
print()

print("=" * 60)
print("SECTION 7 — LOYALTY / REWARDS ANALYSIS")
print("=" * 60)
rewards_perf = df.groupby("is_rewards_member").agg(
    orders=("order_id","count"),
    revenue=("total_spend","sum"),
    avg_spend=("total_spend","mean"),
    avg_satisfaction=("customer_satisfaction","mean"),
    avg_customizations=("num_customizations","mean")
)
print(rewards_perf.round(2))
loyalty_avg     = rewards_perf.loc[True,"avg_spend"]
non_loyalty_avg = rewards_perf.loc[False,"avg_spend"]
spend_uplift    = (loyalty_avg - non_loyalty_avg) / non_loyalty_avg * 100
print(f"\nLoyalty Spend Uplift : +{spend_uplift:.1f}% vs non-members")
print()

print("=" * 60)
print("SECTION 8 — REGION PERFORMANCE")
print("=" * 60)
region_perf = df.groupby("region").agg(
    orders=("order_id","count"),
    revenue=("total_spend","sum"),
    avg_spend=("total_spend","mean"),
    avg_satisfaction=("customer_satisfaction","mean")
).sort_values("revenue", ascending=False)
store_perf = df.groupby("store_location_type").agg(
    orders=("order_id","count"),
    revenue=("total_spend","sum"),
    avg_spend=("total_spend","mean")
).sort_values("revenue", ascending=False)
print(region_perf.round(2))
print()
print("Store Location Type:")
print(store_perf.round(2))
print()

print("=" * 60)
print("SECTION 9 — CUSTOMER BEHAVIOUR")
print("=" * 60)
age_analysis = df.groupby("customer_age_group").agg(
    orders=("order_id","count"),
    avg_spend=("total_spend","mean"),
    avg_satisfaction=("customer_satisfaction","mean")
).sort_values("orders", ascending=False)
gender_analysis = df.groupby("customer_gender").agg(
    orders=("order_id","count"),
    avg_spend=("total_spend","mean")
).sort_values("orders", ascending=False)
cart_analysis = df.groupby("cart_size").agg(
    orders=("order_id","count"),
    revenue=("total_spend","sum"),
    avg_spend=("total_spend","mean")
)
custom_analysis = df.groupby("num_customizations").agg(
    orders=("order_id","count"),
    avg_spend=("total_spend","mean")
)
print("Age Group:")
print(age_analysis.round(2))
print()
print("Gender:")
print(gender_analysis.round(2))
print()
print("Cart Size:")
print(cart_analysis.round(2))
print()
print("Customizations:")
print(custom_analysis.round(2))
print()

print("=" * 60)
print("SECTION 10 — FOOD vs DRINK ANALYSIS")
print("=" * 60)
food_analysis = df.groupby("has_food_item").agg(
    orders=("order_id","count"),
    revenue=("total_spend","sum"),
    avg_spend=("total_spend","mean")
)
print(food_analysis.round(2))
print()

print("=" * 60)
print("SECTION 11 — SATISFACTION ANALYSIS")
print("=" * 60)
satisfaction = df.groupby("customer_satisfaction").agg(
    orders=("order_id","count"),
    avg_spend=("total_spend","mean")
).sort_index(ascending=False)
drink_satisfaction = df.groupby("drink_category")["customer_satisfaction"].mean().sort_values(ascending=False)
print(satisfaction.round(2))
print()
print("Drink Satisfaction Ranking:")
print(drink_satisfaction.round(4))
print()

print("=" * 60)
print("SECTION 12 — TOP STORES & TOP CUSTOMERS")
print("=" * 60)
store_ranking = df.groupby("store_id").agg(
    orders=("order_id","count"),
    revenue=("total_spend","sum")
).sort_values("revenue", ascending=False).head(10)
top_customers = df.groupby("customer_id").agg(
    orders=("order_id","count"),
    total_spent=("total_spend","sum")
).sort_values("total_spent", ascending=False).head(10)
print("Top 10 Stores:")
print(store_ranking)
print()
print("Top 10 Customers:")
print(top_customers)
print()

print("=" * 60)
print("SECTION 13 — REPEAT vs NEW CUSTOMERS")
print("=" * 60)
customer_order_counts = df.groupby("customer_id")["order_id"].count()
repeat_customers = (customer_order_counts > 1).sum()
new_customers    = (customer_order_counts == 1).sum()
print(f"Repeat Customers : {repeat_customers:,}")
print(f"New Customers    : {new_customers:,}")
print()

print("=" * 60)
print("SECTION 14 — PRICE / SPEND ANALYSIS")
print("=" * 60)
spend_bins = pd.cut(df["total_spend"],
    bins=[0,10,20,30,40,50,100],
    labels=["$0-10","$10-20","$20-30","$30-40","$40-50","$50+"])
spend_dist = spend_bins.value_counts().sort_index()
print(spend_dist)
print()

print("=" * 60)
print("SECTION 15 — RFM ANALYSIS + K-MEANS SEGMENTATION")
print("=" * 60)
rfm = df.groupby("customer_id").agg(
    recency=("order_date","max"),
    frequency=("order_id","count"),
    monetary=("total_spend","sum")
).reset_index()
rfm["recency"] = (df["order_date"].max() - rfm["recency"]).dt.days
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[["recency","frequency","monetary"]])
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm["segment"] = kmeans.fit_predict(rfm_scaled)
seg_labels = {s: name for s, name in zip(
    rfm.groupby("segment")["monetary"].mean().sort_values().index,
    ["Bronze","Silver","Gold","Platinum"]
)}
rfm["seg_name"] = rfm["segment"].map(seg_labels)
seg_summary = rfm.groupby("seg_name").agg(
    customers=("customer_id","count"),
    avg_recency=("recency","mean"),
    avg_frequency=("frequency","mean"),
    avg_monetary=("monetary","mean")
)
print(seg_summary.round(2))
print()

print("=" * 60)
print("SECTION 16 — CUSTOMER LIFETIME VALUE (CLV)")
print("=" * 60)
clv = df.groupby("customer_id").agg(
    total_orders=("order_id","count"),
    total_spent=("total_spend","sum"),
    avg_order_value=("total_spend","mean")
).reset_index()
clv["clv_score"] = clv["avg_order_value"] * clv["total_orders"]
clv["clv_tier"]  = pd.cut(clv["clv_score"],
    bins=[0,50,150,300,float("inf")], labels=["Low","Medium","High","VIP"])
clv_tier_summary = clv.groupby("clv_tier", observed=True).agg(
    customers=("customer_id","count"),
    avg_clv=("clv_score","mean"),
    avg_total_spent=("total_spent","mean")
)
print(clv_tier_summary.round(2))
print()

print("=" * 60)
print("SECTION 17 — MARKET BASKET ANALYSIS")
print("=" * 60)
drink_food = df.groupby(["drink_category","has_food_item"]).agg(
    orders=("order_id","count")).reset_index()
drink_food_pivot = drink_food.pivot(
    index="drink_category", columns="has_food_item", values="orders").fillna(0)
drink_food_pivot.columns = ["no_food","with_food"]
drink_food_pivot["food_attach_%"] = (
    drink_food_pivot["with_food"] /
    (drink_food_pivot["no_food"] + drink_food_pivot["with_food"]) * 100
).round(2)
print("Food Attach Rate by Drink Category:")
print(drink_food_pivot.sort_values("food_attach_%", ascending=False))
print()
age_channel = df.groupby(["customer_age_group","order_channel"]).agg(
    orders=("order_id","count")).reset_index()
age_ch_piv = age_channel.pivot(
    index="customer_age_group", columns="order_channel", values="orders").fillna(0)
print("Age Group x Channel Cross-tab:")
print(age_ch_piv.astype(int))
print()

print("=" * 60)
print("SECTION 18 — BUSINESS INSIGHTS SUMMARY")
print("=" * 60)
top_region   = region_perf.index[0]
top_channel  = df["order_channel"].value_counts().index[0]
top_age      = age_analysis.index[0]
best_sat_drink = drink_satisfaction.index[0]
vip_count    = int(clv_tier_summary.loc["VIP","customers"]) if "VIP" in clv_tier_summary.index else 0
print(f"  1.  Total Revenue                  : ${total_revenue:,.2f}")
print(f"  2.  Most Profitable Drink Category : {most_profitable}")
print(f"  3.  Peak Sales Hour                : {peak_order_hour}:00")
print(f"  4.  Peak Revenue Hour              : {peak_revenue_hour}:00")
print(f"  5.  Top Performing Region          : {top_region}")
print(f"  6.  Most Used Order Channel        : {top_channel}")
print(f"  7.  Highest Ordering Age Group     : {top_age}")
print(f"  8.  Best Satisfaction Drink        : {best_sat_drink}")
print(f"  9.  Loyalty Spend Uplift           : +{spend_uplift:.1f}% vs non-members")
print(f" 10.  Repeat vs New Customers        : {repeat_customers:,} vs {new_customers:,}")
print(f" 11.  VIP Tier Customers             : {vip_count:,}")
print(f" 12.  Food Attach Rate               : {food_attach_rate:.1f}%")
print(f" 13.  Avg Customer Satisfaction      : {avg_satisfaction:.2f} / 5")
print(f" 14.  Rewards Member %               : {rewards_pct:.1f}%")
print()

print("=" * 60)
print("SECTION 19 — CORRELATION MATRIX")
print("=" * 60)
corr = df.corr(numeric_only=True)
print(corr.round(3))
print()

print("=" * 60)
print("GENERATING CHARTS...")
print("=" * 60)

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(drink_sales.index, drink_sales.values, color=PALETTE, edgecolor="white", linewidth=0.5)
ax.bar_label(bars, fmt="%d", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Top Selling Drink Categories (Orders)", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Total Orders")
ax.spines[["top","right"]].set_visible(False)
ax.tick_params(axis="x", rotation=15)
save("01_top_drink_categories_orders")

fig, ax = plt.subplots(figsize=(9, 5))
rev_data = category_perf["revenue"].sort_values(ascending=False)
bars = ax.bar(rev_data.index, rev_data.values / 1000, color=PALETTE, edgecolor="white")
ax.bar_label(bars, fmt="$%.1fK", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Revenue by Drink Category ($K)", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Revenue ($K)")
ax.spines[["top","right"]].set_visible(False)
ax.tick_params(axis="x", rotation=15)
save("02_revenue_by_drink_category")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(revenue_trend.index, revenue_trend.values, color=COLORS["primary"], linewidth=1.2)
ax.fill_between(revenue_trend.index, revenue_trend.values, alpha=0.15, color=COLORS["primary"])
ax.set_title("Daily Revenue Trend", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Revenue ($)")
ax.spines[["top","right"]].set_visible(False)
ax.tick_params(axis="x", rotation=30)
save("03_daily_revenue_trend")

fig, ax = plt.subplots(figsize=(12, 5))
x_labels = [str(p) for p in monthly_revenue.index]
bars = ax.bar(x_labels, monthly_revenue.values / 1000, color=COLORS["primary"], edgecolor="white")
ax.bar_label(bars, fmt="$%.1fK", fontsize=8, padding=3, color=COLORS["text"])
ax.set_title("Monthly Revenue Trend ($K)", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Revenue ($K)")
ax.spines[["top","right"]].set_visible(False)
ax.tick_params(axis="x", rotation=30)
save("04_monthly_revenue_trend")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_orders.index, hourly_orders.values, color=COLORS["primary"], linewidth=2.5, marker="o", markersize=5)
ax.axvline(peak_order_hour, color=COLORS["accent"], linestyle="--", linewidth=2, label=f"Peak: {peak_order_hour}:00")
ax.fill_between(hourly_orders.index, hourly_orders.values, alpha=0.12, color=COLORS["primary"])
ax.legend(fontsize=10)
ax.set_title(f"Orders by Hour of Day  |  Peak: {peak_order_hour}:00", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Hour")
ax.set_ylabel("Total Orders")
ax.spines[["top","right"]].set_visible(False)
save("05_orders_by_hour")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_revenue.index, hourly_revenue.values / 1000, color=COLORS["accent"], linewidth=2.5, marker="s", markersize=5)
ax.fill_between(hourly_revenue.index, hourly_revenue.values / 1000, alpha=0.12, color=COLORS["accent"])
ax.set_title(f"Revenue by Hour  |  Peak Revenue: {peak_revenue_hour}:00", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Hour")
ax.set_ylabel("Revenue ($K)")
ax.spines[["top","right"]].set_visible(False)
save("06_revenue_by_hour")

fig, ax = plt.subplots(figsize=(9, 5))
bar_colors = [COLORS["accent"] if d == "Sat" else COLORS["primary"] for d in day_order]
bars = ax.bar(day_order, day_revenue.values / 1000, color=bar_colors, edgecolor="white")
ax.bar_label(bars, fmt="$%.1fK", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Revenue by Day of Week  |  Saturday Peak", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Revenue ($K)")
ax.spines[["top","right"]].set_visible(False)
save("07_revenue_by_day_of_week")

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(day_order, day_orders_cnt.values, color=COLORS["secondary"], edgecolor="white")
ax.bar_label(bars, fmt="%d", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Orders by Day of Week", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Total Orders")
ax.spines[["top","right"]].set_visible(False)
save("08_orders_by_day_of_week")

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(region_perf.index, region_perf["revenue"] / 1000,
               color=sns.color_palette("Greens_r", len(region_perf)), edgecolor="white")
ax.bar_label(bars, fmt="$%.1fK", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Revenue by Region ($K)", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Revenue ($K)")
ax.spines[["top","right"]].set_visible(False)
save("09_region_revenue")

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(store_perf.index, store_perf["revenue"] / 1000,
              color=[COLORS["primary"], COLORS["accent"], COLORS["secondary"]], edgecolor="white")
ax.bar_label(bars, fmt="$%.1fK", fontsize=10, padding=3, color=COLORS["text"])
ax.set_title("Revenue by Store Location Type ($K)", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Revenue ($K)")
ax.spines[["top","right"]].set_visible(False)
save("10_store_location_revenue")

fig, ax = plt.subplots(figsize=(8, 7))
ch_data = df["order_channel"].value_counts()
wedges, texts, autotexts = ax.pie(
    ch_data.values, labels=ch_data.index,
    autopct="%1.1f%%", colors=PALETTE, startangle=90,
    wedgeprops={"edgecolor":"white","linewidth":2})
for at in autotexts:
    at.set_fontsize(10)
ax.set_title("Order Channel Distribution", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
save("11_order_channel_distribution")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
bars1 = axes[0].bar(["Non-Member","Rewards Member"],
    [non_loyalty_avg, loyalty_avg],
    color=["#94A3B8", COLORS["primary"]], edgecolor="white")
axes[0].bar_label(bars1, fmt="$%.2f", fontsize=10, padding=3, color=COLORS["text"])
axes[0].set_title(f"Avg Spend: Loyalty vs Non-Loyalty\n(+{spend_uplift:.1f}% uplift)", fontsize=12, fontweight="bold", color=COLORS["secondary"])
axes[0].set_ylabel("Avg Spend ($)")
axes[0].spines[["top","right"]].set_visible(False)
bars2 = axes[1].bar(["Non-Member","Rewards Member"],
    [rewards_perf.loc[False,"revenue"] / 1000, rewards_perf.loc[True,"revenue"] / 1000],
    color=["#94A3B8", COLORS["primary"]], edgecolor="white")
axes[1].bar_label(bars2, fmt="$%.0fK", fontsize=10, padding=3, color=COLORS["text"])
axes[1].set_title("Total Revenue: Loyalty vs Non-Loyalty", fontsize=12, fontweight="bold", color=COLORS["secondary"])
axes[1].set_ylabel("Revenue ($K)")
axes[1].spines[["top","right"]].set_visible(False)
save("12_loyalty_analysis")

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(age_analysis.index, age_analysis["orders"],
               color=sns.color_palette("YlOrBr_r", len(age_analysis)), edgecolor="white")
ax.bar_label(bars, fmt="%d", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Orders by Age Group", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Total Orders")
ax.spines[["top","right"]].set_visible(False)
save("13_age_group_orders")

fig, ax = plt.subplots(figsize=(9, 5))
age_sorted = age_analysis.sort_values("avg_spend", ascending=False)
bars = ax.bar(age_sorted.index, age_sorted["avg_spend"],
              color=sns.color_palette("YlOrBr", len(age_sorted)), edgecolor="white")
ax.bar_label(bars, fmt="$%.2f", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Avg Spend by Age Group", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Avg Spend ($)")
ax.spines[["top","right"]].set_visible(False)
save("14_avg_spend_by_age_group")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
bars1 = axes[0].bar(gender_analysis.index, gender_analysis["orders"],
    color=PALETTE[:len(gender_analysis)], edgecolor="white")
axes[0].bar_label(bars1, fmt="%d", fontsize=9, padding=3, color=COLORS["text"])
axes[0].set_title("Orders by Gender", fontsize=12, fontweight="bold", color=COLORS["secondary"])
axes[0].set_ylabel("Total Orders")
axes[0].spines[["top","right"]].set_visible(False)
axes[0].tick_params(axis="x", rotation=15)
bars2 = axes[1].bar(gender_analysis.index, gender_analysis["avg_spend"],
    color=PALETTE[:len(gender_analysis)], edgecolor="white")
axes[1].bar_label(bars2, fmt="$%.2f", fontsize=9, padding=3, color=COLORS["text"])
axes[1].set_title("Avg Spend by Gender", fontsize=12, fontweight="bold", color=COLORS["secondary"])
axes[1].set_ylabel("Avg Spend ($)")
axes[1].spines[["top","right"]].set_visible(False)
axes[1].tick_params(axis="x", rotation=15)
save("15_gender_analysis")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
colors16 = sns.color_palette("BuGn", len(cart_analysis))
bars1 = axes[0].bar(cart_analysis.index.astype(str), cart_analysis["orders"],
    color=colors16, edgecolor="white")
axes[0].bar_label(bars1, fmt="%d", fontsize=8, padding=3, color=COLORS["text"])
axes[0].set_title("Orders by Cart Size", fontsize=12, fontweight="bold", color=COLORS["secondary"])
axes[0].set_xlabel("Cart Size")
axes[0].spines[["top","right"]].set_visible(False)
bars2 = axes[1].bar(cart_analysis.index.astype(str), cart_analysis["revenue"] / 1000,
    color=colors16, edgecolor="white")
axes[1].bar_label(bars2, fmt="$%.1fK", fontsize=8, padding=3, color=COLORS["text"])
axes[1].set_title("Revenue by Cart Size ($K)", fontsize=12, fontweight="bold", color=COLORS["secondary"])
axes[1].set_xlabel("Cart Size")
axes[1].spines[["top","right"]].set_visible(False)
save("16_cart_size_analysis")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
bars1 = axes[0].bar(custom_analysis.index.astype(str), custom_analysis["orders"],
    color=COLORS["secondary"], edgecolor="white")
axes[0].bar_label(bars1, fmt="%d", fontsize=9, padding=3, color=COLORS["text"])
axes[0].set_title("Orders by No. of Customizations", fontsize=12, fontweight="bold", color=COLORS["secondary"])
axes[0].set_xlabel("Customizations")
axes[0].spines[["top","right"]].set_visible(False)
bars2 = axes[1].bar(custom_analysis.index.astype(str), custom_analysis["avg_spend"],
    color=COLORS["accent"], edgecolor="white")
axes[1].bar_label(bars2, fmt="$%.2f", fontsize=9, padding=3, color=COLORS["text"])
axes[1].set_title("Avg Spend by No. of Customizations", fontsize=12, fontweight="bold", color=COLORS["secondary"])
axes[1].set_xlabel("Customizations")
axes[1].spines[["top","right"]].set_visible(False)
save("17_customization_analysis")

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
labels18 = ["No Food","With Food"]
bars1 = axes[0].bar(labels18, food_analysis["orders"].values,
    color=[COLORS["muted"], COLORS["primary"]], edgecolor="white")
axes[0].bar_label(bars1, fmt="%d", fontsize=10, padding=3, color=COLORS["text"])
axes[0].set_title("Orders: Food vs No Food", fontsize=12, fontweight="bold", color=COLORS["secondary"])
axes[0].spines[["top","right"]].set_visible(False)
bars2 = axes[1].bar(labels18, food_analysis["avg_spend"].values,
    color=[COLORS["muted"], COLORS["primary"]], edgecolor="white")
axes[1].bar_label(bars2, fmt="$%.2f", fontsize=10, padding=3, color=COLORS["text"])
axes[1].set_title("Avg Spend: Food vs No Food", fontsize=12, fontweight="bold", color=COLORS["secondary"])
axes[1].spines[["top","right"]].set_visible(False)
save("18_food_vs_no_food")

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(satisfaction.index.astype(str), satisfaction["orders"],
              color=sns.color_palette("RdYlGn", len(satisfaction))[::-1], edgecolor="white")
ax.bar_label(bars, fmt="%d", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Customer Satisfaction Distribution", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Satisfaction Score")
ax.set_ylabel("Total Orders")
ax.spines[["top","right"]].set_visible(False)
save("19_satisfaction_distribution")

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(drink_satisfaction.index, drink_satisfaction.values,
               color=sns.color_palette("Greens_r", len(drink_satisfaction)), edgecolor="white")
ax.bar_label(bars, fmt="%.4f", fontsize=9, padding=3, color=COLORS["text"])
ax.set_xlim(3.60, 3.72)
ax.set_title("Avg Satisfaction Score by Drink Category", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Avg Satisfaction Score")
ax.spines[["top","right"]].set_visible(False)
save("20_drink_satisfaction_ranking")

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df["total_spend"], bins=40, color=COLORS["primary"], edgecolor="white", alpha=0.85)
ax.axvline(avg_order_value, color=COLORS["accent"], linestyle="--", linewidth=2.5,
           label=f"Avg: ${avg_order_value:.2f}")
ax.legend(fontsize=10)
ax.set_title("Spend Distribution (Histogram)", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Total Spend ($)")
ax.set_ylabel("Frequency")
ax.spines[["top","right"]].set_visible(False)
save("21_spend_distribution_histogram")

fig, ax = plt.subplots(figsize=(9, 4))
ax.boxplot(df["total_spend"], vert=False, patch_artist=True,
    boxprops=dict(facecolor=COLORS["light"], color=COLORS["secondary"]),
    medianprops=dict(color=COLORS["primary"], linewidth=2.5),
    whiskerprops=dict(color=COLORS["secondary"]),
    capprops=dict(color=COLORS["secondary"]),
    flierprops=dict(marker="o", markerfacecolor=COLORS["accent"], markersize=4, alpha=0.5))
ax.set_title("Spend Distribution (Boxplot)", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Total Spend ($)")
ax.spines[["top","right","left"]].set_visible(False)
ax.set_yticks([])
save("22_spend_boxplot")

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(spend_dist.index.astype(str), spend_dist.values,
              color=sns.color_palette("Blues_r", len(spend_dist)), edgecolor="white")
ax.bar_label(bars, fmt="%d", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Orders by Spend Bucket", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Number of Orders")
ax.spines[["top","right"]].set_visible(False)
save("23_spend_by_bucket")

fig, ax = plt.subplots(figsize=(7, 6))
ax.pie([repeat_customers, new_customers],
       labels=[f"Repeat\n{repeat_customers:,}", f"New\n{new_customers:,}"],
       colors=[COLORS["primary"], COLORS["accent"]],
       autopct="%1.1f%%", startangle=90,
       wedgeprops={"edgecolor":"white","linewidth":3},
       textprops={"fontsize":11})
ax.set_title("Repeat vs New Customers", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
save("24_repeat_vs_new_customers")

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_customers.index.astype(str), top_customers["total_spent"],
               color=sns.color_palette("Greens_r", 10), edgecolor="white")
ax.bar_label(bars, fmt="$%.2f", fontsize=8, padding=3, color=COLORS["text"])
ax.set_title("Top 10 Customers by Lifetime Spend", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Total Spend ($)")
ax.spines[["top","right"]].set_visible(False)
save("25_top10_customers")

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(store_ranking.index.astype(str), store_ranking["revenue"],
               color=sns.color_palette("Blues_r", 10), edgecolor="white")
ax.bar_label(bars, fmt="$%.0f", fontsize=8, padding=3, color=COLORS["text"])
ax.set_title("Top 10 Stores by Revenue", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Total Revenue ($)")
ax.spines[["top","right"]].set_visible(False)
save("26_top10_stores")

fig, ax = plt.subplots(figsize=(9, 6))
seg_colors_map = {"Bronze":"#94A3B8","Silver":"#3B82F6","Gold":"#CBA258","Platinum":"#EF4444"}
for seg_name in rfm["seg_name"].unique():
    subset = rfm[rfm["seg_name"] == seg_name]
    ax.scatter(subset["frequency"], subset["monetary"],
               alpha=0.45, s=20, color=seg_colors_map.get(seg_name, "#999"), label=seg_name)
ax.legend(title="Segment", fontsize=9)
ax.set_title("RFM Customer Segments (K-Means)", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Frequency (Orders)")
ax.set_ylabel("Monetary (Total Spend $)")
ax.spines[["top","right"]].set_visible(False)
save("27_rfm_customer_segments")

fig, ax = plt.subplots(figsize=(8, 5))
tier_counts = clv["clv_tier"].value_counts().reindex(["Low","Medium","High","VIP"])
bars = ax.bar(tier_counts.index, tier_counts.values,
              color=["#94A3B8","#3B82F6","#CBA258","#EF4444"], edgecolor="white")
ax.bar_label(bars, fmt="%d", fontsize=10, padding=3, color=COLORS["text"])
ax.set_title("Customer Lifetime Value (CLV) Tiers", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Number of Customers")
ax.spines[["top","right"]].set_visible(False)
save("28_clv_tier_distribution")

fig, ax = plt.subplots(figsize=(9, 5))
fa_sorted = drink_food_pivot["food_attach_%"].sort_values(ascending=True)
bars = ax.barh(fa_sorted.index, fa_sorted.values,
               color=sns.color_palette("RdYlGn", len(fa_sorted)), edgecolor="white")
ax.bar_label(bars, fmt="%.2f%%", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Food Attach Rate by Drink Category (%)", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Food Attach Rate (%)")
ax.spines[["top","right"]].set_visible(False)
save("29_food_attach_rate_by_drink")

fig, ax = plt.subplots(figsize=(9, 5))
ch_fulfill = df.groupby("order_channel")["fulfillment_time_min"].mean().sort_values()
bars = ax.barh(ch_fulfill.index, ch_fulfill.values,
               color=sns.color_palette("OrRd", len(ch_fulfill)), edgecolor="white")
ax.bar_label(bars, fmt="%.2f min", fontsize=9, padding=3, color=COLORS["text"])
ax.set_title("Avg Fulfillment Time by Order Channel", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Avg Fulfillment Time (min)")
ax.spines[["top","right"]].set_visible(False)
save("30_channel_fulfillment_time")

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
order_ahead_grp = df.groupby("order_ahead").agg(
    orders=("order_id","count"), avg_spend=("total_spend","mean"))
labels31 = ["Not Ordered Ahead","Ordered Ahead"]
bars1 = axes[0].bar(labels31, order_ahead_grp["orders"].values,
    color=[COLORS["muted"], COLORS["primary"]], edgecolor="white")
axes[0].bar_label(bars1, fmt="%d", fontsize=10, padding=3, color=COLORS["text"])
axes[0].set_title("Order Ahead vs Walk-in (Orders)", fontsize=11, fontweight="bold", color=COLORS["secondary"])
axes[0].spines[["top","right"]].set_visible(False)
bars2 = axes[1].bar(labels31, order_ahead_grp["avg_spend"].values,
    color=[COLORS["muted"], COLORS["primary"]], edgecolor="white")
axes[1].bar_label(bars2, fmt="$%.2f", fontsize=10, padding=3, color=COLORS["text"])
axes[1].set_title("Avg Spend: Order Ahead vs Walk-in", fontsize=11, fontweight="bold", color=COLORS["secondary"])
axes[1].spines[["top","right"]].set_visible(False)
save("31_order_ahead_analysis")

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(age_ch_piv, annot=True, fmt=".0f", cmap="Greens",
    ax=ax, linewidths=0.5, annot_kws={"size":10},
    cbar_kws={"shrink":0.7})
ax.set_title("Age Group × Order Channel Cross-tab", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_xlabel("Order Channel")
ax.set_ylabel("Age Group")
save("32_age_channel_heatmap")

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn",
    ax=ax, linewidths=0.5, annot_kws={"size":8},
    cbar_kws={"shrink":0.7})
ax.set_title("Correlation Matrix (All Numeric Features)", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.tick_params(axis="x", rotation=30, labelsize=8)
ax.tick_params(axis="y", rotation=0, labelsize=8)
save("33_correlation_heatmap")

fig, ax = plt.subplots(figsize=(9, 5))
reg_sat = region_perf["avg_satisfaction"].sort_values(ascending=False)
bars = ax.bar(reg_sat.index, reg_sat.values,
              color=sns.color_palette("Greens_r", len(reg_sat)), edgecolor="white")
ax.bar_label(bars, fmt="%.4f", fontsize=9, padding=3, color=COLORS["text"])
ax.set_ylim(3.60, 3.72)
ax.set_title("Avg Customer Satisfaction by Region", fontsize=14, fontweight="bold", color=COLORS["secondary"], pad=12)
ax.set_ylabel("Avg Satisfaction Score")
ax.spines[["top","right"]].set_visible(False)
save("34_region_satisfaction")

print()
