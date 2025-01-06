# Weather Forecast

visual application for Weather Forecast.<p>
brifly about the app:<br>
The countries are loaded from [API](https://documenter.getpostman.com/view/1134062/T1LJjU52). After selecting a country, the capital city is loaded from API. 
<br>you can enter another city for the selected country. If the entered city is valid (weather forecast was retrieved), 
it will be inserted to the local DB and will be added to the list of cities the next time you select that country.
<br>By clicking on the "Get Weather Forecast for..." button,  weather data for the selected city will be retrieved from [API](https://www.visualcrossing.com/weather-api).
<br>weather icons was taken from the weather API [Repo](https://github.com/visualcrossing/WeatherIcons).
<p>There are 3 views:
<ul>
<li>Extended weather data for the current day.</li>
<li>General weather data for the coming week.</li>
<li>Different graphs about the weather.</li>
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