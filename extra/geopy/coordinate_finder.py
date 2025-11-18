from geopy.geocoders import Nominatim

from geopy.exc import GeocoderTimedOut, GeocoderServiceError




## Pro/Advance Level


# creating global geolocator

geolocator = Nominatim(

    user_agent="Hospital_Finder",

    timeout=10

)



address = "Kuleshwor, Kathmandu, Nepal"




## function/method to find coordinates from the given address
## (Forward Geocoding)

def geocode_address(address: str):

    """Convert address → latitude/longitude (optimized)."""

    try:

        location = geolocator.geocode(address)

        if not location:
            return None
        
        return {
            "address": address,
            "lat": location.latitude,
            "lng": location.longitude
        }

    except (GeocoderTimedOut, GeocoderServiceError) as e:

        print("Geocoding Error:", e)

        return None




## function/method to find full address from the given coordinates
## (Reverse Geocoding)

def reverse_geocode(lat: float, lng: float):

    """Convert lat/lng → human-readable address (optimized)."""

    try:

        location = geolocator.reverse((lat, lng), language='en')

        if not location:
            return None
        
        return {
            "lat": lat,
            "lng": lng,
            "address": location.address
        }

    except (GeocoderTimedOut, GeocoderServiceError) as e:

        print("Reverse Geocoding Error:", e)

        return None






geo = geocode_address(address)


if geo:

    print("\nFinding coordinate of the given address: \n")

    print("Address:", geo["address"])

    print("\nLatitude:", geo["lat"])

    print("Longitude:", geo["lng"])

else:

    print("Location not found")





if geo:

    rev = reverse_geocode(geo["lat"], geo["lng"])

    if rev:

        print("\n\nFinding full address of the given coordinate: \n")

        print("Latitude:", rev["lat"])

        print("Longitude:", rev["lng"])

        print("\nAddress:", rev["address"])

    else:
        
        print("Address not found")














# ## Beginners Level

# address = "Kuleshwor, Kathmandu, Nepal"

# geolocator = Nominatim(user_agent="Hospital_Finder (47schoolteaching@gmail.com)")


# location = geolocator.geocode(address)


# if location:

#     print("Address:", address)
#     print("Latitude:", location.latitude)
#     print("Longitude:", location.longitude)

# else:
#     print("Location not found")

