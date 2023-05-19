import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_daily_df(df):
    daily_df = df.resample(rule='D', on='date').agg({
        "instant": "nunique",
        "count": "sum"
    })
    daily_df = daily_df.reset_index()
    daily_df.rename(columns={
        "instant": "order_count",
        "count": "revenue"
    }, inplace=True)
    
    return daily_df

def create_sum_items_df(df):
    sum_items_df = hour_df.groupby("casual").sum()
    return sum_items_df

def create_bytemp_df(df):
    bytemp_df = hour_df.groupby(by="temp").instant.nunique().reset_index()
    bytemp_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
    return bytemp_df

def create_byweather_df(df):
    byweather_df = hour_df.groupby(by="weather").instant.nunique().reset_index()
    byweather_df.rename(columns={
        "instant": "customer_count"
    }, inplace=True)
    
    return byweather_df

def create_rfm_df(df):
    rfm_df = hour_df.groupby(by="instant", as_index=False).agg({
        "date": "max", 
        "instant": "nunique",
        "count": "sum"
    })
    rfm_df.columns = ["instant", "frequency", "monetary"]
    
    return rfm_df
day_df = pd.read_csv("all_datadayagung.csv")
hour_df = pd.read_csv("all_datahouragung.csv")

datetime_columns = ["date", "date"]
hour_df.sort_values(by="date", inplace=True)
hour_df.reset_index(inplace=True)
 
for column in datetime_columns:
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date = hour_df["date"].min()
max_date = hour_df["date"].max()
 
with st.sidebar:
    
    st.image("https://media.istockphoto.com/id/1152337765/id/vektor/logo-untuk-penyewaan-sepeda-ilustrasi-vektor-pada-latar-belakang-putih.jpg?s=1024x1024&w=is&k=20&c=Lg_E5PxrTOW8NflTngPX71f81puEuRnRz-aYGxkpGEQ=")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df["date"] >= str(start_date)) & 
                (hour_df["date"] <= str(end_date))]

daily_df = create_daily_df(main_df)
sum_items_df = create_sum_items_df(main_df)
bytemp_df = create_bytemp_df(main_df)
byweather_df = create_byweather_df(main_df)
rfm_df = create_rfm_df(main_df)

st.header('Bicycle Rent :sparkles:')


st.subheader('TOTAL')
 
col1, col2, = st.columns(2)
 
with col1:
    total_orders = daily_df.order_count.sum()
    st.metric("Total Rent Hours", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_df.revenue.sum(), "TOTAL", locale='es_CO') 
    st.metric("Total Rent", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    hour_df["date"],
    hour_df["count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


st.set_option('deprecation.showPyplotGlobalUse', False)
sns.set_style('darkgrid')


fig, ax = plt.subplots(figsize=(15,10))
sns.lineplot(data=hour_df, x='hour', y='count', hue='weather', ax=ax)
ax.set(title="Jumlah Jam dari penggunaan sepeda berdasarkan cuaca")


st.pyplot(fig)

sewa_bulanan = pd.DataFrame({'month': [1,2,3,4,5,6,7,8,9,10,11,12], 'count': [134933, 151352, 228920, 269094, 331686, 346342, 344948, 351194, 345991, 322352, 254831, 211036]})

st.set_option('deprecation.showPyplotGlobalUse', False)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(sewa_bulanan['month'], sewa_bulanan['count'])
ax.set(title='Jumlah Jam Total Penyewaan Sepeda tiap Bulan', xlabel='Bulan', ylabel='Jumlah')
ax.set_xticks(ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

st.pyplot(fig)

st.caption('Copyright (c) Member Dicoding 2023')