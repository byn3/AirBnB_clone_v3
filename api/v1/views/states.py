#!/usr/bin/python3
""" file that handles all states flask stuff """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.state import State
from flasgger import swag_from


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@swag_from("all_states.yml")
def showStates():
    """ Shows all states in the file storage """
    count_l = []
    for value in storage.all("State").values():
        count_l.append(value.to_dict())
    return(jsonify(count_l))


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
@swag_from("states.yml")
def a_states_id(state_id):
    """
        This is the HBNB API
        Call this api passing a state_id
        and get back its schema
    """
    i = storage.get("State", state_id)
    if i:
        return jsonify(i.to_dict())
    else:
        return (jsonify({"error": "Not found"}), 404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=["DELETE"])
@swag_from("states.yml")
def del_states_id(state_id):
    """ deletes a sate if given the id """
    thing = storage.all('State')
    muricanState = "State." + state_id
    state = thing.get(muricanState)
    if state is None:
        abort(404)
    else:
        state.delete()
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
@swag_from("post_states.yml")
def postStates():
    """ creates a new state """
    thing = request.get_json(silent=True)
    if thing is None or not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    state = thing.get("name")
    if state is None or len(thing) == 0:
        return (jsonify({"error": "Missing name"}), 400)
    s = State()
    s.name = state
    s.save()
    return (jsonify(s.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["PUT"])
@swag_from("states.yml")
def updateState(state_id):
    """ updates the state info, sopecifically name """
    # garbage = {"id", "created_at", "updated_at"}
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    thing = request.get_json(silent=True)
    if thing is None or not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    thing = request.get_json(silent=True)
    for key, value in thing.items():
        if key == 'name':
            setattr(state, key, value)
    state.save()
    return (jsonify(state.to_dict()), 200)
