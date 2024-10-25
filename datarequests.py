import openmeteo_requests
import yfinance as yf
import requests_cache
import pandas as pd
from retry_requests import retry
import json
from datetime import datetime

current_time = datetime.now()

print(current_time.time())

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 52.520064,
	"longitude": 13.404772, 
	"current": "temperature_2m",
	"hourly": ["temperature_2m", "rain", "wind_speed_10m"],
	"forecast_days": 2
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()

print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_rain = hourly.Variables(1).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["rain"] = hourly_rain
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)



# Inizialising the Stock we want the info for
msft = yf.Ticker("MSFT")
# Pulling the data
info = msft.info
# print(msft)
print(info)

# Dumping the Data in JSON files
with open('data.json', 'w') as f:
    json.dump(info, f)

print(hourly_dataframe)

hourly_dataframe = hourly_dataframe.to_json()

with open('wetter.json', 'w') as f:
    f.write(hourly_dataframe)

print(hourly_dataframe)

with open('data.json', mode= "r", encoding="utf-8") as stock:
    stock_data = json.load(stock)

# Getting the Current Price
current_price = stock_data["currentPrice"]

# Printing the Current Price
print("The current stock price for MSFT is", current_price, "USD")
# Opening the Weather Data File and loading it  
with open('wetter.json',mode="r", encoding="utf-8") as weather:
    weather_data = json.load(weather)

# Getting the Current Temperatur
    temperatur = weather_data["temperature_2m"]
 
    current_temperatur = temperatur["22"]

    print("The current Temperatur at 5 p.m is", current_temperatur)
    

    rain = weather_data["rain"]
 
    current_rain = rain["22"]

    print("The Rain at 5 p.m is", current_rain)
   # current_price_json = current_price.to_json()

    with open('searche_data.json', 'w') as data:
        json.dump(current_price, data)

    with open('weather.json', 'w') as data:
        json.dump(current_temperatur, data)



