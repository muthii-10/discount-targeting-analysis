# Customer Segmentation & Personalization Analytics  
**E-commerce Retail | Fashion & Lifestyle**

## 📌 Project Overview
This project analyzes customer shopping behavior for a mid-sized e-commerce retailer in the fashion / lifestyle space.  
The business is facing rising marketing costs and margin pressure due to blanket discounting strategies that treat all customers the same.

The goal of this project is to **segment customers based on value and loyalty**, evaluate the **effectiveness of discounts**, and provide **data-driven recommendations** for personalized marketing, loyalty rewards, and margin protection.

---

## 🚀 Live Dashboard

> **Discount Strategy & Customer Engagement Dashboard**  
> Interactive exploration of all segmentation findings — filter by loyalty tier, value tier, product category, and subscription status.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://customer-segmentation-and-personalization-n3stlwdayzsumw24kitb.streamlit.app)

**Dashboard KPIs tracked:**
- Total Customers
- Total Proxied CLV
- Avg Discount Rate
- Customer Retention Rate (proxy)
- Avg Customer Value Score

**Dashboard sections:**
- Discount usage vs customer value by loyalty tier
- Discount efficiency (cost per $1,000 customer value)
- Revenue impact: discounted vs non-discounted customers
- Category-level discount and value analysis
- Value tier distribution within loyalty segments
- Discount-independent high-value segment identifier
- Subscriber vs non-subscriber retention signal
- Raw customer data explorer with live filters

---

## 🎯 Business Problem
> *“We are spending heavily on promotions but treating all customers the same.”*

Key challenges:
- Discounts applied broadly with limited targeting
- High-value and loyal customers receiving unnecessary incentives
- Lack of visibility into which segments truly need promotions

---

## 🧠 Key Objectives
- Identify high-value and high-loyalty customer segments
- Evaluate discount usage relative to customer value
- Surface opportunities to reduce promotional spend without hurting retention
- Enable smarter personalization and loyalty strategies

---

## 🗂 Dataset Overview
The dataset contains **customer-level shopping behavior data**, including:
- Demographics (age, gender, location)
- Purchase behavior (amount, category, frequency)
- Engagement signals (subscription status, previous purchases)
- Promotion usage (discounts, promo codes)
- Fulfillment preferences (shipping type, payment method)

Each row represents a **single customer snapshot**, not full transaction history.

---

## 🔄 Project Workflow

### 1️⃣ Data Profiling and Cleaning
Key steps:
- Loaded raw CSV data into Python using `pandas`
- Performed EDA
- Renamed columns for consistency (snake_case)
- Converted binary fields (Yes/No) to numerical flags
- Standardized categorical values (frequency of purchases)
- Handled missing and invalid values
- Ensured correct data types for numerical and categorical fields  

📁 Relevant file:
- [Data Profiling and Cleaning Notebook](./notebooks/01_data_profiling_and_cleaning.ipynb)

---

### 2️⃣ Data Transformation

Since full transaction histories were unavailable, customer-level features were engineered using available signals.

#### Engineered Features:
- **Loyalty indicators**
  - Loyalty tiers (New / Returning / Loyal)
  - Encoded purchase frequency
- **Value indicators**
  - Customer value score (proxy for lifetime value)
  - Value tiers (Low / Medium / High)
- **Behavioral indicators**
  - Discount usage flag
  - Subscription flag

These features enabled segmentation, ranking, and efficiency analysis.


📁 Relevant file:
- [Feature Engineering Notebook](./notebooks/02_data_transformation.ipynb)  

📄 Output table:
- `customer_features` (PostgreSQL)

---

## 🧮 SQL Analysis (Core Business Questions)

All strategic analysis was performed in **PostgreSQL**, using:
- Common Table Expressions (CTEs)
- Window functions
- Conditional aggregation
- Tier-based segmentation logic

### 📊 Key SQL Analyses

#### 1. Discount Usage Rate and Average Customer Value by Loyalty Segments  

| loyalty_Tier | customers | avg_customer value_score | discount_usage_rate |
|--------------|-----------|--------------------------|---------------------|
| Loyal        | 2721      | 267.78                   | 0.44                |
| Returning    | 755       | 201.92                   | 0.42                |
| New          | 424       | 141.99                   | 0.40                |



---

#### 2. Average Customer Value Per Product Category 
| category     | customers | avg_customer_value_score |
|--------------|-----------|--------------------------|
| Footwear     | 599       | 243.75                   |
| Clothing     | 1737      | 242.79                   |
| Accessories  | 1240      | 241.89                   |
| Outerwear    | 324       | 227.17                   |


---

#### 3. Normalized Discount Usage by Customer Value
| loyalty_tier | avg_value | discount_rate | discount_per_value_unit |
|--------------|-----------|---------------|--------------------------|
| New          | 141.99    | 0.40          | 0.003                    |
| Returning    | 201.92    | 0.42          | 0.002                    |
| Loyal        | 267.78    | 0.44          | 0.002                    |


---

#### 4. High-Value, Discount Independent Customers
| loyalty_tier | value_tier | customers | avg_value | discount_rate |
|--------------|------------|-----------|-----------|---------------|
| Loyal        | High       | 887       | 392.33    | 0.43          |
| Returning    | High       | 258       | 296.58    | 0.43          |


---

#### 5. Value Tier Distribution Within Loyalty Segments
| loyalty_tier | value_tier | customers | pct_within_loyalty |
|--------------|------------|-----------|--------------------|
| Loyal        | Medium     | 938       | 0.345              |
| Loyal        | Low        | 896       | 0.329              |
| Loyal        | High       | 887       | 0.326              |
| New          | High       | 152       | 0.358              |
| New          | Medium     | 137       | 0.323              |
| New          | Low        | 135       | 0.318              |
| Returning    | Low        | 269       | 0.356              |
| Returning    | High       | 258       | 0.342              |
| Returning    | Medium     | 228       | 0.302              |


---

#### 6. Tier-Aware Top 10% Customers
| customer_id | loyalty_tier | customer_value_score |
|-------------|--------------|----------------------|
| 456  | Loyal     | 493.18 |
| 1848 | Loyal     | 491.20 |
| 96   | Loyal     | 489.18 |
| 2843 | Loyal     | 489.18 |
| 993  | Loyal     | 488.25 |
| 1301 | Loyal     | 487.12 |
| 3747 | Loyal     | 486.29 |
| 2272 | Loyal     | 486.29 |
| 886  | Loyal     | 486.29 |
| 2600 | Loyal     | 484.29 |
| 2065 | New       | 276.39 |
| 3269 | New       | 270.80 |
| 1278 | New       | 270.80 |
| 1375 | New       | 270.80 |
| 2406 | New       | 270.80 |
| 3561 | New       | 268.01 |
| 1967 | New       | 265.22 |
| 751  | New       | 265.22 |
| 3541 | New       | 265.22 |
| 3260 | New       | 265.22 |
| 43   | Returning | 377.26 |
| 2995 | Returning | 370.81 |
| 2952 | Returning | 367.10 |
| 3442 | Returning | 362.17 |
| 766  | Returning | 360.27 |
| 455  | Returning | 359.69 |
| 1438 | Returning | 359.69 |
| 1991 | Returning | 358.40 |
| 582  | Returning | 356.49 |
| 1872 | Returning | 355.98 |


---

#### 7. Discount Removal Insensitive Customers
| loyalty_tier | value_tier | avg_value | discount_rate |
|--------------|------------|-----------|---------------|
| New          | High       | 204.98    | 0.38          |
| Returning    | Low        | 109.80    | 0.39          |



---

## 💡 Key Insights
- **Loyal customers are over-discounted.** 2,721 Loyal customers receive discounts at 44% — nearly identical to New customers (40%) — despite generating 89% more avg value ($268 vs $142)
- **Discounts are not driving incremental revenue.** Purchase amounts are similar between discounted and non-discounted customers within each loyalty tier
- **1,145 high-value customers are discount-independent.** Loyal/High (887 customers, avg $392) and Returning/High (258 customers, avg $297) have above-average value and below-average discount usage — immediate margin recovery opportunity
- **Loyalty and value are not the same dimension.** Value tiers distribute ~33/33/33 within every loyalty tier — blanket loyalty rewards are as inefficient as blanket discounts
- **Subscription is the retention model that works.** Subscribers show higher avg value than non-subscribers across all tiers — scaling subscription perks is more effective than deepening discounts
- **All 4 product categories show near-identical avg value ($228–$244).** Category is not a value predictor; loyalty and value tier are

---

## ✅ Recommendations

### Rec 1 — Stop Over-Discounting Loyal & High-Value Customers
- 887 Loyal/High-value customers (avg $392) receive a 43% discount rate they don't need to convert
- Gradually reduce discounts for this cohort; replace with non-monetary rewards — early access to new collections, exclusive product drops, free express shipping
- Communicate tier benefits clearly so customers understand what replaces the discount
- **Impact:** 1,145 high-value, discount-independent customers identified — immediate margin recovery with zero revenue risk

### Rec 2 — Introduce Targeted Discounting by Segment
- **New customers** (424 total, avg value $142): onboarding discounts to drive first repeat purchase
- **Low-value / price-sensitive customers**: targeted promotions tied to minimum basket size to drive spend uplift
- **Returning/lapsed customers** (755 total, avg value $202): reactivation offers with behavioural triggers
- **Impact:** Discount rate gap between New (40%) and Loyal (44%) is only 4pp — precision targeting can unlock significant margin improvement

### Rec 3 — Personalize Marketing Based on Customer Segments
- **High-value customers** (avg $392): premium product recommendations, VIP experiences, no discounts
- **Discount-sensitive customers**: deal-focused messaging and targeted promotions tied to basket thresholds
- **Category-specific buyers**: tailored product suggestions based on Footwear, Clothing, Accessories, Outerwear behaviour
- **Impact:** All 4 product categories show near-identical avg value ($228–$244) — category is not a value predictor; segment tier is

### Rec 4 — Shift from Discounts to Value-Based Incentives
- Bundled offers, loyalty points, and personalised recommendations replace cash discounts for high-value segments
- Loyalty points redeemable for store credit — builds retention without eroding margin
- Premium experiences for Loyal/High-value customers: styling sessions, members-only drops, VIP events
- **Impact:** Subscribers show higher avg value than non-subscribers across all tiers — subscription is the retention model that works; scale it

### Rec 5 — Build a Customer Value Monitoring Dashboard ✅ Deployed
- Live Streamlit dashboard tracking Total Customers, Total Proxied CLV, Avg Discount Rate, Retention Rate, and Avg Customer Value Score
- Filter by loyalty tier, value tier, category, and subscription status — enables segment-level decisions for CRM and marketing teams
- Surfaces discount-independent high-value segments dynamically — flags margin recovery opportunities as filters change
- 🔗 **[Open Dashboard →](https://customer-segmentation-and-personalization-n3stlwdayzsumw24kitb.streamlit.app)**

---

## 🚀 Next Steps
- Commission 90-day pilot on Loyal/High-value cohort (887 customers) — remove discounts, replace with experience perks, track retention and revenue weekly
- Simulate discount reduction scenarios on full customer base to model revenue impact before full rollout
- Add recommendation engine slides for executive audience
- Extend dashboard with A/B test result tracking

---

## 🛠 Tools & Technologies
- **Python** (pandas, numpy, matplotlib, seaborn)
- **PostgreSQL**
- **Streamlit** (live dashboard)
- **Jupyter Notebooks**
- **Git & GitHub** (version control & portfolio)

---

## 👤 Author
Victor Muthii  
mv.munene01@gmail.com
