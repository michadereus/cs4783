# %%
import sys
sys.path.append('../')
import sql.gateway as gateway
from util.AccessControl import validate_api_key
from util.response_builder import response_builder
import json
from flask import Blueprint, request

# %%
properties_bp = Blueprint('properties', __name__)


@properties_bp.route('/properties', methods=['GET', 'POST'])
def properties():
    gate = gateway.gateway()
    # GET - return dict full of property data in order
    if request.method == 'GET':
        query = gate.get_properties()
        if query == 404:
            return response_builder(json.dumps([{"message":"not found"}]), 404)
        else:
            return response_builder(query, 400)

    # POST - adds a property record
    if request.method == 'POST':
        auth = validate_api_key(request.headers.get("api-key"))
        if auth == True:
            query = gate.post_property(request.form.get("address"), request.form.get("city"), request.form.get("state"), request.form.get("zip"))
            if query == 404:
                return response_builder(json.dumps([{"message":"not found"}]), 404)
            elif query[1] == 200:
                return response_builder(json.dumps([{"message":"added","id":query[0]}]), 200)
            else: 
                return response_builder(query, 400)
        else:
            return response_builder(json.dumps([{"message": "unauthorized"}]), 401)


@properties_bp.route('/properties/<property_id>', methods=['GET', 'DELETE', 'PUT'])
def property_id(property_id):
    gate = gateway.gateway()
    # GET - return detailed info for property with input id
    if request.method == 'GET':
        query = gate.get_property(property_id)
        if query == 404:
            return response_builder(json.dumps([{"message":"not found"}]), 404)
        else:
            return response_builder(query, 200)

    elif request.method == 'DELETE' or request.method == 'PUT':
        auth = validate_api_key(request.headers.get("api-key"))
        if auth == True:
            # DELETE - delete the property w the input id
            if request.method == 'DELETE':
                query = gate.delete_property(property_id)
                if query == 200:
                    return response_builder(json.dumps([{"message":"deleted: "+str(property_id)}]), 200)
                else:
                    return response_builder(json.dumps([{"message":"not found"}]), 404)
                

            # PUT - Updates the property with an id value of <id>. Only the fields to be modified need be present in the response data.
            elif request.method == 'PUT':
                query = gate.put_property(property_id, request.form.get("address"), request.form.get("city"), request.form.get("state"), request.form.get("zip"))
                if query == 200:
                    return response_builder(json.dumps([{"message":"updated property: "+str(property_id)}]), 200)
                else:
                    return response_builder(query, 400)

        else:
            return response_builder(json.dumps([{"message": "unauthorized"}]), 401)
