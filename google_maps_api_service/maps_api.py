import requests
import json 


API_KEY = "AIzaSyCN6QFZnmu9OwRf9GV8XcgVPwHp5aXM-Sw"
address = "Maitidevi, Kathmandu, Nepal"

url = "https://maps.googleapis.com/maps/api/geocode/json"
params = {
    "address": address,
    "key": API_KEY
}

response = requests.get(url, params=params)
print('response: ', response)

data = response.json()
print('data: ', data)

if data["status"] == "OK":
    location = data["results"][0]["geometry"]["location"]
    print(f"Address: {address}")
    print(f"Latitude: {location['lat']}, Longitude: {location['lng']}")
else:
    print("Error:", data["status"])
