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

def set_led_colours(red, green, blue, white):
    """
    Sets the LED colours using RGBW values.
    """
    print(f"Setting LED colours: R:{red}, G:{green}, B:{blue}, W:{white}")