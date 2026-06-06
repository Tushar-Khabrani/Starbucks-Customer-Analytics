import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import warnings
import os

warnings.filterwarnings("ignore")

os.makedirs("charts", exist_ok=True)

GREEN   = "#00704A"
DARK    = "#1E3932"
GOLD    = "#CBA258"
CREAM   = "#F2F0EB"
ACCENT  = "#00A862"
LIGHT_G = "#D4E9E2"
RED     = "#C0392B"
TEXT    = "#1C1C1C"

PALETTE = [GREEN, GOLD, ACCENT, "#5BA4CF", DARK, "#E67E22"]

plt.rcParams.update({
    "font.family":           "DejaVu Sans",
    "figure.facecolor":      CREAM,
    "axes.facecolor":        "#FAFAF7",
    "axes.edgecolor":        "#CCCCCC",
    "axes.labelcolor":       TEXT,
    "xtick.color":           TEXT,
    "ytick.color":           TEXT,
    "text.color":            TEXT,
    "axes.spines.top":       False,
    "axes.spines.right":     False,
    "grid.color":            "#E0DDD8",
    "grid.linewidth":        0.6,
    "axes.grid":             True,
    "axes.grid.axis":        "y",
})

df = pd.read_csv("starbucks_customer_ordering_patterns.csv")

df["order_timestamp"] = pd.to_datetime(df["order_date"] + " " + df["order_time"])
df["hour"]  = df["order_timestamp"].dt.hour
df["month"] = df["order_timestamp"].dt.month

DAY_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
df["day_of_week"] = pd.Categorical(df["day_of_week"], categories=DAY_ORDER, ordered=True)

before = len(df)
df.drop_duplicates(subset="order_id", inplace=True)
print(f"✔ Duplicates removed : {before - len(df)}")

df["total_spend"].fillna(df["total_spend"].median(), inplace=True)
df["customer_satisfaction"].fillna(3, inplace=True)

print(f"✔ Dataset shape      : {df.shape}")
print(f"✔ Date range         : {df['order_date'].min()} → {df['order_date'].max()}")
print(f"✔ Total revenue      : ${df['total_spend'].sum():,.2f}")
print(f"✔ Unique customers   : {df['customer_id'].nunique():,}")
print(f"✔ Avg order value    : ${df['total_spend'].mean():.2f}")
print(f"✔ Avg satisfaction   : {df['customer_satisfaction'].mean():.2f} / 5")
print()

fig = plt.figure(figsize=(18, 20))
fig.suptitle("☕  Starbucks Customer Analytics — Full Report",
             fontsize=22, fontweight="bold", color=DARK, y=0.98)

gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.55, wspace=0.35)

kpis = [
    ("Total Orders",     f"{len(df):,}",            GREEN),
    ("Total Revenue",    f"${df['total_spend'].sum()/1e6:.2f}M", GOLD),
    ("Unique Customers", f"{df['customer_id'].nunique():,}",     DARK),
    ("Avg Order Value",  f"${df['total_spend'].mean():.2f}",     ACCENT),
    ("Avg Satisfaction", f"{df['customer_satisfaction'].mean():.2f} ★", "#E67E22"),
    ("Rewards Members",  f"{df['is_rewards_member'].mean()*100:.1f}%", "#5BA4CF"),
]
for i, (label, val, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i % 3]) if i < 3 else None
    if i == 3:
        ax = fig.add_subplot(gs[1, 0])
    elif i == 4:
        ax = fig.add_subplot(gs[1, 1])
    elif i == 5:
        ax = fig.add_subplot(gs[1, 2])
    ax.set_facecolor(color)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.5, 0.65, val, ha="center", va="center",
            fontsize=20, fontweight="bold", color="white", transform=ax.transAxes)
    ax.text(0.5, 0.25, label, ha="center", va="center",
            fontsize=10, color="white", alpha=0.9, transform=ax.transAxes)

ax2 = fig.add_subplot(gs[2, :2])
reg = df.groupby("region")["total_spend"].sum().sort_values(ascending=True)
bars = ax2.barh(reg.index, reg.values / 1e6, color=PALETTE[:len(reg)], edgecolor="white", linewidth=0.5)
for bar, val in zip(bars, reg.values / 1e6):
    ax2.text(val + 0.02, bar.get_y() + bar.get_height() / 2,
             f"${val:.2f}M", va="center", fontsize=9, color=TEXT)
ax2.set_xlabel("Revenue (Millions $)")
ax2.set_title("Revenue by Region", fontweight="bold", fontsize=12, pad=10)
ax2.grid(axis="x"); ax2.grid(axis="y", visible=False)

ax3 = fig.add_subplot(gs[2, 2])
drinks = df["drink_category"].value_counts()
wedges, texts, autotexts = ax3.pie(
    drinks.values, labels=None, autopct="%1.1f%%",
    colors=PALETTE[:len(drinks)], startangle=140,
    pctdistance=0.75, wedgeprops=dict(edgecolor="white", linewidth=1.5))
for at in autotexts:
    at.set_fontsize(8)
ax3.legend(drinks.index, loc="lower center", bbox_to_anchor=(0.5, -0.25),
           ncol=2, fontsize=8, frameon=False)
ax3.set_title("Drink Category Mix", fontweight="bold", fontsize=12, pad=10)

ax4 = fig.add_subplot(gs[3, :])
hourly = df.groupby("hour").size()
colors_h = [RED if v == hourly.max() else (GOLD if v >= hourly.quantile(0.75) else GREEN)
            for v in hourly.values]
ax4.bar(hourly.index, hourly.values, color=colors_h, edgecolor="white", linewidth=0.5)
ax4.set_xlabel("Hour of Day (24h)")
ax4.set_ylabel("Number of Orders")
ax4.set_title("Order Volume by Hour  (🔴 Peak  🟡 High  🟢 Normal)",
              fontweight="bold", fontsize=12, pad=10)
ax4.set_xticks(range(0, 24))

plt.savefig("charts/01_executive_dashboard.png", dpi=150, bbox_inches="tight")
plt.close()

fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle("☕  Customer Behaviour Analysis", fontsize=18,
             fontweight="bold", color=DARK, y=1.01)
fig.patch.set_facecolor(CREAM)

ax = axes[0, 0]
rwd = df.groupby("is_rewards_member")["total_spend"].mean()
rwd_vals = [rwd.iloc[0], rwd.iloc[1]]  
bars = ax.bar(["Non-Rewards", "Rewards"], rwd_vals,
              color=["#AAAAAA", GREEN], edgecolor="white", width=0.5)
for bar, val in zip(bars, [rwd[False], rwd[True]]):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.05,
            f"${val:.2f}", ha="center", fontsize=11, fontweight="bold")
ax.set_title("Avg Spend: Rewards vs Non-Rewards", fontweight="bold")
ax.set_ylabel("Avg Order Value ($)")

ax = axes[0, 1]
chan = df["order_channel"].value_counts()
ax.bar(chan.index, chan.values, color=PALETTE[:len(chan)], edgecolor="white")
ax.set_title("Orders by Channel", fontweight="bold")
ax.set_ylabel("Number of Orders")
ax.tick_params(axis="x", rotation=20)
for i, (bar_x, val) in enumerate(zip(chan.index, chan.values)):
    ax.text(i, val + 200, f"{val:,}", ha="center", fontsize=9)

ax = axes[0, 2]
sat = df.groupby("drink_category")["customer_satisfaction"].mean().sort_values(ascending=True)
colors_s = [GREEN if v >= sat.mean() else GOLD for v in sat.values]
ax.barh(sat.index, sat.values, color=colors_s, edgecolor="white")
ax.axvline(sat.mean(), color=RED, linestyle="--", linewidth=1.2, label=f"Mean: {sat.mean():.2f}")
ax.set_title("Avg Satisfaction by Drink", fontweight="bold")
ax.set_xlabel("Satisfaction Score (1–5)")
ax.legend(fontsize=8)
for i, val in enumerate(sat.values):
    ax.text(val + 0.005, i, f"{val:.2f}", va="center", fontsize=9)

ax = axes[1, 0]
age_order = ["18-24", "25-34", "35-44", "45-54", "55+"]
age = df.groupby("customer_age_group").agg(
    orders=("order_id", "count"),
    avg_spend=("total_spend", "mean")
).reindex(age_order)
x = np.arange(len(age))
width = 0.4
b1 = ax.bar(x - width/2, age["orders"] / 1000, width, color=GREEN, label="Orders (K)", edgecolor="white")
ax2_twin = ax.twinx()
b2 = ax2_twin.plot(x, age["avg_spend"], "o-", color=GOLD, linewidth=2,
                   markersize=7, label="Avg Spend ($)")
ax.set_xticks(x); ax.set_xticklabels(age_order)
ax.set_ylabel("Orders (Thousands)", color=GREEN)
ax2_twin.set_ylabel("Avg Spend ($)", color=GOLD)
ax.set_title("Age Group: Orders & Avg Spend", fontweight="bold")
ax.grid(axis="y"); ax2_twin.grid(visible=False)
lines = [mpatches.Patch(color=GREEN, label="Orders (K)"),
         plt.Line2D([0], [0], color=GOLD, marker="o", label="Avg Spend ($)")]
ax.legend(handles=lines, fontsize=8, loc="upper right")

ax = axes[1, 1]
ax.hist(df["fulfillment_time_min"], bins=40, color=ACCENT, edgecolor="white", alpha=0.85)
ax.axvline(df["fulfillment_time_min"].mean(), color=RED, linestyle="--",
           linewidth=1.5, label=f"Mean: {df['fulfillment_time_min'].mean():.1f} min")
ax.axvline(df["fulfillment_time_min"].median(), color=GOLD, linestyle="--",
           linewidth=1.5, label=f"Median: {df['fulfillment_time_min'].median():.1f} min")
ax.set_title("Fulfillment Time Distribution", fontweight="bold")
ax.set_xlabel("Minutes")
ax.set_ylabel("Frequency")
ax.legend(fontsize=9)

ax = axes[1, 2]
oa = df.groupby("order_ahead").agg(
    avg_fulfillment=("fulfillment_time_min", "mean"),
    avg_satisfaction=("customer_satisfaction", "mean")
).rename(index={True: "Order Ahead", False: "Walk-in"})
x = np.arange(2)
b1 = ax.bar(x - 0.2, oa["avg_fulfillment"], 0.35, color=GREEN, label="Avg Fulfillment (min)", edgecolor="white")
ax_r = ax.twinx()
b2 = ax_r.bar(x + 0.2, oa["avg_satisfaction"], 0.35, color=GOLD, label="Avg Satisfaction", edgecolor="white")
ax.set_xticks(x); ax.set_xticklabels(["Walk-in", "Order Ahead"])
ax.set_ylabel("Fulfillment Time (min)", color=GREEN)
ax_r.set_ylabel("Satisfaction Score", color=GOLD)
ax.set_title("Order Ahead vs Walk-in", fontweight="bold")
ax_r.set_ylim(0, 6)
ax.grid(axis="y"); ax_r.grid(visible=False)
lines = [mpatches.Patch(color=GREEN, label="Fulfillment (min)"),
         mpatches.Patch(color=GOLD, label="Satisfaction")]
ax.legend(handles=lines, fontsize=8)

plt.tight_layout()
plt.savefig("charts/02_customer_behaviour.png", dpi=150, bbox_inches="tight")
plt.close()

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("☕  Time & Location Patterns", fontsize=18,
             fontweight="bold", color=DARK)
fig.patch.set_facecolor(CREAM)

ax = axes[0, 0]
pivot = df.pivot_table(values="total_spend", index="day_of_week",
                       columns="hour", aggfunc="mean")
sns.heatmap(pivot, ax=ax, cmap="YlGn", linewidths=0.3,
            cbar_kws={"label": "Avg Spend ($)"}, fmt=".0f", annot=False)
ax.set_title("Avg Spend Heatmap: Day × Hour", fontweight="bold")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Day of Week")

ax = axes[0, 1]
day_orders = df.groupby("day_of_week", observed=True).size()
colors_d = [GREEN if v == day_orders.max() else LIGHT_G for v in day_orders.values]
bars = ax.bar(day_orders.index, day_orders.values, color=colors_d, edgecolor=GREEN, linewidth=0.8)
ax.set_title("Orders by Day of Week", fontweight="bold")
ax.set_ylabel("Orders")
for bar, val in zip(bars, day_orders.values):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 100,
            f"{val:,}", ha="center", fontsize=8)

ax = axes[1, 0]
loc = df.groupby("store_location_type").agg(
    orders=("order_id", "count"),
    revenue=("total_spend", "sum")
).sort_values("revenue", ascending=True)
bars = ax.barh(loc.index, loc["revenue"] / 1e6, color=[GREEN, GOLD, ACCENT], edgecolor="white")
for bar, val in zip(bars, loc["revenue"] / 1e6):
    ax.text(val + 0.01, bar.get_y() + bar.get_height() / 2,
            f"${val:.2f}M", va="center", fontsize=10, fontweight="bold")
ax.set_title("Revenue by Store Location Type", fontweight="bold")
ax.set_xlabel("Revenue (Millions $)")
ax.grid(axis="x"); ax.grid(axis="y", visible=False)

ax = axes[1, 1]
cart = df["cart_size"].value_counts().sort_index()
ax.bar(cart.index, cart.values, color=PALETTE[:len(cart)], edgecolor="white", width=0.7)
avg_cart = df["cart_size"].mean()
ax.axvline(avg_cart, color=RED, linestyle="--",
           linewidth=1.5, label=f"Avg: {avg_cart:.1f} items")
ax.set_title("Cart Size Distribution", fontweight="bold")
ax.set_xlabel("Number of Items in Cart")
ax.set_ylabel("Orders")
ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig("charts/03_time_location_patterns.png", dpi=150, bbox_inches="tight")
plt.close()

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("☕  Regional & Demographic Breakdown", fontsize=18,
             fontweight="bold", color=DARK)
fig.patch.set_facecolor(CREAM)

ax = axes[0]
reg_drink = df.groupby(["region", "drink_category"]).size().unstack(fill_value=0)
reg_drink_pct = reg_drink.div(reg_drink.sum(axis=1), axis=0) * 100
reg_drink_pct.plot(kind="bar", ax=ax, stacked=True, color=PALETTE[:6],
                   edgecolor="white", linewidth=0.4, legend=True)
ax.set_title("Drink Mix by Region (%)", fontweight="bold")
ax.set_ylabel("Share (%)")
ax.tick_params(axis="x", rotation=25)
ax.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1.0, 1.0))
ax.grid(axis="y"); ax.grid(axis="x", visible=False)

ax = axes[1]
cust_sat = df.groupby("num_customizations").agg(
    avg_sat=("customer_satisfaction", "mean"),
    count=("order_id", "count")
).reset_index()
sc = ax.scatter(cust_sat["num_customizations"], cust_sat["avg_sat"],
                s=cust_sat["count"] / 100, c=cust_sat["avg_sat"],
                cmap="RdYlGn", vmin=1, vmax=5, edgecolors=DARK, linewidth=0.5, alpha=0.85)
plt.colorbar(sc, ax=ax, label="Satisfaction")
ax.set_title("Customizations vs Satisfaction\n(bubble = order volume)", fontweight="bold")
ax.set_xlabel("Number of Customizations")
ax.set_ylabel("Avg Satisfaction Score")

ax = axes[2]
gend = df.groupby(["customer_gender", "is_rewards_member"])["total_spend"].mean().unstack()
gend.columns = ["Non-Rewards", "Rewards"]
gend.plot(kind="bar", ax=ax, color=[GOLD, GREEN], edgecolor="white", width=0.55)
ax.set_title("Avg Spend by Gender & Rewards Status", fontweight="bold")
ax.set_ylabel("Avg Spend ($)")
ax.tick_params(axis="x", rotation=0)
ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig("charts/04_regional_demographic.png", dpi=150, bbox_inches="tight")
plt.close()

print()
print("=" * 60)
print("  KEY BUSINESS INSIGHTS")
print("=" * 60)

top_region = df.groupby("region")["total_spend"].sum().idxmax()
top_drink  = df["drink_category"].value_counts().idxmax()
peak_hour  = df.groupby("hour").size().idxmax()
peak_day   = df.groupby("day_of_week", observed=True).size().idxmax()
rwd_lift   = (df[df["is_rewards_member"] == True]["total_spend"].mean() /
              df[df["is_rewards_member"] == False]["total_spend"].mean() - 1) * 100

print(f"  🏆 Top Revenue Region   : {top_region}")
print(f"  ☕ Most Ordered Drink   : {top_drink}")
print(f"  🕐 Peak Order Hour      : {peak_hour}:00")
print(f"  📅 Busiest Day          : {peak_day}")
print(f"  💳 Rewards Spend Lift   : +{rwd_lift:.1f}% vs non-members")
print(f"  ⚡ Avg Fulfillment Time : {df['fulfillment_time_min'].mean():.1f} min")
print(f"  🛒 Most Common Cart Size: {df['cart_size'].mode()[0]} items")
print("=" * 60)
print()
