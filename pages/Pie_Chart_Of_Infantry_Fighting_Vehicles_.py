from streamlit_folium import folium_static

import streamlit as st
import json
import pandas as pd

st.title('Russia Losses Dashboard')

with st.spinner('Loading data...'):
    data = json.load(open('user_uploaded_files/russia_losses.json'))

df = pd.DataFrame(data['losses'])
if 'geo' in df.columns:
    df['geo'] = df['geo'].apply(lambda x: pd.NA if x is None or x == 'null' or x == '' else x)
df = df[df['type'] == 'Infantry fighting vehicles']

st.subheader('Infantry Fighting Vehicles Losses by Date')
pie_chart_data = df['date'].value_counts()
st.plotly_chart({'data': [{'values': list(pie_chart_data.values), 'labels': list(pie_chart_data.index), 'type': 'pie'}]})

st.subheader('Data')
st.dataframe(df)
