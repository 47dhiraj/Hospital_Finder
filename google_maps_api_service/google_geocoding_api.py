import requests

## your google Geocoding API Key here ....
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"


def get_lat_lon_from_address(address):

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return {
            "address": data["results"][0]["formatted_address"],
            "lat": location["lat"],
            "lng": location["lng"]
        }
    else:
        return None




# Example use
address = "Kuleshwor, Kathmandu, Nepal"

result = get_lat_lon_from_address(address)


if result:
    
    print("Input Address:", address)
    print("Formatted Address:", result["address"])
    print("Latitude:", result["lat"])
    print("Longitude:", result["lng"])

else:

    print("Location not found")
