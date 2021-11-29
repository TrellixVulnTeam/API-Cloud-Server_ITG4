from chalice import Chalice
import os
from datetime import datetime as dt
try:
    import requests
    from requests import get
except ImportError:
    os.system('python -m pip install requests')
app = Chalice(app_name='Cloud_Server')
@app.route('/')
def index():
    return "Jarvis API"

@app.route('/time')
def getTime(): 
    now = dt.now()
    currentTime = now.strftime('%H:%M:%S')
    return currentTime
@app.route('/ip_address/private')
def private():
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    return ip
@app.route('/ip_address/public')
def public():
    ip = get('https://api.ipify.org').text
    return ip
@app.route('/weather')
def weather(): 
    api_key = "90e19536df9f0408dfc9f39e73a0ff89"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    from datetime import date
    import geoip2.database
    Ip = public()
    with geoip2.database.Reader('GeoLite2-City_20210105/GeoLite2-City.mmdb') as reader:
        ip_address_location = reader.city(Ip)
        ip_rasa = ip_address_location.city.name
        city_name = ip_rasa
        complete_url = base_url + "appid=" + api_key + "&q=" + str(city_name)
        response = get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            round(current_temperature, 2)
            Temperature = current_temperature - 273
            Temperature = int(Temperature)
            current_pressure = current_pressure * 0.75
            data = "City: " + city_name + "\n" + "Temperature: " + str(Temperature) + " C" + "\n" + "Pressure: " + str(current_pressure) + " mmHg" + "\n" + "Humidity: "  + str(current_humidiy) + "%"+ "\n" + "Weather Description: " + weather_description
            return data
@app.route('/help')
def help():
    data = "1. Weather(" + private() + ":8000/ip_address/private) \n2.Time(" + private() + ":8000/time)" + "\n" + "3.Public IP Address(IPv4)(" + private() + ":8000/ip_address/public" + "\n" + "4.Private IP Address(" + private() + ":8000/ip_address/private" + "\n" + "More to be added soon, be in touch..."
    return data
