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





def extract_lat_lng(response: dict):

    """Safely extract lat/lng from geocode_address() response."""

    data = response.get("data", {})

    return data.get("lat"), data.get("lng")

