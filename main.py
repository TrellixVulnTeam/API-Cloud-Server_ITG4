import requests
import socket
local_ip = socket.gethostbyname(socket.gethostname())
url = "http://" + local_ip + ":8000/"
weather =  requests.get(url + "weather").text
time = requests.get(url + "time").text
public_ip = requests.get(url + "ip_address/public").text
private_ip = requests.get(url + "ip_address/private").text
help = requests.get(url + "help").text
"""
data = {"weather":weather,
        "time":time,
        "public_ip":public_ip,
        "private_ip":private_ip,
        "help":help}
"""
print(weather)