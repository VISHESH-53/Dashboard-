
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Sales.csv")
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Sales"] = df["Price"] * df["Units_Sold"] * (1 - df["Discount"] / 100)
    return df

df = load_data()

st.title("🛒 E-Commerce Sales Dashboard")

# Sidebar filters
st.sidebar.header("🔎 Filters")

categories = st.sidebar.multiselect(
    "Product Category",
    df["Product_Category"].unique(),
    default=df["Product_Category"].unique()
)

segments = st.sidebar.multiselect(
    "Customer Segment",
    df["Customer_Segment"].unique(),
    default=df["Customer_Segment"].unique()
)

df = df[
    (df["Product_Category"].isin(categories)) &
    (df["Customer_Segment"].isin(segments))
]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"{df['Sales'].sum():,.0f}")
col2.metric("📦 Units Sold", int(df["Units_Sold"].sum()))
col3.metric("🎯 Avg Discount (%)", round(df["Discount"].mean(), 2))
col4.metric("🧾 Total Orders", len(df))

st.markdown("---")

# PIE + BAR CHARTS
st.subheader("📊 Category-wise Sales Analysis")

cat_sales = df.groupby("Product_Category")["Sales"].sum().reset_index()

colA, colB = st.columns(2)

with colA:
    st.plotly_chart(
        px.pie(
            cat_sales,
            names="Product_Category",
            values="Sales",
            title="Sales Distribution by Category"
        ),
        use_container_width=True
    )

with colB:
    st.plotly_chart(
        px.bar(
            cat_sales,
            x="Product_Category",
            y="Sales",
            color="Product_Category",
            title="Sales by Product Category"
        ),
        use_container_width=True
    )

# LINE GRAPH
st.subheader("📈 Monthly Sales Trend")

monthly_sales = df.groupby("Month")["Sales"].sum().reset_index()

st.plotly_chart(
    px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    ),
    use_container_width=True
)

# CUSTOMER SEGMENT ANALYSIS
st.subheader("👥 Customer Segment Analysis")

segment_sales = df.groupby("Customer_Segment")["Sales"].sum().reset_index()

st.plotly_chart(
    px.bar(
        segment_sales,
        x="Customer_Segment",
        y="Sales",
        color="Customer_Segment",
        title="Sales by Customer Segment"
    ),
    use_container_width=True
)

# RAW DATA
with st.expander("📄 View Raw Data"):
    st.dataframe(df)

st.markdown("✅ Fully Functional Dashboard with Pie, Bar & Line Charts")
