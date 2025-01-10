import datetime as dt
from datetime import timedelta, timezone, datetime

def fahrenheit_to_celsius(fahrenheit:str):
    return int((float(fahrenheit) - 32) * 5 / 9)

def today_weather(daily_container, data, cityWeather, selectedCity, selectedCountry):
    with daily_container:
        cols = daily_container.columns(1)
        col1 = daily_container.columns(2)
        col2 = daily_container.columns(2)
        col3 = daily_container.columns(2)
        col4 = daily_container.columns(2)
        col5 = daily_container.columns(2)
        col6 = daily_container.columns(2)
        col7 = daily_container.columns(2)

        today = data.iloc[0].to_frame().T
        cols[0].write(today)
        cols[0].markdown("""<h3> {city}, {state} </h3>""".format(city=selectedCity, state=selectedCountry),
                    unsafe_allow_html=True)
        col2[0].markdown("""<h4> {date_time} </h4>""".format(
            date_time=(dt.datetime.now(timezone.utc) + timedelta(hours=cityWeather['tzoffset'])).strftime(
                "%d/%m/%Y %H:%M:%S")), unsafe_allow_html=True)
        col3[0].markdown("**{description}**".format(description=today['description'][0]))
        col4[0].image("./images/{img_name}.png".format(img_name=today['icon'][0]))
        col4[1].markdown("#  Temp: {val}\u2103".format(val=today['temp_c'][0]))
        col5[0].markdown("* **sunrise: {val}**".format(val=":".join(today['sunrise'][0].split(":")[:2])))
        col5[1].markdown("* **sunset: {val}**".format(val=":".join(today['sunset'][0].split(":")[:2])))
        col6[0].markdown("* **humidity: {val}**".format(val=today['humidity'][0]))
        col6[1].markdown("* **uv index: {val}**".format(val=int(today['uvindex'][0])))
        col7[0].markdown("* **Max. Temp: {val}\u2103**".format(val=today['tempmax_c'][0]))
        col7[1].markdown("* **Min. Temp: {val}\u2103**".format(val=today['tempmin_c'][0]))

def daily_weather(daily_container, data, day_num):
    global colsW, colsW1
    with daily_container:
        colsW = daily_container.columns(3)
        colsW1 = daily_container.columns(3)
        colsW[0].markdown(
            "{date_time}".format(date_time=datetime.strptime(data.iloc[day_num]['datetime'], '%Y-%m-%d').strftime("%d-%m")))
        colsW[1].markdown("**{conditions}**".format(conditions=data.iloc[day_num]['conditions']))
        colsW1[0].image("./images/{img_name}.png".format(img_name=data.iloc[day_num]['icon']))
        colsW1[1].markdown("**humidity: {val}**".format(val=data.iloc[day_num]['humidity']))
        colsW[2].markdown("**Max. Temp: {val}\u2103**".format(val=data.iloc[day_num]['tempmax_c']))
        colsW1[2].markdown("**Min. Temp: {val}\u2103**".format(val=data.iloc[day_num]['tempmin_c']))