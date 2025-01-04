import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from numpy.matlib import empty

import Api
import DbHelper
from Api import get_weather

st.markdown("""
# My App
* hello world!!!!
""")
st.session_state.country_selected = False
st.session_state.clicked = False

countries_data = Api.get_countries()

countries_dic = {}
cities = []

countries_dic[""] = ""
for data in countries_data["data"]:
    countries_dic[data['name']] = data['iso2']

db = DbHelper.DbWheather(table="cities")

selectedCountry = st.selectbox(
                'SELECT COUNTRY',
                countries_dic)

if selectedCountry !=  "":
    cities.append(Api.get_capital(selectedCountry))
    st.session_state.country_selected = True

for city in db.retrieve(selectedCountry):
    cities.append(city[0])
cities.append("Another option...")
if st.session_state.country_selected:
    selectedCity = st.selectbox(
            'SELECT CITY',
            cities)
        # Create text input for user entry
    if selectedCity == "Another option...":
        otherOption = st.text_input("Enter your other option...")
        selectedCity = otherOption

    if st.button("Get Weather for {city}!".format(city=selectedCity)): #, on_click=Api.get_weather, args=(selectedCountry, selectedCity))
        cityWeather =  Api.get_weather(selectedCountry, selectedCity)
        st.session_state.clicked = True

if st.session_state.clicked and cityWeather and type(cityWeather) == dict:
    if selectedCity not in cities:
        db.insert(dict(country=selectedCountry, city=selectedCity))

    data = pd.json_normalize(cityWeather["days"])
    data['temp_c'] = data.apply(lambda x: round(((x.temp - 32) * 0.5556), 1), axis=1)

    fig, ax = plt.subplots(figsize = (12,6))
    sns.lineplot(data=data, x='datetime', y='temp_c', ax=ax)

    myFmt = mdates.DateFormatter("%d/%m/%y")
    # ax.xaxis.set_major_formatter(myFmt)

    plt.grid(True, alpha=1)
    fig.autofmt_xdate(rotation=45)

    st.pyplot(fig)