#!/usr/bin/python3
"""A simple API endpoints for testing user authentication"""

from flask import Flask, jsonify, abort, request, session
from flask_cors import CORS
from models.user import User, storage
from models.utils.hash_password import hash_password
from functools import wraps


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = "jjhhs997b8@3b8h3#!!O8HNCNIN89/SOUUBCUYUU9"
cors = CORS(app, resources={r"/*": {"origins": "*"}})

storage.reload()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        email = session.get('email')

        def denied():
            return jsonify({'error': 'Login Required!'}), 401

        if email is None:
            return denied()
        return f(*args, **kwargs)
    return decorated_function


@app.route("/status")
def status():
    return jsonify({"status": "OK"})


@app.errorhandler(404)
def not_found(error):
    """404 Not found"""
    return jsonify({"error": "Not found!"}), 404


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    for attr in ['email', 'password']:
        if attr not in data:
            return jsonify({'error': 'Missing data: ' + attr}), 400

    existing_user = storage.get(User, data.get('email'))
    if existing_user is not None:
        return jsonify({'error': 'User already exists'}), 409

    user = User(email=data.get('email'),
                password=hash_password(data.get('password')))
    user.save()
    return jsonify(user.__dict__), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    for attr in ['email', 'password']:
        if attr not in data:
            return jsonify({'error': 'Missing data: ' + attr}), 400

    user = storage.get(User, data.get('email'))
    if user is None:
        abort(404)
    if user.password == str(hash_password(data.get('password'))):
        session['email'] = user.email
        return jsonify(user.__dict__), 200
    return jsonify({'error': 'Wrong Username or Passowrd'}), 400


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({}), 200


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify([user.__dict__ for user in storage.all().values()])


@app.route('/@me')
@login_required
def profile():
    return jsonify({'user': {'email': session.get('email')}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
