from geopy.geocoders import Nominatim

from geopy.exc import GeocoderTimedOut, GeocoderServiceError



# creating global geolocator

geolocator = Nominatim(

    user_agent="Hospital_Finder",

    timeout=15

)




## function/method to find coordinates from the provided address
## (Forward Geocoding)


def geocode_address(address: str):

    """Convert address → latitude/longitude (optimized)."""

    try:

        location = geolocator.geocode(address)

        if not location:

            return {
                "status": "error",
                "message": "coordinates not found",
                "data": {
                    "address": address,
                    "lat": None,
                    "lng": None
                }
            }
        

        return {
            "status": "success",
            "message": "coordinates found",
            "data": {
                "address": address,
                "lat": location.latitude,
                "lng": location.longitude
            }
        }


    except (GeocoderTimedOut, GeocoderServiceError) as e:

        return {
            "status": "error",
            "message": "coordinates not found",
            "data": {
                "address": address,
                "lat": None,
                "lng": None
            }
        }






## calling geocode_address() function to test the geopy

# address = "Kuleshwor, Kathmandu, Nepal"
# response = geocode_address(address)
# print(response)


## Response Example

# {
#     'status': 'success', 
#     'message': 'coordinates found', 
#     'data': {
#         'address': 'Kuleshwor, Kathmandu, Nepal', 
#         'lat': 27.6910608, 
#         'lng': 85.3002049
#     }
# }
