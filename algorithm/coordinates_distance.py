
# import math


# def haversine(lat1, lon1, lat2, lon2):

#     R = 6371  

#     lat1_rad = math.radians(lat1)
#     lon1_rad = math.radians(lon1)
#     lat2_rad = math.radians(lat2)
#     lon2_rad = math.radians(lon2)

#     dlat = lat2_rad - lat1_rad
#     dlon = lon2_rad - lon1_rad

#     a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

#     distance = R * c

#     return distance

# # Coordinates of Gaushala and Putalisadak

# gaushala_lat = 27.7094546       
# gaushala_lon = 85.3408835   

# putalisadak_lat = 27.7031974    
# putalisadak_lon = 85.320079    


# distance = haversine(putalisadak_lat, putalisadak_lon, gaushala_lat, gaushala_lon)


# print("Air distance : ", distance, "KM")




import math

def haversine(lat1, lon1, lat2, lon2):

    # Converting coordinates (latitude and longitude) from Degree to Radian
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # HAVERSINE Formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Earth's radius in kilometers
    R = 6371.0
    
    # Distance in kilometers
    distance = R * c
    
    return distance


# Kathmandu Example:

lat1, lon1 = 28.2296976, 83.8740449 # Pokhara, Nepal
lat2, lon2 = 27.5060061, 83.4149658 # Bhairahawa (Gautam Buddha International Airport), Nepal

# Air Distance calculation
distance = haversine(lat1, lon1, lat2, lon2)


print(f"Air Distance: {distance} KM")
