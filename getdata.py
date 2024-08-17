import json

with open('data.json', mode= "r", encoding="utf-8") as stock:
    stock_data = json.load(stock)


current_price = stock_data["currentPrice"]

print(current_price)


with open('wetter.json',mode="r", encoding="utf-8") as weather:
    weather_data = json.load(weather)

   ## current_weather = weather_data["1"]

## print(current_weather)

