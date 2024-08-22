import json


# Opening the Stock Data File and loading it  
with open('data.json', mode= "r", encoding="utf-8") as stock:
    stock_data = json.load(stock)

# Getting the Current Price
current_price = stock_data["currentPrice"]

# Printing the Current Price
print(current_price)

# Opening the Weather Data File and loading it 
with open('wetter.json',mode="r", encoding="utf-8") as weather:
    weather_data = json.load(weather)

# Getting the Current Temperatur
    current_temperatur = weather_data["1"]

    print(current_temperatur)

