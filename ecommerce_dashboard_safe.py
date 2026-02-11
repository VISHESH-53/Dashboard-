
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Sales.csv")
    df.columns = df.columns.str.strip()  # remove extra spaces

    # Auto-detect date column
    date_col = None
    for col in df.columns:
        if "date" in col.lower():
            date_col = col
            break

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df["Month"] = df[date_col].dt.to_period("M").astype(str)
    else:
        st.error("❌ No date column found in dataset")

    return df

df = load_data()

st.title("🛒 E-Commerce Sales Dashboard")

# Sidebar filters
st.sidebar.header("🔎 Filters")

category_col = next((c for c in df.columns if "category" in c.lower()), None)
region_col = next((c for c in df.columns if "region" in c.lower()), None)

if category_col:
    categories = st.sidebar.multiselect(
        "Category",
        df[category_col].unique(),
        default=df[category_col].unique()
    )
    df = df[df[category_col].isin(categories)]

if region_col:
    regions = st.sidebar.multiselect(
        "Region",
        df[region_col].unique(),
        default=df[region_col].unique()
    )
    df = df[df[region_col].isin(regions)]

# KPI auto-detection
sales_col = next((c for c in df.columns if "sales" in c.lower()), None)
profit_col = next((c for c in df.columns if "profit" in c.lower()), None)
quantity_col = next((c for c in df.columns if "quantity" in c.lower()), None)

col1, col2, col3, col4 = st.columns(4)

if sales_col:
    col1.metric("💰 Total Sales", f"{df[sales_col].sum():,.0f}")
if profit_col:
    col2.metric("📈 Total Profit", f"{df[profit_col].sum():,.0f}")
if quantity_col:
    col3.metric("📦 Quantity", int(df[quantity_col].sum()))

col4.metric("🧾 Orders", len(df))

st.markdown("---")

# Charts
if category_col and sales_col:
    cat_sales = df.groupby(category_col)[sales_col].sum().reset_index()
    st.plotly_chart(
        px.bar(cat_sales, x=category_col, y=sales_col, title="Sales by Category"),
        use_container_width=True
    )

    st.plotly_chart(
        px.pie(cat_sales, names=category_col, values=sales_col, title="Sales Distribution"),
        use_container_width=True
    )

if "Month" in df.columns and sales_col:
    monthly = df.groupby("Month")[sales_col].sum().reset_index()
    st.plotly_chart(
        px.line(monthly, x="Month", y=sales_col, markers=True, title="Monthly Sales Trend"),
        use_container_width=True
    )

st.markdown("### 📄 Raw Data")
st.dataframe(df)
