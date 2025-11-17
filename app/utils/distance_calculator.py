from geopy.distance import geodesic



def calculate_distance_in_km(lat1, lon1, lat2, lon2):

    """
        Calculate distance in kilometers between two points (lat/lon).

        Returns float value of distance in KM.
    """

    if None in [lat1, lon1, lat2, lon2]:

        return float('inf')  # Treat missing coordinates as "infinitely far"
    
    
    coordinate1 = (lat1, lon1)

    coordinate2 = (lat2, lon2)
    

    return geodesic(coordinate1, coordinate2).kilometers

