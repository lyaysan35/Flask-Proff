#resources folder is like controllers
import models

from flask import Blueprint, jsonify, request
# from flask_login import current_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

professional = Blueprint('professionals', 'professional')

@professional.route('/', methods=["GET"])
def get_all_professionals():
    ## find the professianals and change each one to a dictionary into a new array
    try:
        professionals = [model_to_dict(professional) for professional in models.Professional.select()]
        print(professionals)
        return jsonify(data=professionals, status={"code": 200, "message": "Success"})
    except DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@professional.route('/search', methods=["GET"])
def search_professionals():
    ## find the professianals and change each one to a dictionary into a new array
    try:
        # Get field & location for query string
        # Example request.args.get('field')
        field = request.args.get('field'); # get the field from client's request
        location = request.args.get('location'); # get the location from client's request
        professionals = [model_to_dict(professional) for professional in models.Professional.select()] # get all professionals from database
        # filter professionals from database and keep only the ones that match client's request
        matchingProfs = list(filter(lambda p: p['field'].lower() == field.lower() and p['location'].lower() == location.lower(), professionals))
        # lambda - anonymous TEST function
        # filter - function takes each professional from array and puts it through the TEST
        # if professional passes test, we keep it

        ## send filtered array to client in response
        return jsonify(data=matchingProfs, status={"code": 200, "message": "Success"})
    except DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


@professional.route('/', methods=["POST"])
def create_professionals():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    professionals = models.Professional.create(**payload)
    ## see the object

    print(professionals.__dict__)
    ## Look at all the methods
    print(dir(professionals))
    # Change the model to a dict
    print(model_to_dict(professionals), 'model to dict')
    professionals_dict = model_to_dict(professionals)
    return jsonify(data=professionals_dict, status={"code": 201, "message": "Success"})



@professional.route('/<id>', methods=["GET"])
def get_one_professionals(id):
    print(id, 'reserved word?')
    professional = models.Professional.get_by_id(id)
    print(professional.__dict__)
    return jsonify(data=model_to_dict(professional), status={"code": 200, "message": "Success"})



@professional.route('/<id>', methods=["PUT"])
def update_professionals(id):
    payload = request.json
    print(payload, 'payload')
    query = models.Professional.update(**payload).where(models.Professional.id==id)
    query.execute() # you have to execute the update queries
    return jsonify(data=model_to_dict(models.Professional.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})



@professional.route('/<id>', methods=["Delete"])
def delete_professionals(id):
    query = models.Professional.delete().where(models.Professional.id==id)
    query.execute() # you have to execute the update queries
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

