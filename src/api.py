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
@requires_auth('get:drinks-detail')
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
@requires_auth('post:drinks')
def post_new_drink():
    data = request.get_json()
    drink = None
    try:
        drink = DrinkAccess.create_new_drink(data)
    except ValueError:
        abort(400)
    except Exception as e:
        abort(400, str(e))
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
@requires_auth('patch:drinks')
def update_drink(drink_id):
    if drink_id is None:
        abort(422)

    data = request.get_json()

    drink = None
    try:
        drink = DrinkAccess.update_drink(drink_id, data)
    except ValueError:
        abort(404)
    drinks = [drink.long()]
    response = jsonify({
        'success': True,
        'drinks': drinks
    })
    return response


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    if drink_id is None:
        abort(422)
    try:
        DrinkAccess.delete_drink(drink_id)
    except ValueError:
        abort(400)
    response = jsonify({
        'success': True,
        'delete': drink_id
    })
    return response


@app.errorhandler(422)
def un_processable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "un-processable"
    }), 422


@app.errorhandler(401)
def un_authorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "un-authorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
