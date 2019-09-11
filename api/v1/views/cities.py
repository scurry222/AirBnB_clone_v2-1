#!/usr/bin/python3
"""new view for City objects"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from api.v1.app import handle_404
from flask import abort, request


@app_views.route('/cities', strict_slashes=False)
def all_cities():
    """retrieves all cities"""
    city_list = []
    for v in storage.all('City').values():
        city_list.append(v.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def one_city(city_id):
    """retrieve one city"""
    g = storage.get("City", city_id)
    if g:
        return jsonify(g.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_one_city(city_id):
    """deletes city at passed in city id"""
    g = storage.get("City", city_id)
    if g:
        storage.delete(g)
        storage.save()
        storage.close()
        return '{}\n'
    else:
        abort(404)


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def post_cities():
    """posts a specified city"""
    try:
        dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'name' not in dic:
        abort(400, "Missing name")
    else:
        city = City(**dic)
        storage.new(city)
        storage.save()
        storage.close()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def put_city(city_id):
    """puts a specified city"""
    try:
        dic = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if 'name' not in dic:
        abort(400, "Missing name")
    else:
        g = storage.get("City", city_id)
        if g is None:
            abort(404)
        else:
            for attr in dic:
                if attr == "id" or attr == "created_at" or \
                  attr == "updated_at":
                    continue
                setattr(g, attr, dic[attr])
            storage.save()
            storage.close()
            return jsonify(g.to_dict()), 200