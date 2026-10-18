import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Business Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Generate Sample Data
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=90, freq="D")
    
    categories = ["Electronics", "Fashion", "Home & Kitchen", "Books", "Sports"]
    regions = ["North", "South", "East", "West"]
    
    records = []
    for date in dates:
        for _ in range(np.random.randint(5, 12)):
            cat = np.random.choice(categories)
            reg = np.random.choice(regions)
            revenue = round(np.random.uniform(50, 500), 2)
            marketing_spend = round(revenue * np.random.uniform(0.1, 0.4), 2)
            visitors = int(revenue * np.random.uniform(1.5, 3.5))
            
            records.append({
                "Date": date,
                "Category": cat,
                "Region": reg,
                "Revenue": revenue,
                "Marketing_Spend": marketing_spend,
                "Visitors": visitors
            })
            
    df = pd.DataFrame(records)
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("🔍 Filters")

selected_region = st.sidebar.multiselect(
    "Select Region(s):",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category(ies):",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Filter Dataframe
filtered_df = df[
    (df["Region"].isin(selected_region)) & 
    (df["Category"].isin(selected_category))
]

# 4. Header & Top Metrics
st.title("📊 Business Performance Dashboard")
st.markdown("An interactive overview of sales performance, marketing impact, and regional distributions.")

total_revenue = filtered_df["Revenue"].sum()
total_spend = filtered_df["Marketing_Spend"].sum()
total_visitors = filtered_df["Visitors"].sum()
roas = round(total_revenue / total_spend, 2) if total_spend > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${total_revenue:,.2f}", delta="+8.4%")
col2.metric("Marketing Spend", f"${total_spend:,.2f}", delta="-2.1%")
col3.metric("Total Visitors", f"{total_visitors:,}", delta="+12.3%")
col4.metric("ROAS", f"{roas}x", delta="+0.4x")

st.divider()

# 5. Row 1: Line Chart & Area Chart
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Revenue Trend Over Time")
    daily_trend = filtered_df.groupby("Date")[["Revenue", "Marketing_Spend"]].sum().reset_index()
    fig_trend = px.line(
        daily_trend, 
        x="Date", 
        y=["Revenue", "Marketing_Spend"],
        labels={"value": "Amount ($)", "variable": "Metric"},
        color_discrete_map={"Revenue": "#1f77b4", "Marketing_Spend": "#ff7f0e"}
    )
    fig_trend.update_layout(hovermode="x unified", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.subheader("🌊 Cumulative Visitors Growth")
    daily_visitors = filtered_df.groupby("Date")["Visitors"].sum().cumsum().reset_index()
    fig_area = px.area(
        daily_visitors,
        x="Date",
        y="Visitors",
        color_discrete_sequence=["#2ca02c"]
    )
    fig_area.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_area, use_container_width=True)

# 6. Row 2: Bar Chart & Donut Chart
col_bar, col_pie = st.columns(2)

with col_bar:
    st.subheader("📊 Sales by Product Category")
    category_summary = (
        filtered_df.groupby("Category")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
    )
    fig_bar = px.bar(
        category_summary,
        x="Category",
        y="Revenue",
        color="Category",
        text_auto=".2s"
    )
    fig_bar.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_pie:
    st.subheader("🍩 Revenue Share by Region")
    region_summary = filtered_df.groupby("Region")["Revenue"].sum().reset_index()
    fig_pie = px.pie(
        region_summary,
        names="Region",
        values="Revenue",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

# 7. Row 3: Scatter Plot
st.subheader("🎯 Marketing Spend vs. Revenue Correlation")
fig_scatter = px.scatter(
    filtered_df,
    x="Marketing_Spend",
    y="Revenue",
    color="Category",
    size="Visitors",
    hover_data=["Region", "Date"],
    opacity=0.75
)
fig_scatter.update_layout(margin=dict(l=20, r=20, t=30, b=20))
st.plotly_chart(fig_scatter, use_container_width=True)

# 8. Raw Data Inspection
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)
