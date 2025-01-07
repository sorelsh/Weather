# Weather Forecast

visual streamlit application for Weather Forecast.<p>
<b>About the App:</b>
<br>The app loads a list of countries from an [API](https://documenter.getpostman.com/view/1134062/T1LJjU52). After selecting a country, the capital city is fetched from the same API.
You can also enter a different city for the selected country. If the city is valid (i.e., its weather forecast is successfully retrieved), it will be saved to a local database and included in the city list the next time you select that country.

By clicking the "Get Weather Forecast for..." button, weather data for the chosen city is retrieved from the Visual Crossing Weather [API](https://www.visualcrossing.com/weather-api). 
<br>Weather icons are sourced from the API [GitHub repository](https://github.com/visualcrossing/WeatherIcons).

The app features three views:
<ul>
<li>Extended weather data for the current day.</li>
<li>General weather data for the coming week.</li>
<li>General graphs on next 15 days weather.</li>
</ul>

## Installation

Use <b>"poetry install"</b> to install Weather Forecast dependencies.

```bash
poetry install
```

## Usage
[my App on streamlit](https://weather-jsbjg4hew5nzw4op7pjvby.streamlit.app/)


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[Sorel sneier](https://github.com/sorelsh)