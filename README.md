# Saanlarm Backend (Raspberry Pi)

This is the backend part of the Saanlarm project, which runs on the Raspberry Pi. It exposes an API to control the LED strip based on various states (e.g., off, reading, cozy, alarm). The API is built using Flask.

## Prerequisites

### Software

- Python 3.x installed on your Raspberry Pi
- git installed on your Raspberry Pi
- pip for installing dependencies

### Hardware 

- Raspberry Pi
- KY040 rotary encoder (https://pypi.org/project/pyky040/)
- LED Strip (I use a SK6812)

## Setup

### 1. Clone the repository (or create a directory for the project)

`git clone <repo-url>`
`cd saanlarm-backend`


### 2. Install dependencies

Install the dependencies with sudo because accessing the GPIO pins on a Raspberry Pi directly through memory-mapped I/O typically requires root privileges. 

`sudo pip3 install -r requirements.txt`


### 3. Rotary Encoder

`sudo nano /boot/firmware/config.txt`

Add the following line at the end of the file, replacing pin_a=17 and pin_b=18 with your actual GPIO pins:
`dtoverlay=rotary-encoder,pin_a=17,pin_b=18,relative_axis=1,steps-per-period=1`

`sudo reboot`



## Running the Backend

### 1. Start the Flask server

Run the following command to start the API server on the Raspberry Pi:

`python app.py`

This will start the server on http://0.0.0.0:5000


## API Endpoints

### 1. GET /led-state

Retrieves the current state of the LED strip.
Example response:

`{ "state": "off" }`


### 2. POST /led-state

Sets the state of the LED strip. The request body must include a JSON object with a state key.

Valid states:

- "off"
- "reading"
- "cozy"
- "alarm"

Example request:

```json
{
  "state": "reading"  
}
```

Example response:

```json
{ "message": "LED state updated to reading" }
```
