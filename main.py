import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import Api
import DbHelper
import Utils


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
    data['temp_c'] = data.apply(lambda x: int(((x.temp - 32) * 0.5556)), axis=1)
    data['tempmax_c'] = data.apply(lambda x: Utils.fahrenheit_to_celsius(x.tempmax), axis=1)
    data['tempmin_c'] = data.apply(lambda x: Utils.fahrenheit_to_celsius(x.tempmin), axis=1)



    daily_container = st.expander("view today forecast",expanded=True)
    Utils.today_weather(daily_container, data, cityWeather, selectedCity, selectedCountry)

    weekly_container = st.expander("view weekly forecast", expanded=False)
    day1_container = weekly_container.container(border=True)
    day2_container = weekly_container.container(border=True)
    day3_container = weekly_container.container(border=True)
    day4_container = weekly_container.container(border=True)
    day5_container = weekly_container.container(border=True)
    day6_container = weekly_container.container(border=True)
    day7_container = weekly_container.container(border=True)

    with weekly_container:
        Utils.daily_weather(day1_container, data, 0)
        Utils.daily_weather(day2_container, data, 1)
        Utils.daily_weather(day3_container, data, 2)
        Utils.daily_weather(day4_container, data, 3)
        Utils.daily_weather(day5_container, data, 4)
        Utils.daily_weather(day6_container, data, 5)
        Utils.daily_weather(day7_container, data, 6)

    graphs_container = st.expander("general graphs for next 15 days",expanded=False)
    with graphs_container:
        fig1, ax1 = plt.subplots(figsize = (12,6))
        sns.barplot(data=data, x='datetime', y=data[['tempmax_c','tempmin_c']].mean(axis=1), ax=ax1).set(xlabel='date', ylabel='mean Temperature \u2103')
        myFmt = mdates.DateFormatter("%d/%m/%y")
        plt.grid(True, alpha=1)
        fig1.autofmt_xdate(rotation=45)
        st.pyplot(fig1)

        fig2, ax3 = plt.subplots(figsize = (12,6))
        sns.histplot(data=data, x='conditions', hue='conditions', ax=ax3)
        st.pyplot(fig2)

        fig3, ax2 = plt.subplots(figsize = (12,6))
        sns.scatterplot(data=data, x='tempmin_c', y='tempmax_c', hue='conditions', ax=ax2).set(title='Minimum vs Maximum Temperature \u2103', xlabel='Minimum Temperature \u2103', ylabel='Maximum Temperature \u2103')
        st.pyplot(fig3)

elif st.session_state.clicked and selectedCity is not None:
    st.markdown("**:red[No information found for: {city_name}, check if the city name is correct]**".format(city_name=selectedCity))