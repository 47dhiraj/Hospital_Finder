from geopy.distance import geodesic




## coordinate of Maitidevi seto pul

lat1 = 27.7030097
long1 = 85.3311939


## coordinate of Gaushala chowk

lat2 = 27.7078657
long2 = 85.3407783




## Pro/Advance Level


## Creating reusable functions/methods to calculate distance in desired unit/metric


## Example 1: cacluate distance in kilometers

def calculate_distance_in_km(latitude1, longitude1, latitude2, longitude2):
    
    coordinate1 = (latitude1, longitude1)

    coordinate2 = (latitude2, longitude2)

    return geodesic(coordinate1, coordinate2).kilometers



km = calculate_distance_in_km(lat1, long1, lat2, long2)             ## calling function calculate_distance_in_km(lat1, long1, lat2, long2)

print("\nDistance in kilometers: ", km)




## Example 2: Cacluate distance in miles

def calculate_distance_in_miles(latitude1, longitude1, latitude2, longitude2):
    
    coordinate1 = (latitude1, longitude1)

    coordinate2 = (latitude2, longitude2)

    return geodesic(coordinate1, coordinate2).miles


miles = calculate_distance_in_miles(lat1, long1, lat2, long2)

print("\nDistance in miles: ", miles)




## Example 3: Cacluate distance in meters

def calculate_distance_in_meters(latitude1, longitude1, latitude2, longitude2):
    
    coordinate1 = (latitude1, longitude1)

    coordinate2 = (latitude2, longitude2)

    return geodesic(coordinate1, coordinate2).meters



meters = calculate_distance_in_meters(lat1, long1, lat2, long2)

print("\nDistance in meters: ", meters, "\n")






# ## Beginners Level / Understanding

# ## coordinate --> (latitude, longitude)

# coordinate1 = (lat1, long1)            
# coordinate2 = (lat2, long2)         


# ## calculate geodesic (straight-line) distance

# distance_kilometers = geodesic(coordinate1, coordinate2).kilometers
# distance_meters = geodesic(coordinate1, coordinate2).meters
# distance_miles = geodesic(coordinate1, coordinate2).miles


# print("\n\nDistance in kilometers: ", distance_kilometers)
# print("\nDistance in meters: ", distance_meters)
# print("\nDistance in miles: ", distance_miles)
