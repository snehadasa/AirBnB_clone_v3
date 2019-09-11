#!/usr/bin/python3
"""script that starts a Flask web application"""


from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.state import City
import os
app = Flask(__name__)


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id=None):
    """Retrieves the list of all City objects"""
    cities = storage.all('City')
    city_list = []
    flag = 0
    for city in cities.values():
        if city.state_id == state_id:
            city_list.append(city.to_dict())
            flag = 1
    if flag == 0:
        abort(404)
    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """Retrieves a City object with the id linked to it"""
    city_dict = storage.all('City')
    city = city_dict.get('City' + "." + city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """Deletes a City object"""
    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id=None):
    """Creates a City"""
    state_dict = storage.all('State')
    state = state_dict.get('State' + "." + state_id)
    if state is None:
        abort(404)
    result = request.get_json()
    if not result:
        abort(400, {"Not a JSON"})
    if 'name' not in result:
        abort(400, {"Missing name"})
    obj = City(name=result['name'], state_id=state_id)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
    """Updates a City object"""
    result = request.get_json()
    if not result:
        abort(400, {"Not a JSON"})
    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    invalid_keys = ["id", "created_at", "updated_at"]
    for key, value in result.items():
        if key not in invalid_keys:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200