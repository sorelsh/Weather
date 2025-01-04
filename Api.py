import requests
import streamlit as st
from dotenv import dotenv_values



def get_weather(country, city):
    api_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={YOUR_API_KEY}"
    #st.write(api_url.format(YOUR_API_KEY=st.secrets["API_KEY"]))
    #secrets = dotenv_values(".env")
    response = requests.get(api_url.format(location=city+","+country, YOUR_API_KEY=st.secrets["API_KEY"]))
    if response.status_code == 200:
        return response.json()
    else:
        return "Error on calling weather Api, return code: " + str(response.status_code)

def get_countries():
    response = requests.get("https://countriesnow.space/api/v0.1/countries/states")
    if response.status_code == 200:
        return response.json()
    else:
        return "Error on calling countries Api, return code: " + str(response.status_code)

def get_capital(country):
    myobj = {"country": country}
    capital_url = "https://countriesnow.space/api/v0.1/countries/capital"
    response = requests.post(capital_url, json=myobj)
    if response.status_code == 200:
        return response.json()["data"]["capital"]
    else:
        return "Error on calling capital Api, return code: " + str(response.status_code)
