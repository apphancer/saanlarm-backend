# Todo

- When app is restarted, it should read the state from the button
- Control Logic
- Authentication 
- Run program as daemon

## Control Logic

- Read button state and update app state
- Write LED indicator state
- Write LED light state
- Program to run alarm and fade-in light


## LED logic

a script tells the Pi which intensity for each LED should be turned on

e.g.

```python
red_value = 100
green_value = 60
blue_value = 40
white_value = 255
```

or

```python
red_value = 0
green_value = 0
blue_value = 0
white_value = 0
```

Requesting cozy light or reading light sends requests to the above script with predefined values
Requesting alarm, sends multiple requests to the above script incrementing white value each time
