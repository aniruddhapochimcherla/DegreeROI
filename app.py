"""The Degree Dividend: Early-Career ROI Dashboard.

Interactive dashboard exploring post-graduation earnings, debt burden,
and earnings trajectory across the top 50 U.S. Bachelor's degrees.
"""

from typing import Tuple
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Application Configuration
st.set_page_config(
    page_title="The Degree Dividend",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 The Degree Dividend: Early-Career ROI Across College Majors")
st.markdown(
    """
This dashboard benchmarks early-career outcomes (1 to 4 years post-graduation)
across the **Top 50 most conferred Bachelor's degrees** in the United States,
combining **IPEDS** completions and **College Scorecard** financial metrics.
"""
)


@st.cache_data
def load_data(filepath: str = "top_50_majors_outcomes.csv") -> pd.DataFrame:
    """Load pre-computed economic summary dataset."""
    return pd.read_csv(filepath)


df = load_data()

# -------------------------------------------------------------
# Sidebar: Custom Composite Value Index
# -------------------------------------------------------------
st.sidebar.header("🎯 Custom Value Score Weights")
st.sidebar.caption(
    "Calibrate preference weights to compute a dynamic composite ranking."
)

weight_earnings = st.sidebar.slider(
    "Weight: 4-Year Earnings", 0.0, 1.0, 0.40, step=0.05
)
weight_debt = st.sidebar.slider(
    "Weight: Low Debt Burden", 0.0, 1.0, 0.35, step=0.05
)
weight_growth = st.sidebar.slider(
    "Weight: Early Wage Growth", 0.0, 1.0, 0.25, step=0.05
)

# Feature normalization (Min-Max Scaling to [0, 1])
norm_earnings = (
    df["national_median_earn_4yr"] - df["national_median_earn_4yr"].min()
) / (df["national_median_earn_4yr"].max() - df["national_median_earn_4yr"].min())

# Invert debt-to-earnings scale so lower debt corresponds to a higher score
norm_debt = (
    df["debt_to_earnings_ratio"].max() - df["debt_to_earnings_ratio"]
) / (df["debt_to_earnings_ratio"].max() - df["debt_to_earnings_ratio"].min())

norm_growth = (
    df["early_wage_growth_pct"] - df["early_wage_growth_pct"].min()
) / (df["early_wage_growth_pct"].max() - df["early_wage_growth_pct"].min())

total_weight = weight_earnings + weight_debt + weight_growth

if total_weight > 0:
    composite_raw = (
        (weight_earnings * norm_earnings)
        + (weight_debt * norm_debt)
        + (weight_growth * norm_growth)
    ) / total_weight
    df["composite_score"] = np.round(composite_raw * 100, 1)
else:
    df["composite_score"] = 0.0

# -------------------------------------------------------------
# Main Controls: Sorting and Filtering
# -------------------------------------------------------------
col_select, _ = st.columns([2, 1])

sort_criteria = {
    "Best Composite Value Score": ("composite_score", False),
    "Highest 4-Year Median Earnings": ("national_median_earn_4yr", False),
    "Highest Earnings Premium (%)": ("earnings_premium_pct", False),
    "Lowest Debt-to-Earnings Ratio": ("debt_to_earnings_ratio", True),
    "Highest Early Wage Growth (%)": ("early_wage_growth_pct", False),
    "Highest Downside Risk Floor (25th Pct)": ("downside_risk_earn_4yr", False),
    "Most Popular (Total Conferred)": ("total_conferred", False),
}

with col_select:
    selected_ranking = st.selectbox(
        "Rank Majors By:", list(sort_criteria.keys())
    )

target_column, ascending_order = sort_criteria[selected_ranking]
ranked_df = df.sort_values(
    by=target_column, ascending=ascending_order
).reset_index(drop=True)

# -------------------------------------------------------------
# Headline Metrics (Leader for Selected Metric)
# -------------------------------------------------------------
top_major = ranked_df.iloc[0]
st.write("")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Top Ranked Major", f"{top_major['major_title'][:26]}...")
col_m2.metric(
    "Median 4-Yr Earnings", f"${top_major['national_median_earn_4yr']:,.0f}"
)
col_m3.metric("Debt-to-Earnings", f"{top_major['debt_to_earnings_ratio']:.3f}")
col_m4.metric("Earnings Premium", f"{top_major['earnings_premium_pct']:+.1f}%")

st.divider()

# -------------------------------------------------------------
# Visual: Earnings vs. Debt-to-Earnings Distribution
# -------------------------------------------------------------
st.subheader("📊 Post-Graduation Landscape: Earnings vs. Debt Burden")

fig = px.scatter(
    df,
    x="debt_to_earnings_ratio",
    y="national_median_earn_4yr",
    size="total_conferred",
    hover_name="major_title",
    hover_data={
        "cip4": True,
        "earnings_premium_pct": ":.1f%",
        "early_wage_growth_pct": ":.1f%",
        "debt_to_earnings_ratio": ":.3f",
        "national_median_earn_4yr": ":$,.0f",
    },
    labels={
        "debt_to_earnings_ratio": "Debt-to-Earnings Ratio (Lower is Better)",
        "national_median_earn_4yr": "Median Earnings 4-Years Post-Graduation ($)",
        "total_conferred": "Annual Graduates",
    },
    title="Bubble size represents annual conferral volume across U.S. institutions",
    template="plotly_white",
)

fig.update_layout(height=520)
st.plotly_chart(fig, width="stretch")

# -------------------------------------------------------------
# Tabular View: Ranked Output
# -------------------------------------------------------------
st.subheader("📋 Top 50 Majors Ranked")

table_view = ranked_df[
    [
        "cip4",
        "major_title",
        "composite_score",
        "national_median_earn_4yr",
        "debt_to_earnings_ratio",
        "earnings_premium_pct",
        "early_wage_growth_pct",
        "total_conferred",
    ]
].copy()

table_view.columns = [
    "CIP",
    "Major Title",
    "Composite Score",
    "4-Yr Median Pay",
    "Debt/Earnings",
    "Earnings Premium",
    "Wage Growth (1-4yr)",
    "Total Conferred",
]

st.dataframe(
    table_view.style.format(
        {
            "Composite Score": "{:.1f}",
            "4-Yr Median Pay": "${:,.0f}",
            "Debt/Earnings": "{:.3f}",
            "Earnings Premium": "{:+.1f}%",
            "Wage Growth (1-4yr)": "{:+.1f}%",
            "Total Conferred": "{:,.0f}",
        }
    ),
    width="stretch",
    height=450,
)
