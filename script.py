from re import template
from turtle import left
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title='Sales Dashboard ⚡️',
    page_icon=':bar_chart',
    layout="wide",
)


def get_data_from_excel():
  dataset = pd.read_excel(
    io='./supermarkt_sales.xlsx',
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols="B:R",
    nrows=1000,
    )
  dataset["hour"] = pd.to_datetime(
    dataset["Time"], format="%H:%M:%S").dt.hour
  return dataset

dataset=get_data_from_excel()


# SIDEBAR
# filter based on different cities,

st.sidebar.header("Data Filter")
city = st.sidebar.multiselect(
    "Select the City",
    options=dataset["City"].unique(),
    default=dataset["City"].unique(),
)
customer_type = st.sidebar.multiselect(
    "Select the Customer Type",
    options=dataset["Customer_type"].unique(),
    default=dataset["Customer_type"].unique(),
)
gender = st.sidebar.multiselect(
    "Select the Gender",
    options=dataset["Gender"].unique(),
    default=dataset["Gender"].unique(),
)

df_selection = dataset.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# MAIN PAGE
st.title(":bar_chart: Super Market Sales Dashboard")
st.markdown('##')

# TOP KPI
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
rating_score = ":star:"*int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales")
    st.subheader(f"US $ {total_sales:,}")

with middle_column:
    st.subheader("Average Rating")
    st.subheader(f"{average_rating} {rating_score}")

with right_column:
    st.subheader("Average Sale per Transaction")
    st.subheader(f"{average_sale_by_transaction}")

st.markdown("###")


# Sales by Product LIne(Bar_Chart)
sales_by_product_line = (
    dataset.groupby(by=["Product line"]).sum()[["Total"]].sort_values("Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation='h',
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"]*len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
# SALES BY HOUR
sales_by_hour = (
    dataset.groupby(by=["hour"]).sum()[["Total"]].sort_values("Total")
)
fig_hour_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    orientation='v',
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=["#0083B8"]*len(sales_by_hour),
    template="plotly_white",
)
fig_hour_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(tickmode="linear")),
    yaxis=(dict(showgrid=False))
)



left_column,right_column = st.columns(2)

left_column.plotly_chart(fig_product_sales,use_container_widht=True)
right_column.plotly_chart(fig_hour_sales,use_container_widht=True)
st.dataframe(df_selection)

### Custom CSS

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
