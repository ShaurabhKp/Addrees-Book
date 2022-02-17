from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
import requests
from geopy.geocoders import Nominatim
import random
from sql_db import *
from map_address import *
import logger
from logger import *


app = Flask(__name__)
api = Api(app)

class Address(Resource):
    
    def get(self,ad_id = None):
        log().info('Get method is called')
        if ad_id is None:
            return jsonify(get_address())
        else:
            log().info('%s %s','Ad id is',str(ad_id))
            return jsonify(get_address_by_id(ad_id))

    def post(self,ad_id = None):
        data = request.get_json()
        log().info('%s %s','Post method is called. Payload is ',str(data))
        address = data["address"]
        address = address.strip()
        if(address != ''):
            address_data =  map_coordinates(address)
            if address_data == {}:
                log().error("Could not find cordinates of the address")
                return jsonify({"error_message":"Could not find cordinates of the address, please check and provide and again with some other reference"})
            else:
                log().info("Inserting data into DB")
                return jsonify(insert_address(address_data))
        else:
            log().info("Address field should is sent as empty")
            return jsonify({"message": "Address field should not be sent as empty"})

    def put(self, ad_id):
        log().info('Put method is called')
        check_id_exists = get_address_by_id(ad_id)
        if check_id_exists == {}:
            log().error("Address ID does not exist")
            return jsonify({"error_message":"Address ID does not exist"})
        data = request.get_json()
        address = data["address"]
        address = address.strip()
        address_data =  map_coordinates(address)
        if address_data == {}:
            log().error("Could not update the address as could not find the cordinates of the address")
            return jsonify({"message":"Could not update the address as could not find the cordinates of the address"})
        else:
            log().info("Updating data into DB")
            return jsonify(update_address(address_data,ad_id))

    def delete(self, ad_id):
        log().info('Delete method is called')
        check_id_exists = get_address_by_id(ad_id)
        if check_id_exists == {}:
            log().error("Address ID does not exist")
            return jsonify({"error_message":"Address ID does not exist"})
        
        return jsonify(delete_user(ad_id))

api.add_resource(Address, '/add_address', endpoint = 'add_address')
api.add_resource(Address, '/add_address/<int:ad_id>', endpoint = 'add_address/<int:ad_id>')


if __name__ == "__main__":
    app.run(port = 5000, debug =True)