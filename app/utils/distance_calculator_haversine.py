import math
from typing import Union
from decimal import Decimal


def calculate_distance_with_haversine(
    lat1: Union[float, str, Decimal], 
    lon1: Union[float, str, Decimal],
    lat2: Union[float, str, Decimal], 
    lon2: Union[float, str, Decimal],
    unit: str = "km"
) -> float:
    

    """
        Calculate the great-circle distance between two points on the Earth using the Haversine formula.

        Parameters:
            lat1, lon1: Latitude and Longitude of point 1 (float, decimal, or string)
            lat2, lon2: Latitude and Longitude of point 2 (float, decimal, or string)
            unit: 'km' for kilometers (default), 'mi' for miles

        Returns:
            Distance between the two points in the specified unit as a float
    """


    # Convert all inputs to float safely
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    # Earth radius
    R_km = 6371.0  # kilometers
    R_mi = 3958.8  # miles
    R = R_km if unit == "km" else R_mi

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return float(distance)










## Example 2

# import math


# def calculate_distance_in_km_with_haversine(lat1, lon1, lat2, lon2):

#     """
#         Calculate the great-circle distance between two points on the Earth using the Haversine formula.

#         Parameters:
#             lat1, lon1: Latitude and Longitude of point 1 (decimal or float)
#             lat2, lon2: Latitude and Longitude of point 2 (decimal or float)

#         Returns:
#             Distance in kilometers as a float

#     """

#     lat1 = float(lat1)
#     lon1 = float(lon1)
#     lat2 = float(lat2)
#     lon2 = float(lon2)


#     # Radius of the Earth in kilometers
#     R = 6371.0  

#     # Converting degrees to radians
#     lat1_rad = math.radians(lat1)
#     lon1_rad = math.radians(lon1)
#     lat2_rad = math.radians(lat2)
#     lon2_rad = math.radians(lon2)

#     # Differences
#     dlat = lat2_rad - lat1_rad
#     dlon = lon2_rad - lon1_rad

#     # Haversine formula
#     a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

#     distance = R * c

#     return float(distance)

