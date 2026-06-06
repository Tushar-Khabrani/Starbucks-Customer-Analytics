import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import warnings
warnings.filterwarnings("ignore")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tush@rK104",
    database="star_bucks"
)

orders_overview  = pd.read_sql("SELECT * FROM orders_overview",          connection)
customer_insights= pd.read_sql("SELECT * FROM customer_insights",        connection)
peak_time        = pd.read_sql("SELECT * FROM peak_order_time",          connection)
drink_perf       = pd.read_sql("SELECT * FROM drink_performance",        connection)
region_rev       = pd.read_sql("SELECT * FROM revenue_region_analysis",  connection)
store_perf       = pd.read_sql("SELECT * FROM store_performance",        connection)

connection.close()

PALETTE = ["#00704A","#CBA258","#1E3932","#D4E9E2","#6F4E37","#C8A97E"]
sns.set_style("whitegrid")
sns.set_palette(PALETTE)
plt.rcParams.update({
    "figure.dpi"       : 120,
    "axes.titlesize"   : 13,
    "axes.titleweight" : "bold",
    "axes.labelsize"   : 10,
    "xtick.labelsize"  : 9,
    "ytick.labelsize"  : 9,
})

def is_true(val):
    return str(val).strip().lower() in ('true', '1', 'yes')

row = orders_overview.iloc[0]

print("\n" + "="*50)
print("         STARBUCKS — BUSINESS OVERVIEW")
print("="*50)
print(f"  Total Orders           : {int(row['total_orders']):,}")
print(f"  Unique Customers       : {int(row['unique_customers']):,}")
print(f"  Total Revenue          : ${row['total_revenue']:,.2f}")
print(f"  Avg Order Value        : ${row['avg_order_value']:.2f}")
print(f"  Avg Cart Size          : {row['avg_cart_size']:.2f} items")
print(f"  Avg Fulfillment Time   : {row['avg_fulfillment_time']:.2f} min")
print(f"  Avg Customizations     : {row['avg_customizations']:.2f}")
print(f"  Avg Satisfaction Score : {row['avg_satisfaction_score']:.2f} / 5")
print(f"  Food Item Orders       : {int(row['food_item_orders']):,}  ({row['food_item_pct']}%)")
print(f"  Order Ahead Orders     : {int(row['order_ahead_orders']):,}  ({row['order_ahead_pct']}%)")
print(f"  Rewards Member Orders  : {int(row['rewards_member_orders']):,}  ({row['rewards_member_pct']}%)")
print(f"  Total Stores           : {int(row['total_stores'])}")
print(f"  Total Regions          : {int(row['total_regions'])}")
print(f"  Customer Lifetime Value: ${row['customer_lifetime_value']:.2f}")

print("\n" + "="*50)
print("         TOP DRINK ANALYSIS")
print("="*50)
top_drink = drink_perf.sort_values("total_orders", ascending=False).iloc[0]
low_drink  = drink_perf.sort_values("total_orders").iloc[0]
most_rev   = drink_perf.sort_values("total_revenue", ascending=False).iloc[0]
most_cust  = drink_perf.sort_values("avg_customizations", ascending=False).iloc[0]
for _, r in drink_perf.iterrows():
    print(f"  {r['drink_category']:<18} | Orders: {int(r['total_orders']):>6,} | "
          f"Revenue: ${r['total_revenue']:>10,.2f} | Avg: ${r['avg_order_value']:.2f} | "
          f"Food Combo: {r['food_combo_pct']}% | Order Ahead: {r['order_ahead_pct']}% | "
          f"Satisfaction: {r['avg_satisfaction']:.2f}")
print(f"\n  Most Popular   : {top_drink['drink_category']} ({int(top_drink['total_orders']):,} orders)")
print(f"  Highest Revenue: {most_rev['drink_category']} (${most_rev['total_revenue']:,.2f})")
print(f"  Most Customized: {most_cust['drink_category']} ({most_cust['avg_customizations']:.2f} avg)")
print(f"  Least Popular  : {low_drink['drink_category']} ({int(low_drink['total_orders']):,} orders)")

print("\n" + "="*50)
print("         PEAK ORDER TIME ANALYSIS")
print("="*50)
hour_agg = peak_time.groupby("order_hour").agg(
    total_orders=("total_orders","sum"),
    hourly_revenue=("hourly_revenue","sum")
).reset_index()
peak_row = hour_agg.sort_values("total_orders", ascending=False).iloc[0]
low_row  = hour_agg.sort_values("total_orders").iloc[0]
day_agg  = peak_time.groupby("day_of_week")["total_orders"].sum().reset_index()
peak_day = day_agg.sort_values("total_orders", ascending=False).iloc[0]
chan_agg = peak_time.groupby("order_channel")["total_orders"].sum().reset_index()
top_chan = chan_agg.sort_values("total_orders", ascending=False).iloc[0]
print(f"  Peak Hour   : {int(peak_row['order_hour'])}:00  ({int(peak_row['total_orders']):,} orders)")
print(f"  Slowest Hour: {int(low_row['order_hour'])}:00  ({int(low_row['total_orders']):,} orders)")
print(f"  Peak Day    : {peak_day['day_of_week']}  ({int(peak_day['total_orders']):,} orders)")
print(f"  Top Channel : {top_chan['order_channel']}  ({int(top_chan['total_orders']):,} orders)")
print(f"\n  Orders by Day:")
for _, r in day_agg.sort_values("total_orders", ascending=False).iterrows():
    print(f"    {r['day_of_week']:<4} : {int(r['total_orders']):,}")

print("\n" + "="*50)
print("         REGION PERFORMANCE")
print("="*50)
reg_agg = region_rev.groupby("region").agg(
    total_orders=("total_orders","sum"),
    total_revenue=("total_revenue","sum"),
    avg_satisfaction=("avg_satisfaction","mean"),
    avg_fulfillment=("avg_fulfillment_time","mean")
).reset_index().sort_values("total_revenue", ascending=False)
for _, r in reg_agg.iterrows():
    print(f"  {r['region']:<12} | Revenue: ${r['total_revenue']:>12,.2f} | "
          f"Orders: {int(r['total_orders']):>6,} | Satisfaction: {r['avg_satisfaction']:.2f} | "
          f"Fulfillment: {r['avg_fulfillment']:.2f} min")

order_ahead_impact = region_rev.groupby("order_ahead")[["avg_fulfillment_time","avg_satisfaction"]].mean()
print(f"\n  Order Ahead Impact:")
for oa, row_oa in order_ahead_impact.iterrows():
    label = "Order Ahead" if is_true(oa) else "Regular Order"
    print(f"    {label:<15} → Fulfillment: {row_oa['avg_fulfillment_time']:.2f} min | "
          f"Satisfaction: {row_oa['avg_satisfaction']:.2f}")

print("\n" + "="*50)
print("         REWARDS MEMBER BEHAVIOUR")
print("="*50)
rwd = customer_insights.groupby("is_rewards_member").agg(
    total_orders=("total_orders","sum"),
    avg_spend=("avg_spend_per_order","mean"),
    avg_satisfaction=("avg_satisfaction","mean"),
    avg_cart=("avg_cart_size","mean"),
    avg_customizations=("avg_customizations","mean")
).reset_index()
for _, r in rwd.iterrows():
    label = "Rewards Member" if is_true(r["is_rewards_member"]) else "Non-Member    "
    print(f"  {label} | Avg Spend: ${r['avg_spend']:.2f} | "
          f"Avg Cart: {r['avg_cart']:.2f} | Satisfaction: {r['avg_satisfaction']:.2f} | "
          f"Customizations: {r['avg_customizations']:.2f}")
if len(rwd) == 2:
    mem_spend = rwd[rwd["is_rewards_member"].apply(is_true)]["avg_spend"].values[0]
    non_spend = rwd[~rwd["is_rewards_member"].apply(is_true)]["avg_spend"].values[0]
    diff = mem_spend - non_spend
    print(f"\n  Rewards members spend ${abs(diff):.2f} {'more' if diff > 0 else 'less'} per order than non-members")

print("\n" + "="*50)
print("         STORE PERFORMANCE")
print("="*50)
best_rev  = store_perf.sort_values("total_revenue",     ascending=False).iloc[0]
best_sat  = store_perf.sort_values("avg_satisfaction",  ascending=False).iloc[0]
worst_sat = store_perf.sort_values("avg_satisfaction").iloc[0]
fastest   = store_perf.sort_values("avg_fulfillment_time").iloc[0]
print(f"  Top Revenue Store    : {best_rev['store_id']}  (${best_rev['total_revenue']:,.2f}, Region: {best_rev['region']})")
print(f"  Highest Satisfaction : {best_sat['store_id']}  (Score: {best_sat['avg_satisfaction']:.2f})")
print(f"  Lowest Satisfaction  : {worst_sat['store_id']}  (Score: {worst_sat['avg_satisfaction']:.2f})")
print(f"  Fastest Fulfillment  : {fastest['store_id']}  ({fastest['avg_fulfillment_time']:.2f} min)")
loc_agg = store_perf.groupby("store_location_type").agg(
    total_revenue=("total_revenue","sum"),
    avg_satisfaction=("avg_satisfaction","mean"),
    total_orders=("total_orders","sum")
).reset_index().sort_values("total_revenue", ascending=False)
print(f"\n  Performance by Location Type:")
for _, r in loc_agg.iterrows():
    print(f"    {r['store_location_type']:<10} | Revenue: ${r['total_revenue']:>12,.2f} | "
          f"Orders: {int(r['total_orders']):>6,} | Satisfaction: {r['avg_satisfaction']:.2f}")

print("\n" + "="*50)
print("         CUSTOMER SATISFACTION ANALYSIS")
print("="*50)
overall_sat = store_perf["avg_satisfaction"].mean()
print(f"  Overall Avg Satisfaction : {overall_sat:.2f} / 5.0")
reg_sat = region_rev.groupby("region")["avg_satisfaction"].mean().sort_values(ascending=False)
print(f"\n  Satisfaction by Region:")
for region, score in reg_sat.items():
    print(f"    {region:<12} : {score:.2f}")

print("\n" + "="*50)
print("         ANALYSIS COMPLETE — GENERATING CHARTS")
print("="*50 + "\n")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Drink Performance", fontsize=14, fontweight="bold")
drink_sorted = drink_perf.sort_values("total_orders", ascending=False)
sns.barplot(ax=axes[0], x="drink_category", y="total_orders",  data=drink_sorted, palette=PALETTE)
axes[0].set_title("Orders by Drink Category")
axes[0].set_xlabel("")
axes[0].tick_params(axis="x", rotation=30)
for bar in axes[0].patches:
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+100,
                 f"{int(bar.get_height()):,}", ha="center", fontsize=8)
sns.barplot(ax=axes[1], x="drink_category", y="total_revenue", data=drink_sorted, palette=PALETTE)
axes[1].set_title("Revenue by Drink Category")
axes[1].set_xlabel("")
axes[1].tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig("chart_01_drink_performance.png", bbox_inches="tight")
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Drink Deep-Dive: Food Combo & Order Ahead", fontsize=14, fontweight="bold")
sns.barplot(ax=axes[0], x="drink_category", y="food_combo_pct",
            data=drink_perf.sort_values("food_combo_pct", ascending=False), palette=PALETTE)
axes[0].set_title("Food Combo % by Drink Category")
axes[0].set_xlabel("")
axes[0].tick_params(axis="x", rotation=30)
axes[0].set_ylabel("Food Combo %")
for bar in axes[0].patches:
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
                 f"{bar.get_height():.1f}%", ha="center", fontsize=8)
sns.barplot(ax=axes[1], x="drink_category", y="order_ahead_pct",
            data=drink_perf.sort_values("order_ahead_pct", ascending=False), palette=PALETTE)
axes[1].set_title("Order Ahead % by Drink Category")
axes[1].set_xlabel("")
axes[1].tick_params(axis="x", rotation=30)
axes[1].set_ylabel("Order Ahead %")
for bar in axes[1].patches:
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
                 f"{bar.get_height():.1f}%", ha="center", fontsize=8)
plt.tight_layout()
plt.savefig("chart_02_drink_deepdive.png", bbox_inches="tight")
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Peak Time Analysis", fontsize=14, fontweight="bold")
h_agg = peak_time.groupby("order_hour").agg(
    total_orders=("total_orders","sum")
).reset_index()
sns.barplot(ax=axes[0], x="order_hour", y="total_orders", data=h_agg, color=PALETTE[0])
axes[0].set_title("Orders by Hour")
axes[0].set_xlabel("Hour of Day")
d_order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
d_agg   = peak_time.groupby("day_of_week")["total_orders"].sum().reindex(d_order).reset_index()
sns.barplot(ax=axes[1], x="day_of_week", y="total_orders", data=d_agg, palette=PALETTE)
axes[1].set_title("Orders by Day of Week")
axes[1].set_xlabel("")
plt.tight_layout()
plt.savefig("chart_03_peak_time.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(14, 5))
pivot = peak_time.groupby(["day_of_week","order_hour"])["total_orders"].sum().unstack(fill_value=0)
pivot = pivot.reindex(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
sns.heatmap(pivot, cmap="YlGn", ax=ax, linewidths=0.3, annot=False)
ax.set_title("Orders Heatmap — Day × Hour", fontsize=13, fontweight="bold")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Day of Week")
plt.tight_layout()
plt.savefig("chart_04_heatmap.png", bbox_inches="tight")
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Region Performance", fontsize=14, fontweight="bold")
r_agg = region_rev.groupby("region").agg(
    total_revenue=("total_revenue","sum"),
    avg_satisfaction=("avg_satisfaction","mean")
).reset_index().sort_values("total_revenue", ascending=False)
sns.barplot(ax=axes[0], x="region", y="total_revenue",    data=r_agg, palette=PALETTE)
axes[0].set_title("Revenue by Region")
axes[0].tick_params(axis="x", rotation=20)
sns.barplot(ax=axes[1], x="region", y="avg_satisfaction", data=r_agg, palette=PALETTE)
axes[1].set_title("Avg Satisfaction by Region")
axes[1].set_ylim(0, 5)
axes[1].tick_params(axis="x", rotation=20)
plt.tight_layout()
plt.savefig("chart_05_region.png", bbox_inches="tight")
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Order Ahead Impact", fontsize=14, fontweight="bold")
oa = region_rev.groupby("order_ahead").agg(
    avg_fulfillment=("avg_fulfillment_time","mean"),
    avg_satisfaction=("avg_satisfaction","mean")
).reset_index()
oa["label"] = oa["order_ahead"].apply(lambda x: "Order Ahead" if is_true(x) else "Regular")
sns.barplot(ax=axes[0], x="label", y="avg_fulfillment",  data=oa, palette=[PALETTE[2],PALETTE[0]])
axes[0].set_title("Avg Fulfillment Time")
axes[0].set_xlabel("")
sns.barplot(ax=axes[1], x="label", y="avg_satisfaction", data=oa, palette=[PALETTE[2],PALETTE[0]])
axes[1].set_title("Avg Satisfaction Score")
axes[1].set_xlabel("")
axes[1].set_ylim(0, 5)
plt.tight_layout()
plt.savefig("chart_06_order_ahead.png", bbox_inches="tight")
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Rewards Member Behaviour", fontsize=14, fontweight="bold")
rwd_grp = customer_insights.groupby("is_rewards_member").agg(
    avg_spend=("avg_spend_per_order","mean"),
    avg_cart=("avg_cart_size","mean"),
    avg_sat=("avg_satisfaction","mean")
).reset_index()
rwd_grp["label"] = rwd_grp["is_rewards_member"].apply(lambda x: "Member" if is_true(x) else "Non-Member")
for ax, col, title in zip(axes,
                           ["avg_spend","avg_cart","avg_sat"],
                           ["Avg Spend per Order","Avg Cart Size","Avg Satisfaction"]):
    sns.barplot(ax=ax, x="label", y=col, data=rwd_grp, palette=[PALETTE[2],PALETTE[0]])
    ax.set_title(title)
    ax.set_xlabel("")
plt.tight_layout()
plt.savefig("chart_07_rewards.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(14, 5))
top10 = store_perf.sort_values("total_revenue", ascending=False).head(10)
sns.barplot(ax=ax, x="store_id", y="total_revenue", data=top10,
            hue="region", palette=PALETTE, legend=True)
ax.set_title("Top 10 Revenue Generating Stores", fontsize=13, fontweight="bold")
ax.tick_params(axis="x", rotation=30)
ax.set_xlabel("")
plt.tight_layout()
plt.savefig("chart_08_top_stores.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
region_colors = {r: PALETTE[i] for i, r in enumerate(store_perf["region"].unique())}
for region, grp in store_perf.groupby("region"):
    ax.scatter(grp["avg_satisfaction"], grp["total_revenue"],
               label=region, alpha=0.6, s=40, color=region_colors[region])
ax.set_title("Store: Revenue vs Satisfaction", fontsize=13, fontweight="bold")
ax.set_xlabel("Avg Satisfaction Score")
ax.set_ylabel("Total Revenue ($)")
ax.legend(title="Region")
plt.tight_layout()
plt.savefig("chart_09_rev_vs_sat.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(9, 5))
sns.regplot(ax=ax, x="avg_fulfillment_time", y="avg_satisfaction",
            data=store_perf, scatter_kws={"alpha":0.4,"color":PALETTE[0]},
            line_kws={"color":PALETTE[2]})
ax.set_title("Fulfillment Time vs Customer Satisfaction", fontsize=13, fontweight="bold")
ax.set_xlabel("Avg Fulfillment Time (min)")
ax.set_ylabel("Avg Satisfaction Score")
plt.tight_layout()
plt.savefig("chart_10_fulfillment_sat.png", bbox_inches="tight")
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Customer Demographics", fontsize=14, fontweight="bold")
age_grp = customer_insights.groupby("customer_age_group").agg(
    avg_spend=("avg_spend_per_order","mean"),
    total_orders=("total_orders","sum")
).reset_index().sort_values("total_orders", ascending=False)
sns.barplot(ax=axes[0], x="customer_age_group", y="total_orders", data=age_grp, palette=PALETTE)
axes[0].set_title("Orders by Age Group")
axes[0].set_xlabel("")
gen_grp = customer_insights.groupby("customer_gender").agg(
    avg_spend=("avg_spend_per_order","mean"),
    total_orders=("total_orders","sum")
).reset_index()
sns.barplot(ax=axes[1], x="customer_gender", y="avg_spend", data=gen_grp, palette=PALETTE[:3])
axes[1].set_title("Avg Spend by Gender")
axes[1].set_xlabel("")
plt.tight_layout()
plt.savefig("chart_11_demographics.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(12, 5))
h_rev = peak_time.groupby("order_hour")["hourly_revenue"].sum().reset_index()
sns.barplot(ax=ax, x="order_hour", y="hourly_revenue", data=h_rev, color=PALETTE[1])
ax.set_title("Revenue Generated by Hour", fontsize=13, fontweight="bold")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("chart_12_revenue_by_hour.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(8, 5))
ch_agg = peak_time.groupby("order_channel")["total_orders"].sum().reset_index()
ax.pie(ch_agg["total_orders"], labels=ch_agg["order_channel"],
       autopct="%1.1f%%", colors=PALETTE, startangle=140,
       wedgeprops={"edgecolor":"white","linewidth":1.5})
ax.set_title("Order Channel Distribution", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("chart_13_channels.png", bbox_inches="tight")
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle("Store Location Type Analysis", fontsize=14, fontweight="bold")
loc_grp = store_perf.groupby("store_location_type").agg(
    total_revenue=("total_revenue","sum"),
    avg_satisfaction=("avg_satisfaction","mean"),
    avg_fulfillment=("avg_fulfillment_time","mean")
).reset_index()
for ax, col, title in zip(axes,
    ["total_revenue","avg_satisfaction","avg_fulfillment"],
    ["Total Revenue","Avg Satisfaction","Avg Fulfillment (min)"]):
    sns.barplot(ax=ax, x="store_location_type", y=col, data=loc_grp, palette=PALETTE[:3])
    ax.set_title(title)
    ax.set_xlabel("")
plt.tight_layout()
plt.savefig("chart_14_location_type.png", bbox_inches="tight")
plt.show()

fig = plt.figure(figsize=(14, 6))
fig.patch.set_facecolor("#1E3932")
kpis = [
    ("Total Orders",        f"{int(row['total_orders']):,}"),
    ("Total Revenue",       f"${row['total_revenue']:,.0f}"),
    ("Unique Customers",    f"{int(row['unique_customers']):,}"),
    ("Avg Order Value",     f"${row['avg_order_value']:.2f}"),
    ("Avg Satisfaction",    f"{row['avg_satisfaction_score']:.2f}/5"),
    ("Rewards Member %",    f"{row['rewards_member_pct']}%"),
    ("Order Ahead %",       f"{row['order_ahead_pct']}%"),
    ("Food Item %",         f"{row['food_item_pct']}%"),
    ("Customer LTV",        f"${row['customer_lifetime_value']:.2f}"),
    ("Avg Fulfillment",     f"{row['avg_fulfillment_time']:.2f} min"),
]
for idx, (label, value) in enumerate(kpis):
    ax = fig.add_subplot(2, 5, idx + 1)
    ax.set_facecolor("#00704A")
    ax.text(0.5, 0.6, value, ha="center", va="center", fontsize=16,
            fontweight="bold", color="white", transform=ax.transAxes)
    ax.text(0.5, 0.2, label, ha="center", va="center", fontsize=8,
            color="#D4E9E2", transform=ax.transAxes)
    ax.axis("off")
fig.suptitle("STARBUCKS ANALYTICS — KPI DASHBOARD", fontsize=14,
             fontweight="bold", color="white", y=1.01)
plt.tight_layout()
plt.savefig("chart_15_kpi_dashboard.png", bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()

print("\n All 15 charts saved as PNG files in current directory.")
print(" Full analysis complete.\n")