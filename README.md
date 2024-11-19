# Saanlarm Backend (Raspberry Pi) ⏰🌅

This is the backend part of the Saanlarm project, which runs on the Raspberry Pi. It exposes an API to control the LED strip based on various states (e.g., off, reading, cozy, alarm). The API is built using Flask.

## Prerequisites

### Software

- Python 3.x installed on your Raspberry Pi
- git installed on your Raspberry Pi
- pip for installing dependencies

```bash
sudo apt update
sudo apt install git
sudo apt install python3-pip
```

### Hardware 

- Raspberry Pi
- KY040 rotary encoder (https://pypi.org/project/pyky040/)
- LED Strip (I use a SK6812)

## Setup

### 1. Clone the repository (or create a directory for the project)

`git clone git@github.com:apphancer/saanlarm-backend.git`
`cd saanlarm-backend`


### 2. Install dependencies

Install the dependencies with sudo because accessing the GPIO pins on a Raspberry Pi directly through memory-mapped I/O typically requires root privileges. 

`sudo pip3 install -r requirements.txt`


### 3. Rotary Encoder

Depending on the version of RaspianOS:
`sudo nano /boot/config.txt` or `sudo nano /boot/firmware/config.txt`

Add the following line at the end of the file, replacing pin_a=17 and pin_b=18 with your actual GPIO pins:
`dtoverlay=rotary-encoder,pin_a=17,pin_b=18,relative_axis=1,steps-per-period=1`

Then reboot
`sudo reboot`



## Running the Backend

Run the following command to start the API server on the Raspberry Pi:

`sudo python app.py`

This will start the server on http://0.0.0.0:5000


## To run a daemon


`sudo apt-get install supervisor`

Create a .conf file for your script (e.g., /etc/supervisor/conf.d/app.conf):

```ini
[program:saanlarm]
command=sudo /usr/bin/python /home/pi/saanlarm-backend/app.py
autostart=true
autorestart=true
stderr_logfile=/var/log/saanlarm.err.log
stdout_logfile=/var/log/saanlarm.out.log
user=pi
environment=HOME="/home/pi"
```

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start saanlarm
sudo supervisorctl status saanlarm
```