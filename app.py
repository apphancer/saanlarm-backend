from flask import Flask, request, jsonify
from alarm_checker import periodic_alarm_check, fade_in_completed
from threading import Thread
from user_settings import (
    load_user_settings, save_user_settings, get_alarm_time, set_alarm_time, get_rgbw_values, set_rgbw_values, get_alarm_state, set_alarm_state
)
from rotary import start_rotary_thread
import config_local as config
from auth import token_required, generate_token, USERS

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

load_user_settings()

@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth['username'] or not auth['password']:
        return jsonify({'message': 'Missing credentials'}), 401

    username = auth['username']
    password = auth['password']

    if username in USERS and check_password_hash(USERS[username], password):
        token = generate_token(username)
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/alarm', methods=['GET'])
@token_required
def get_alarm_endpoint():
    return jsonify(get_alarm_time())

@app.route('/alarm', methods=['POST'])
@token_required
def set_alarm_endpoint():
    data = request.get_json()
    response, status_code = set_alarm_time(data)
    return jsonify(response), status_code

@app.route('/colours', methods=['GET'])
@token_required
def get_colours():
    return jsonify(get_rgbw_values()), 200

@app.route('/colours', methods=['POST'])
@token_required
def set_colours():
    data = request.get_json()
    response, status_code = set_rgbw_values(data)
    return jsonify(response), status_code

if __name__ == '__main__':
    start_rotary_thread()

    alarm_thread = Thread(target=periodic_alarm_check)
    alarm_thread.daemon = True
    alarm_thread.start()

    app.run(host=config.HOST, port=config.PORT)