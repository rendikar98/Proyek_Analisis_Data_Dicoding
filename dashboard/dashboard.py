"""
Author: Rendika Rahmaturrizki
Date: 05/03/2024
This is the dashboard.py module.
Usage:
- This module is used to create a dashboard for the air quality data.
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    try:
        # # Print current directory for debugging
        # st.write("Current directory:", os.getcwd())

        # # List files in the directory for debugging
        # st.write("Files in directory:", os.listdir())

        # Load data
        #file_path = "./main_data.csv"
        file_path = "dashboard/main_data.csv"
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("Failed to load data. File not found.")
        return None

def pm25_dist(data):
    data['year'] = pd.Categorical(data['year'])
    return data.groupby('year').agg({'PM2.5': 'mean'}).reset_index()

def feature_dist(data):
    features = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    total = data[features].sum().sum()
    return data[features].sum() / total

st.set_page_config(
    page_title = "Air Quality Analysis",
    layout = "wide",
)

# Load the cleaned data
main_data = load_data()
main_data.head()

# Center-align the title
st.markdown("<h1  style='text-align: center;'>Air Quality Analysis</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


pm25_dist = pm25_dist(main_data)
feature_dist = feature_dist(main_data)

with st.container():    
    st.subheader('PM2.5 distribution from 2013 until 2017')
    st.markdown('<hr>', unsafe_allow_html=True)
    chart1 = plt.figure(figsize=(8,4), facecolor='w')
    pm25_dist.plot(x='year', y='PM2.5', kind='line', color='skyblue', marker='o', ax=chart1.gca())
    # Customize the plot
    plt.title('Air Quality (2013 - 2017)')
    plt.xlabel('Year', color='w')
    plt.ylabel('PM2.5')
    plt.xticks(range(len(pm25_dist['year'].unique())), pm25_dist['year'].unique(), rotation=45)
    plt.grid(True)
    # Show plot
    # plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    st.pyplot(chart1)
    
    st.write("""
                **Analisis:**
                Berdasarkan hasil visualisasi yang sudah 
                saya buat untuk component PM2.5, didapatkan bahwa 
                jumlah komponen PM2.5 paling banyak ada pada tahun 2017. 
                Berdasarkan catatan dan beberapa literatur yang sudah saya baca, 
                PM2.5 mempengaruhi kualitas udara pada suatu daerah. PM2.5 adalah partikel 
                yang sangat halus dengan diameter lebih kecil dari 2.5 mikron (mikrometer). 
                Jadi kualitas Udara paling baik berada pada tahun 2017
            """)

with st.container():    
    st.subheader('Air Component Distribution in Station Guanyuan')
    st.markdown('<hr>', unsafe_allow_html=True)
    chart2 = plt.figure(figsize=(8,4))
    # Assuming feature_dist now returns a DataFrame with a 'proportions' column
    plt.pie(feature_dist, labels=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'], autopct='%1.1f%%', startangle=90)
    # Customize the plot
    plt.axis('equal')
    plt.title('Feature Distribution')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    st.pyplot(chart2)

    st.write("""
                **Analisis:**
                Berdasarkan hasil visualisasi yang sudah buat dengan 
                pie chart didapatkan jawabannya, bahwa komponen udara 
                yang paling banyak di daerah Guanyuan adalah CO, 
                sedangkan perbandingan komponen CO dengan komponen yang lainnya 
                sangatlah jauh. Jumlah paling sedikit berada pada komponen SO2
            """)

