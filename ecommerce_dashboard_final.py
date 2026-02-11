
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Sales.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title("🛒 E-Commerce Sales Dashboard")

# Show detected columns
st.subheader("📌 Detected Columns")
st.write(list(df.columns))

# ---- Column Mapping (adjusted automatically) ----
def find_col(keywords):
    for col in df.columns:
        for k in keywords:
            if k in col.lower():
                return col
    return None

date_col = find_col(["date", "order"])
sales_col = find_col(["sales", "revenue", "amount"])
profit_col = find_col(["profit"])
quantity_col = find_col(["quantity", "qty"])
category_col = find_col(["category"])
region_col = find_col(["region"])
subcat_col = find_col(["sub"])

# ---- Date Processing ----
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df["Month"] = df[date_col].dt.to_period("M").astype(str)

# ---- Sidebar Filters ----
st.sidebar.header("🔎 Filters")

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

# ---- KPIs ----
col1, col2, col3, col4 = st.columns(4)

if sales_col:
    col1.metric("💰 Total Sales", f"{df[sales_col].sum():,.0f}")
if profit_col:
    col2.metric("📈 Total Profit", f"{df[profit_col].sum():,.0f}")
if quantity_col:
    col3.metric("📦 Quantity Sold", int(df[quantity_col].sum()))

col4.metric("🧾 Total Orders", len(df))

st.markdown("---")

# ---- Charts Section ----
st.subheader("📊 Sales Analysis")

if category_col and sales_col:
    cat_sales = df.groupby(category_col)[sales_col].sum().reset_index()

    colA, colB = st.columns(2)

    with colA:
        st.plotly_chart(
            px.bar(
                cat_sales,
                x=category_col,
                y=sales_col,
                title="Sales by Category",
                color=category_col
            ),
            use_container_width=True
        )

    with colB:
        st.plotly_chart(
            px.pie(
                cat_sales,
                names=category_col,
                values=sales_col,
                title="Category-wise Sales Distribution"
            ),
            use_container_width=True
        )

if "Month" in df.columns and sales_col:
    monthly = df.groupby("Month")[sales_col].sum().reset_index()
    st.plotly_chart(
        px.line(
            monthly,
            x="Month",
            y=sales_col,
            markers=True,
            title="Monthly Sales Trend"
        ),
        use_container_width=True
    )

if region_col and profit_col:
    region_profit = df.groupby(region_col)[profit_col].sum().reset_index()
    st.plotly_chart(
        px.bar(
            region_profit,
            x=region_col,
            y=profit_col,
            title="Region-wise Profit",
            color=region_col
        ),
        use_container_width=True
    )

if subcat_col and sales_col:
    sub_sales = df.groupby(subcat_col)[sales_col].sum().reset_index()
    st.plotly_chart(
        px.bar(
            sub_sales.sort_values(by=sales_col, ascending=False),
            x=sales_col,
            y=subcat_col,
            orientation="h",
            title="Top Sub-Categories by Sales"
        ),
        use_container_width=True
    )

# ---- Raw Data ----
with st.expander("📄 View Raw Data"):
    st.dataframe(df)

st.markdown("✅ Interactive Dashboard with Pie, Bar & Line Charts")
