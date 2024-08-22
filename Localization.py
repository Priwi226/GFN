#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:26:09 2024

@author: priwi
"""

import requests
from geopy.distance import geodesic
import anmeldung

def get_geolocation():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        location = data['loc'].split(',')
        latitude = float(location[0])
        longitude = float(location[1])
    except Exception as e:
        print(f"Error getting geolocation: {e}")
        return None, None, None

    # Assuming anmeldung.standort_p is a tuple (latitude, longitude)
    your_location = anmeldung.standort_p  
    current_location = (latitude, longitude)

    if not all([latitude, longitude, your_location]):
        return None, None, None

    distance = geodesic(your_location, current_location).kilometers
    tolerance_km = 5  # Tolerancia v kilometroch

    if distance < tolerance_km:
        print(f"Du bist bei den GFN Standort:\nDeine GPS: {latitude}, {longitude}")
        standort = 1
    else:
        print(f"Du bist nicht Bein dem GFN Standort:\nDeine GPS: {latitude}, {longitude}.\nReichwete: {distance:.2f} km")
        standort = 0

    # print (f"Standort = {standort}")
    return latitude, longitude, standort

# latitude, longitude, standort = get_geolocation()

