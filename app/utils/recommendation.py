from app.models import Disease
from app.models import Surg
from app.models import Patient
from app.models import Hospital
from app.models import Rate
from app.models import District

from .distance_calculator_haversine import calculate_distance_with_haversine

# from .distance_calculator_geopy import calculate_distance_in_km_with_geopy






## Project Utilities Functions here ...


def recommendations_by_disease(disease):

    hospitals = disease.hospitals.all()

    # print('\n\nDisease Recommended Hospitals: ', hospitals)

    return list(hospitals)






def recommendations_by_surgery(surgery):

    hospitals = surgery.hospitals.all()

    # print('\n\nSurgery Recommended Hospitals: ', hospitals)

    return list(hospitals)






def recommendation_by_distance(hospitals, patient_latitude, patient_longitude):

    """
        Sort hospitals based on distance to patient.
    """

    if not hospitals:
        return []


    hospital_distances = []

    for hospital in hospitals:

        ## To calculate distance using Haversine Algorith / Formula
        distance = calculate_distance_with_haversine(
            patient_latitude,
            patient_longitude,
            hospital.latitude,
            hospital.longitude,
            unit="km"
        )


        ## To calculate distance using geopy
        # distance = calculate_distance_in_km_with_geopy(
        #     patient_latitude,
        #     patient_longitude,
        #     hospital.latitude,
        #     hospital.longitude
        # )

        # print('\nDistance: ', distance, ' Type; ', type(distance))

        ## making hospital_distances a list of tuples e.g (hospital_1, 10)
        hospital_distances.append((hospital, distance))

    

    hospital_distances.sort(key = lambda item: item[1])                         # item[0] represent single hospital_object and item[1] is a distance from patient to that paritcular hospital.


    return [hospital_ojects[0] for hospital_ojects in hospital_distances]       # Return sorted hospital objects

