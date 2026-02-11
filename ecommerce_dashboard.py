
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Sales.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔎 Filter Options")

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Category"].isin(category_filter)) &
    (df["Region"].isin(region_filter))
]

# ---------------- KPIs ----------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_orders = filtered_df.shape[0]

st.title("🛒 E-Commerce Sales Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
col3.metric("📦 Quantity Sold", total_quantity)
col4.metric("🧾 Total Orders", total_orders)

st.markdown("---")

# ---------------- SALES BY CATEGORY ----------------
col1, col2 = st.columns(2)

with col1:
    cat_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_bar = px.bar(
        cat_sales,
        x="Category",
        y="Sales",
        title="Sales by Category",
        color="Category"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_pie = px.pie(
        cat_sales,
        names="Category",
        values="Sales",
        title="Category-wise Sales Distribution"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- SALES TREND ----------------
filtered_df["Month"] = filtered_df["Order Date"].dt.to_period("M").astype(str)
monthly_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()

fig_line = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig_line, use_container_width=True)

# ---------------- PROFIT BY REGION ----------------
col1, col2 = st.columns(2)

with col1:
    region_profit = filtered_df.groupby("Region")["Profit"].sum().reset_index()
    fig_region = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        color="Region",
        title="Profit by Region"
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    subcat_sales = filtered_df.groupby("Sub-Category")["Sales"].sum().reset_index()
    fig_subcat = px.bar(
        subcat_sales.sort_values(by="Sales", ascending=False),
        x="Sales",
        y="Sub-Category",
        orientation="h",
        title="Top Sub-Categories by Sales"
    )
    st.plotly_chart(fig_subcat, use_container_width=True)

# ---------------- RAW DATA ----------------
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)

st.markdown("✅ Dashboard built using Streamlit & Plotly")
