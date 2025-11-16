import requests
import json


def geocode_address(address):

    api_key = 'AIzaSyCN6QFZnmu9OwRf9GV8XcgVPwHp5aXM-Sw'

    # api_key = 'your_billing_enabled_api_key_here'

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    
    params = {
        'address': address, 
        'key': api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        print('Response: ', response)

        data = response.json()
        print('Data: ', data)

        if data['status'] == 'OK':

            location = data['results'][0]['geometry']['location']

            print(f"Latitude: {location['lat']}")

            print(f"Longitude: {location['lng']}")

            return location
        
        else:
            print(f"Geocoding failed: {data['status']}")
            
            return None
            

    except requests.exceptions.RequestException as e:

        print(f"Error: {e}")
        return None




# Use Case (Usage)
geocode_address('Maitidevi, Kathmandu, Nepal')



