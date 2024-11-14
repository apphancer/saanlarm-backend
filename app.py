from flask import Flask, request, jsonify

app = Flask(__name__)

# Default LED state
led_state = {"state": "off"}

@app.route('/led-state', methods=['GET'])
def get_led_state():
    """
    Endpoint to get the current state of the LED
    """
    return jsonify(led_state)

@app.route('/led-state', methods=['POST'])
def set_led_state():
    """
    Endpoint to set the LED state (off, reading, cozy, alarm)
    """
    data = request.get_json()

    # Check if 'state' key exists in the request
    if 'state' not in data:
        return jsonify({"error": "State is required"}), 400

    state = data['state']

    # Validating state
    valid_states = ["off", "reading", "cozy", "alarm"]
    if state not in valid_states:
        return jsonify({"error": "Invalid state"}), 400

    # Update the LED state and simulate control
    led_state['state'] = state
    control_led(state)

    return jsonify({"message": f"LED state updated to {state}"}), 200

def control_led(state):
    """
    Function to control the LED based on the state
    """

    if state == "off":
        print("Turning off LED")
    elif state == "reading":
        print("Setting LED to 100% brightness")
    elif state == "cozy":
        print("Setting LED to 50% brightness")
    elif state == "alarm":
        print("Setting up alarm activation")
    else:
        print("Unknown state")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)