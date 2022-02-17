from geopy.geocoders import Nominatim
from sql_db import *
import random
from flask import Flask, request, jsonify

def map_coordinates(address):
    geolocator = Nominatim(user_agent="example app")
    location = geolocator.geocode(address)
    address_data = {}
    if location is not None:
        log().info("able to get coordinates for the given address")
        latitude = location.latitude  
        longitude = location.longitude
        address_data['ad_id'] = random.randint(10000, 99999)
        address_data['address_detail'] = str(address)
        address_data['latitude'] = str(latitude)
        address_data['longitude'] = str(longitude)

    return address_data
    


         
