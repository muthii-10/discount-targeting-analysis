"""
Discount Strategy & Customer Engagement Dashboard
Customer Segmentation & Personalization Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Discount Strategy Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 18px 20px;
        border-left: 5px solid;
        margin-bottom: 10px;
    }
    .metric-value { font-size: 2rem; font-weight: 700; margin: 0; }
    .metric-label { font-size: 0.85rem; color: #666; margin: 0; }
    .insight-box {
        background: #fff8e1;
        border-left: 4px solid #f4a261;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 10px 0;
        font-size: 0.9rem;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #264653;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 6px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ── Data loading & feature engineering ───────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/customer_data_clean.csv")
    binary_map = {"Yes": 1, "No": 0}
    df["discount_flag"] = df["discount_applied"].map(binary_map)
    df["subscription_flag"] = df["subscription_status"].map(binary_map)
    freq_map = {"Weekly": 5, "Fortnightly": 4, "Monthly": 3, "Quarterly": 2, "Annually": 1}
    df["purchase_frequency_score"] = df["frequency_of_purchases"].map(freq_map)
    df["loyalty_score"] = round(np.log(df["previous_purchases"] + 1), 4)
    def loyalty_tier(x):
        if x <= 5: return "New"
        elif x <= 15: return "Returning"
        else: return "Loyal"
    df["loyalty_tier"] = df["previous_purchases"].apply(loyalty_tier)
    df["value_tier"] = pd.qcut(df["purchase_amount_usd"], q=3, labels=["Low", "Medium", "High"])
    df["customer_value_score"] = round(df["purchase_amount_usd"] * (1 + df["loyalty_score"]), 2)
    def review_sentiment(x):
        if x < 3: return "Low"
        elif x < 4: return "Neutral"
        else: return "High"
    df["review_sentiment"] = df["review_rating"].apply(review_sentiment)
    df["high_value_low_satisfaction_flag"] = np.where(
        (df["value_tier"] == "High") & (df["review_sentiment"] == "Low"), 1, 0
    )
    return df

df = load_data()

TIER_ORDER = ["New", "Returning", "Loyal"]
TIER_COLORS = {"New": "#4C9BE8", "Returning": "#F4A261", "Loyal": "#2A9D8F"}
VALUE_COLORS = {"Low": "#E9C46A", "Medium": "#F4A261", "High": "#2A9D8F"}

sns.set_theme(style="whitegrid", font_scale=1.0)
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filters")
st.sidebar.markdown("Segment the customer base to explore discount dynamics.")

selected_tiers = st.sidebar.multiselect(
    "Loyalty Tier", TIER_ORDER, default=TIER_ORDER
)
selected_value = st.sidebar.multiselect(
    "Value Tier", ["Low", "Medium", "High"], default=["Low", "Medium", "High"]
)
selected_cats = st.sidebar.multiselect(
    "Product Category", df["category"].unique().tolist(), default=df["category"].unique().tolist()
)
selected_sub = st.sidebar.radio(
    "Subscription Status", ["All", "Subscribers Only", "Non-Subscribers Only"], index=0
)

# Apply filters
fdf = df[
    df["loyalty_tier"].isin(selected_tiers) &
    df["value_tier"].isin(selected_value) &
    df["category"].isin(selected_cats)
].copy()
if selected_sub == "Subscribers Only":
    fdf = fdf[fdf["subscription_status"] == "Yes"]
elif selected_sub == "Non-Subscribers Only":
    fdf = fdf[fdf["subscription_status"] == "No"]

if fdf.empty:
    st.warning("No customers match the selected filters. Please adjust the sidebar.")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📊 Discount Strategy & Customer Engagement Dashboard")
st.markdown(
    "**Business question:** Is the company's blanket discounting strategy driving revenue and retention — "
    "or eroding margins without meaningful return?"
)
st.caption(f"Showing **{len(fdf):,}** of {len(df):,} customers based on current filters.")
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📌 Key Metrics</div>', unsafe_allow_html=True)

total_customers = len(fdf)
total_clv = fdf["customer_value_score"].sum()
avg_discount_rate = fdf["discount_flag"].mean()
avg_clv_per_customer = fdf["customer_value_score"].mean()

# Retention rate proxy: % of customers who are Loyal or Returning
retention_rate = fdf[fdf["loyalty_tier"].isin(["Loyal", "Returning"])].shape[0] / total_customers

col1, col2, col3, col4, col5 = st.columns(5)

def kpi(col, value, label, color, delta=None):
    with col:
        st.markdown(f"""
        <div class="metric-card" style="border-color:{color}">
            <p class="metric-value" style="color:{color}">{value}</p>
            <p class="metric-label">{label}</p>
        </div>
        """, unsafe_allow_html=True)

kpi(col1, f"{total_customers:,}", "Total Customers", "#4C9BE8")
kpi(col2, f"${total_clv:,.0f}", "Total Proxied CLV", "#2A9D8F")
kpi(col3, f"{avg_discount_rate*100:.1f}%", "Avg Discount Rate", "#E76F51")
kpi(col4, f"{retention_rate*100:.1f}%", "Retention Rate (proxy)", "#9B59B6")
kpi(col5, f"${avg_clv_per_customer:.0f}", "Avg Customer Value Score", "#264653")

st.divider()

# ── Row 1: Discount Rate vs Value by Tier | Discount Efficiency ───────────────
st.markdown('<div class="section-header">💸 Discount Usage vs Customer Value</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    tier_metrics = (
        fdf.groupby("loyalty_tier")
        .agg(customers=("customer_id","count"), avg_value=("customer_value_score","mean"),
             discount_rate=("discount_flag","mean"))
        .reindex([t for t in TIER_ORDER if t in fdf["loyalty_tier"].unique()])
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(tier_metrics))
    width = 0.38
    b1 = ax.bar(x - width/2, tier_metrics["discount_rate"]*100, width,
                label="Discount Rate (%)", color=[TIER_COLORS.get(t,"#ccc") for t in tier_metrics["loyalty_tier"]],
                alpha=0.85, edgecolor="white")
    ax2 = ax.twinx()
    ax2.plot(x, tier_metrics["avg_value"], "D--", color="#264653", linewidth=2,
             markersize=7, label="Avg Value Score")
    ax2.set_ylabel("Avg Customer Value Score ($)", color="#264653")
    ax2.spines["top"].set_visible(False)
    for bar, v in zip(b1, tier_metrics["discount_rate"]):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4, f"{v*100:.1f}%",
                ha="center", fontsize=8.5, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(tier_metrics["loyalty_tier"])
    ax.set_ylabel("Discount Rate (%)")
    ax.set_title("Discount Rate vs Avg Value by Loyalty Tier", fontsize=11, fontweight="bold")
    lines1, labs1 = ax.get_legend_handles_labels()
    lines2, labs2 = ax2.get_legend_handles_labels()
    ax.legend(lines1+lines2, labs1+labs2, fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_b:
    if not tier_metrics.empty:
        tier_metrics["discount_per_value_unit"] = tier_metrics["discount_rate"] / tier_metrics["avg_value"] * 1000
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.barh(tier_metrics["loyalty_tier"],
                       tier_metrics["discount_per_value_unit"],
                       color=[TIER_COLORS.get(t,"#ccc") for t in tier_metrics["loyalty_tier"]],
                       edgecolor="white")
        for bar, v in zip(bars, tier_metrics["discount_per_value_unit"]):
            ax.text(bar.get_width()+0.01, bar.get_y()+bar.get_height()/2,
                    f"{v:.2f}", va="center", fontsize=9, fontweight="bold")
        ax.set_title("Discount Cost per $1,000 Customer Value\n(Lower = More Efficient)", fontsize=11, fontweight="bold")
        ax.set_xlabel("Discount Rate per $1,000 Value")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

st.markdown("""
<div class="insight-box">
💡 <b>Insight:</b> Loyal customers have the highest value but receive discounts at nearly the same rate as new customers. 
Discount efficiency is lowest for the segment that needs incentives least.
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Row 2: Revenue impact | Category breakdown ─────────────────────────────────
st.markdown('<div class="section-header">📈 Revenue & Category Impact</div>', unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    rev_df = (
        fdf.groupby(["loyalty_tier","discount_applied"])["purchase_amount_usd"]
        .mean().reset_index()
    )
    present_tiers = [t for t in TIER_ORDER if t in fdf["loyalty_tier"].unique()]
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(present_tiers))
    width = 0.35
    for i, (disc, label, color) in enumerate([("No","No Discount","#4C9BE8"),("Yes","Discounted","#E76F51")]):
        vals = [rev_df[(rev_df["loyalty_tier"]==t)&(rev_df["discount_applied"]==disc)]["purchase_amount_usd"].values for t in present_tiers]
        vals = [v[0] if len(v)>0 else 0 for v in vals]
        bars = ax.bar(x + i*width, vals, width, label=label, color=color, edgecolor="white", alpha=0.9)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                    f"${v:.0f}", ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x + width/2)
    ax.set_xticklabels(present_tiers)
    ax.set_title("Avg Spend: Discounted vs Non-Discounted\nby Loyalty Tier", fontsize=11, fontweight="bold")
    ax.set_ylabel("Avg Purchase Amount (USD)")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_d:
    cat_df = (
        fdf.groupby("category")
        .agg(discount_rate=("discount_flag","mean"), avg_value=("customer_value_score","mean"),
             customers=("customer_id","count"))
        .reset_index().sort_values("avg_value", ascending=True)
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = sns.color_palette("muted", len(cat_df))
    bars = ax.barh(cat_df["category"], cat_df["discount_rate"]*100, color=colors, edgecolor="white")
    for bar, (_, row) in zip(bars, cat_df.iterrows()):
        ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
                f"{row['discount_rate']*100:.1f}%", va="center", fontsize=9)
    ax.set_title("Discount Rate by Product Category", fontsize=11, fontweight="bold")
    ax.set_xlabel("% Customers Discounted")
    ax.set_xlim(0, 60)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("""
<div class="insight-box">
💡 <b>Insight:</b> If discounted and non-discounted customers spend similar amounts within each tier, 
discounts are not driving incremental revenue — they are pure margin cost.
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Row 3: Value distribution | Discount-independent segments ─────────────────
st.markdown('<div class="section-header">🎯 Segmentation & Targeting</div>', unsafe_allow_html=True)

col_e, col_f = st.columns(2)

with col_e:
    seg = (
        fdf.groupby(["loyalty_tier","value_tier"])
        .agg(customers=("customer_id","count"))
        .reset_index()
    )
    pivot = seg.pivot(index="loyalty_tier", columns="value_tier", values="customers")
    pivot = pivot.reindex([t for t in TIER_ORDER if t in pivot.index])
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(6, 4))
    bottom = np.zeros(len(pivot_pct))
    for vt, color in VALUE_COLORS.items():
        if vt in pivot_pct.columns:
            bars = ax.bar(pivot_pct.index, pivot_pct[vt], bottom=bottom,
                         label=vt, color=color, edgecolor="white", linewidth=0.5)
            for bar, v in zip(bars, pivot_pct[vt].fillna(0)):
                if v > 6:
                    ax.text(bar.get_x()+bar.get_width()/2,
                            bar.get_y()+bar.get_height()/2,
                            f"{v:.0f}%", ha="center", va="center",
                            fontsize=8, fontweight="bold", color="white")
            bottom += pivot_pct[vt].fillna(0).values
    ax.set_title("Value Tier Distribution Within Loyalty Segments", fontsize=11, fontweight="bold")
    ax.set_ylabel("% of Loyalty Tier")
    ax.legend(title="Value Tier", bbox_to_anchor=(1,1))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_f:
    overall_avg_value = df["customer_value_score"].mean()
    overall_avg_discount = df["discount_flag"].mean()
    seg_all = (
        fdf.groupby(["loyalty_tier","value_tier"])
        .agg(customers=("customer_id","count"),
             avg_value=("customer_value_score","mean"),
             discount_rate=("discount_flag","mean"))
        .reset_index()
    )
    disc_indep = seg_all[
        (seg_all["avg_value"] > overall_avg_value) &
        (seg_all["discount_rate"] < overall_avg_discount)
    ].copy()

    if not disc_indep.empty:
        disc_indep["segment"] = disc_indep["loyalty_tier"] + " / " + disc_indep["value_tier"].astype(str)
        fig, ax = plt.subplots(figsize=(6, 4))
        scatter = ax.scatter(
            disc_indep["discount_rate"]*100, disc_indep["avg_value"],
            s=disc_indep["customers"]*0.5,
            c=disc_indep["customers"], cmap="YlGn",
            edgecolors="#333", linewidths=0.7, alpha=0.9
        )
        for _, row in disc_indep.iterrows():
            ax.annotate(f"{row['loyalty_tier']} / {row['value_tier']}\n({int(row['customers'])} cust.)",
                        (row["discount_rate"]*100, row["avg_value"]),
                        textcoords="offset points", xytext=(7, 3), fontsize=7.5)
        plt.colorbar(scatter, ax=ax, label="Customers")
        ax.axvline(overall_avg_discount*100, color="red", linestyle="--", alpha=0.5, label="Avg discount rate")
        ax.set_xlabel("Discount Rate (%)")
        ax.set_ylabel("Avg Customer Value Score ($)")
        ax.set_title("Discount-Independent High-Value Segments\n(Margin Recovery Opportunity)", fontsize=11, fontweight="bold")
        ax.legend(fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        total_di = disc_indep["customers"].sum()
        st.markdown(f"""
        <div class="insight-box">
        💡 <b>{int(total_di):,} customers</b> in your filtered view are high-value and below-average discount users. 
        These are the safest candidates for a discount reduction pilot.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No discount-independent high-value segments found in the current filter selection.")

st.divider()

# ── Row 4: Subscriber analysis ─────────────────────────────────────────────────
st.markdown('<div class="section-header">🔄 Retention Signal: Subscribers vs Non-Subscribers</div>', unsafe_allow_html=True)

col_g, col_h = st.columns(2)

sub_metrics = (
    fdf.groupby(["loyalty_tier","subscription_status"])
    .agg(discount_rate=("discount_flag","mean"), avg_value=("customer_value_score","mean"),
         customers=("customer_id","count"))
    .reset_index()
)

present_tiers = [t for t in TIER_ORDER if t in fdf["loyalty_tier"].unique()]

with col_g:
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(present_tiers))
    width = 0.35
    for i, (status, color, label) in enumerate([("No","#E9C46A","Non-Subscriber"),("Yes","#2A9D8F","Subscriber")]):
        vals = [sub_metrics[(sub_metrics["loyalty_tier"]==t)&(sub_metrics["subscription_status"]==status)]["discount_rate"].values for t in present_tiers]
        vals = [v[0]*100 if len(v)>0 else 0 for v in vals]
        bars = ax.bar(x + i*width, vals, width, label=label, color=color, edgecolor="white", alpha=0.9)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                    f"{v:.1f}%", ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x + width/2)
    ax.set_xticklabels(present_tiers)
    ax.set_title("Discount Rate: Subscriber vs Non-Subscriber", fontsize=11, fontweight="bold")
    ax.set_ylabel("% Receiving Discount")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_h:
    fig, ax = plt.subplots(figsize=(6, 4))
    for i, (status, color, label) in enumerate([("No","#E9C46A","Non-Subscriber"),("Yes","#2A9D8F","Subscriber")]):
        vals = [sub_metrics[(sub_metrics["loyalty_tier"]==t)&(sub_metrics["subscription_status"]==status)]["avg_value"].values for t in present_tiers]
        vals = [v[0] if len(v)>0 else 0 for v in vals]
        bars = ax.bar(x + i*width, vals, width, label=label, color=color, edgecolor="white", alpha=0.9)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                    f"${v:.0f}", ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x + width/2)
    ax.set_xticklabels(present_tiers)
    ax.set_title("Avg Value Score: Subscriber vs Non-Subscriber", fontsize=11, fontweight="bold")
    ax.set_ylabel("Avg Customer Value Score ($)")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("""
<div class="insight-box">
💡 <b>Insight:</b> If subscribers show higher value but similar or lower discount dependency, 
the subscription itself is doing the retention work — validating a strategy of expanding 
subscription perks rather than deepening discounts.
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Raw data explorer ─────────────────────────────────────────────────────────
with st.expander("🗄️ Explore Filtered Customer Data"):
    display_cols = ["customer_id","age","gender","category","purchase_amount_usd",
                    "loyalty_tier","value_tier","customer_value_score",
                    "discount_applied","subscription_status","review_rating"]
    st.dataframe(fdf[display_cols].sort_values("customer_value_score", ascending=False), use_container_width=True)
    st.caption(f"{len(fdf):,} customers in current filter.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Dashboard built by Victor Muthii · Customer Segmentation & Personalization Project · Python / Streamlit / Matplotlib / Seaborn")
