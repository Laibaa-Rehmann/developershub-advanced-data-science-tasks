import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.write("NEW CODE IS RUNNING")
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

# =========================
# LOAD DATA (FIXED FOR ALL ENCODING ISSUES)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(
        r'C:\Users\FA23-BCS-041.CUI\Desktop\datasets\Global_Superstore2.csv',
        encoding='latin1',
        engine='python',
        on_bad_lines='skip'
    )

    df.columns = df.columns.str.strip()

    # Convert numeric safely
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")

    df = df.dropna(subset=["Sales", "Profit"])

    return df


df = load_data()

# =========================
# TITLE
# =========================
st.title("📊 Global Superstore Dashboard")

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.title("Filters")

region_list = df["Region"].dropna().unique()
category_list = df["Category"].dropna().unique()
subcategory_list = df["Sub-Category"].dropna().unique()

region = st.sidebar.multiselect("Select Region", region_list, default=region_list)
category = st.sidebar.multiselect("Select Category", category_list, default=category_list)
subcategory = st.sidebar.multiselect("Select Sub-Category", subcategory_list, default=subcategory_list)

# =========================
# FILTER DATA
# =========================
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(subcategory))
]

# =========================
# KPI METRICS
# =========================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Total Profit", f"{total_profit:,.0f}")

# =========================
# SALES BY CATEGORY
# =========================
st.subheader("Sales by Category")

cat_data = filtered_df.groupby("Category")["Sales"].sum().reset_index()

fig1 = px.bar(cat_data, x="Category", y="Sales", color="Category")
st.plotly_chart(fig1, use_container_width=True)

# =========================
# TOP 5 CUSTOMERS
# =========================
st.subheader("Top 5 Customers")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig2 = px.bar(top_customers, x="Customer Name", y="Sales", color="Sales")
st.plotly_chart(fig2, use_container_width=True)

# =========================
# RAW DATA
# =========================
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
