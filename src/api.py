import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db
from .database.database_access import DrinkAccess
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''

db_drop_and_create_all()


@app.route('/drinks')
def get_all_drinks():
    response = jsonify({
        'success': True,
        'drinks': DrinkAccess.get_all_drinks_short()
    })
    return response


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
'''


@app.route('/drinks-detail')
def get_all_drinks_detail():
    response = jsonify({
        'success': True,
        'drinks': DrinkAccess.get_all_drinks_long()
    })
    return response


'''
@TODO implement endpoint
    POST /drinks
        it should require the 'post:drinks' permission
'''


@app.route('/drinks', methods=['POST'])
def post_new_drink():
    data = request.get_json()
    drink = None
    try:
        drink = DrinkAccess.create_new_drink(data)
    except ValueError:
        abort(400)
    drinks = [drink.long()]
    response = jsonify({
        'success': True,
        'drinks': drinks
    })
    return response


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        it should require the 'patch:drinks' permission
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def update_drink(drink_id):
    if drink_id is None:
        abort(422)

    data = request.get_json()

    drink = None
    try:
        drink = DrinkAccess.update_drink(drink_id, data)
    except ValueError:
        abort(400)
    drinks = [drink.long()]
    response = jsonify({
        'success': True,
        'drinks': drinks
    })
    return response


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

## Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
