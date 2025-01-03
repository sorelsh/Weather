from dotenv import dotenv_values
import requests
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px


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


fig, ax = plt.subplots(figsize = (12,6))
sns.lineplot(data=data, x='datetime', y='temp', ax=ax)

myFmt = mdates.DateFormatter("%d-%m")
ax.xaxis.set_major_formatter(myFmt)

plt.grid(True, alpha=1)
fig.autofmt_xdate(rotation=45)

st.pyplot(fig)


# Convert the DataFrame to a Plotly-friendly format
interactive_data = data.reset_index()

# Create an interactive time series plot
fig = px.line(interactive_data, x='datetime', y='temp', title='Interactive Temperature Over Time')
st.pyplot(fig)