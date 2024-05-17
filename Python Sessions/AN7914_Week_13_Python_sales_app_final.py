import pandas as pd  # pip install pandas openpyxl
import numpy as np
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

st.sidebar.header("Please Filter Here:")

@st.cache_data
def get_data_csv() :
    df=pd.read_csv('sales_uk.csv')
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df=get_data_csv()
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)

#st.dataframe(df_selection)


# ---- MAINPAGE ----
st.title("Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum()) ## only show integer values
average_rating = round(df_selection["Rating"].mean(), 1) # round to 1 decimal
star_rating = ":star:" * int(round(average_rating, 0)) #only show integer
average_sale_by_transaction = round(df_selection["Total"].mean(), 2) 

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"£ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"£ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    #color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)


sales_by_hour = df_selection.groupby("hour")[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    #color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
