import openmeteo_requests
import yfinance as yf
import requests_cache
import pandas as pd
from retry_requests import retry
import json
from datetime import datetime
import time
import requests
import xmltodict, json
import xml.etree.ElementTree as ET

#Getting the current time
current_time = datetime.now()

print(current_time.time())



    # Open-Meteo

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 49.003974,
	"longitude": 8.370159, 
	"current": "temperature_2m",
	"hourly": ["temperature_2m", "rain", "wind_speed_10m"],
	"forecast_days": 2
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()

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

hourly_dataframe = hourly_dataframe.to_json()

with open('wetter.json', 'w') as f:
    f.write(hourly_dataframe)



    #Yahoo Finance

# Inizialising the Stock we want the info for
msft = yf.Ticker("MSFT")
# Pulling the data
info = msft.info


#annoyingly reimporting the data to parse it as a JSON :I

with open('stock.json','w') as file:
     json.dump(info, file)

with open('stock.json', mode= "r", encoding="utf-8") as stock:
    stock_data = json.load(stock)

# Getting the Current Price
current_price = stock_data["currentPrice"]




#Trias

# api-endpoint
URL = "https://projekte.kvv-efa.de/mangangtrias/trias"

time_now = time.strftime("%Y-%m-%dT%H:%M:%S")
day = time.strftime("%Y-%m-%dT")

time_fix = time_now.replace("T", "")
time = time_fix.replace("Z", "")

print(time_now)

with open('kvv.xml', 'r') as file:
     mydata = file.read()

data_modified = mydata.replace('timenow',time_now)

headers = {'Content-Type': 'application/xml'} # set what your server accepts
answer = requests.post(url= URL, data=data_modified, headers=headers).text

data = json.dumps(xmltodict.parse(answer))

fix = data.replace('trias:','')

with open('test.json','w') as a:
	a.write(fix)

with open('test.json','r') as l:
	tri = json.load(l)

trias = tri["Trias"]

StopEventResult = trias["ServiceDelivery"]["DeliveryPayload"]["StopEventResponse"]["StopEventResult"]

with open('trias.json', 'w', encoding="utf-8") as trias_json:
     json.dump(StopEventResult, trias_json)

with open('trias.json', 'r', encoding="unicode-escape") as trias_json_load:
    trip = json.load(trias_json_load)



#Printing

# Printing the Current Price
print("The current stock price for MSFT is", current_price, "USD")

# Open-Meteo

# Getting the Current Temperatur

with open('wetter.json',mode="r", encoding="utf-8") as weather:
    weather_data = json.load(weather)

temperatur = weather_data["temperature_2m"]
 
current_temperatur = temperatur["22"]

print("The current Temperatur at 10 p.m is", current_temperatur)
    

rain = weather_data["rain"]
 
current_rain = rain["22"]

print("The Rain at 10 p.m is", current_rain)
   # current_price_json = current_price.to_json()


# Trias

for i in trip :

    Trip_name = i["StopEvent"]["Service"]["ServiceSection"]["PublishedLineName"]["Text"]
    text_line = Trip_name.encode('latin1').decode('utf8')

    Trip_time = i["StopEvent"]["ThisCall"]["CallAtStop"]["ServiceDeparture"]["TimetabledTime"]
    text_time = Trip_time.encode('latin1').decode('utf8')

    Trip_dest = i["StopEvent"]["Service"]["DestinationText"]["Text"]
    text_dest = Trip_dest.encode('latin1').decode('utf8')

    trias_time = text_time.replace("Z","")
    arr_time = trias_time.replace("T", "")
    arr = text_time.replace(day, "")
    time_arr = arr.replace("Z", "")
    #print(arr_time)
#    dt = datetime.strptime(arr_time, "%a, %d %b %Y %H:%M:%S")
#    datetime = datetime.datetime-strptime(time,"%Y-%m-%d%H:%M:%S")

#    print(dt)
#    print(datetime)

    trias_result = "Linie:" + " "+ text_line + " " +"Nach"+ " "+ text_dest + " " +"Abfahrt:" + " "+ time_arr

    print(trias_result)

print("Request done")