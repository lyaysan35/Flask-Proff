import models

from flask import Blueprint, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

#register our user blueprint
#pass in the blueprint name and the import_name

user = Blueprint('users', 'user')



@user.route('/register', methods=["POST"])
def register():
    ## see request payload anagolous to req.body in express
    ## This is how you get the image you sent over


    ## This has all the data like username, email, password
    payload = request.get_json()



    payload['email'].lower()
    try:
        # Find if the user already exists?
        models.User.get(models.User.email == payload['email']) # model query finding by email
        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})
    except DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) # bcrypt line for generating the hash
        user = models.User.create(**payload) # put the user in the database
                                             # **payload, is spreading like js (...) the properties of the payload object out

        #login_user
        login_user(user) # starts session

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        # delete the password
        del user_dict['password'] # delete the password before we return it, because we don't need the client to be aware of it

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})



@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, '< --- this is playload')
    try:
        user = models.User.get(models.User.email== payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            # After user successfully logs in, fetch the Professional model that user
            # created when he/she registered by matching the userId of the Professional
            # model with the id of the user, who just logged in.
            prof_dict = model_to_dict(models.Professional.get(models.Professional.userId == user.id))
            response = { 'user': user_dict, 'prof': prof_dict }
            return jsonify(data=response, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

@user.route('/logout', methods=["POST"])
def logout():
    try:
        logout_user()
        return jsonify(status={"code": 200, "message": "Successfully logged out"})
    except models.DoesNotExist:
        return jsonify(status={"code": 400, "message": "Failed to logout"})