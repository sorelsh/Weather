from dotenv import dotenv_values
import requests
import pandas as pd
import streamlit as st

st.markdown("""
# My App
* hello world!!!!
""")

secrets = dotenv_values(".env")
api_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/London,UK?key={YOUR_API_KEY}"
st.write(api_url.format(YOUR_API_KEY=st.secrets["API_KEY"]))
response = requests.get(api_url.format(YOUR_API_KEY=st.secrets["API_KEY"]))
if response.status_code == 200:
    weather_data = response.json()
    data = pd.json_normalize(weather_data["days"])
else:
    st.write("API call failed")

