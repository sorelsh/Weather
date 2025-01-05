import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from datetime import timedelta, timezone

from numpy.ma.extras import column_stack
from numpy.matlib import empty

import Api
import DbHelper
import Utils
from Api import get_weather

st.markdown("""
# Weather Forecast App
""")
st.session_state.country_selected = False
st.session_state.clicked = False

countries_data = Api.get_countries()

countries_dic = {}
cities = []
main_container = st.container()
cols= main_container.columns(2)
cols1 = main_container.columns(2)

countries_dic[""] = ""
for data in countries_data["data"]:
    countries_dic[data['name']] = data['iso2']

db = DbHelper.DbWheather(table="cities")
with main_container:
    selectedCountry = cols[0].selectbox(
                    'SELECT COUNTRY',
                    countries_dic)

    if selectedCountry !=  "":
        cities.append(Api.get_capital(selectedCountry))
        st.session_state.country_selected = True

    for city in db.retrieve(selectedCountry):
        cities.append(city[0])
    cities.append("Another option...")
    if st.session_state.country_selected:
        selectedCity = cols[1].selectbox(
                'SELECT CITY',
                cities)
            # Create text input for user entry
        if selectedCity == "Another option...":
            otherOption = cols1[1].text_input("Enter city name...")
            selectedCity = otherOption

        if st.button("Get Weather Forecast for {city}!".format(city=selectedCity)): #, on_click=Api.get_weather, args=(selectedCountry, selectedCity))
            cityWeather =  Api.get_weather(selectedCountry, selectedCity)
            st.session_state.clicked = True



if st.session_state.clicked and cityWeather and type(cityWeather) == dict:
    if selectedCity not in cities:
        db.insert(dict(country=selectedCountry, city=selectedCity))

    data = pd.json_normalize(cityWeather["days"])
    #convert fahrenheit_to_celsius
    data['temp_c'] = data.apply(lambda x: round(((x.temp - 32) * 0.5556), 1), axis=1)
    data['tempmax_c'] = data.apply(lambda x: Utils.fahrenheit_to_celsius(x.tempmax), axis=1)
    data['tempmin_c'] = data.apply(lambda x: Utils.fahrenheit_to_celsius(x.tempmin), axis=1)


    daily_container = st.container(border=True)
    with daily_container:
        today = data[data.datetime == dt.datetime.now().strftime("%Y-%m-%d")]
        st.write(today)
        st.markdown("""<h3> {city}, {state} </h3>""".format(city=selectedCity, state=selectedCountry), unsafe_allow_html=True)
        st.markdown("""<h4> {date_time} </h4>""".format(date_time=(dt.datetime.now(timezone.utc) +  timedelta(hours=cityWeather['tzoffset'])).strftime("%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)
        st.markdown("**{description}**".format(description=today['description'][0]))
        st.image("./images/{img_name}.png".format(img_name=today['icon'][0]))
        st.markdown("#  Temp: {val}".format(val=today['temp_c'][0]))
        st.markdown("* **sunrise: {val}**".format(val=today['sunrise'][0]))
        st.markdown("* **sunset: {val}**".format(val=today['sunset'][0]))
        st.markdown("* **humidity: {val}**".format(val=today['humidity'][0]))
        st.markdown("* **Max. Temp: {val}**".format(val=today['tempmax_c'][0]))
        st.markdown("* **Min. Temp: {val}**".format(val=today['tempmin_c'][0]))

    fig, ax = plt.subplots(figsize = (12,6))
    sns.lineplot(data=data, x='datetime', y='temp_c', ax=ax)

    myFmt = mdates.DateFormatter("%d/%m/%y")
    # ax.xaxis.set_major_formatter(myFmt)

    plt.grid(True, alpha=1)
    fig.autofmt_xdate(rotation=45)

    st.pyplot(fig)
elif st.session_state.clicked and selectedCity is not None:
    st.markdown("**:red[No information found for: {city_name}, check if the city name is correct]**".format(city_name=selectedCity))