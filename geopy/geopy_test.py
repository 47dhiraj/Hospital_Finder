from geopy.geocoders import Nominatim

address = "Kuleshwor, Kathmandu, Nepal"

geolocator = Nominatim(user_agent="Hospital_Finder (47schoolteaching@gmail.com)")

location = geolocator.geocode(address)

if location:
    print("Address:", address)
    print("Latitude:", location.latitude)
    print("Longitude:", location.longitude)
else:
    print("Location not found")



### Reverse way

latitude = location.latitude
longitude = location.longitude

geolocator = Nominatim(user_agent="Hospital_Finder (47schoolteaching@gmail.com)")

location = geolocator.reverse((latitude, longitude), language='en')

if location:
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("Address:", location.address)
else:
    print("Address not found")