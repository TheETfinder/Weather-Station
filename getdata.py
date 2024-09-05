import json


# Opening the Stock Data File and loading it  
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
 
    current_temperatur = temperatur["13"]

    print("The current Temperatur at 1 p.m is", current_temperatur)

   # current_price_json = current_price.to_json()

    with open('searche_data.json', 'w') as data:
        json.dump(current_price, data)

    with open('weather.json', 'w') as data:
        json.dump(current_temperatur, data)


