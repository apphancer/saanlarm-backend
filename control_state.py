def control_state(state):
    """
    Control the LED based on the state.
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