import pandas as pd  # pip install pandas openpyxl
import numpy as np
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import seaborn as sns

tips_df = sns.load_dataset("tips")

# Sidebar multiselect for selecting options from the "time" column
time_select = st.sidebar.multiselect(
    "Select time option:",
    options=tips_df["time"].unique(),
    default=list(tips_df["time"].unique())
)
sex_select = st.sidebar.multiselect(
    "Select gender option:",
    options=tips_df["sex"].unique(),
    default=list(tips_df["sex"].unique())
)

smoker_select = st.sidebar.multiselect(
    "Select smoker option:",
    options=tips_df["smoker"].unique(),
    default=list(tips_df["smoker"].unique())
)

# Slider for selecting the size
size_slider = st.sidebar.slider(
    "Select size:", 
    min_value=tips_df["size"].min(), 
    max_value=tips_df["size"].max(), 
    value=(tips_df["size"].min(), tips_df["size"].max()), 
    step=1
)

filtered_df = tips_df[
    (tips_df["time"].isin(time_select)) &
    (tips_df["size"] >= size_slider[0]) &
    (tips_df["size"] <= size_slider[1])
]

st.dataframe(filtered_df)

fig = px.scatter(filtered_df, x='total_bill', y='tip', title='Tips Data Scatter Plot')
st.plotly_chart(fig)