"""
sudo apt-get update
sudo apt-get install python3
sudo apt-get install RPi.GPIO
"""

import time
from time import sleep
import requests

import RPi.GPIO as GPIO

TEAM1_PIN_OUTPUT = 14
TEAM1_PIN_INPUT = 20

TEAM2_PIN_OUTPUT = 18
TEAM2_PIN_INPUT = 21

#Loop timer
SENSITIVITY = 20

#Duration timer
DURATION = 10

URL = 'http://locahost:8080'

def setup():
    """
    setup GPIO bus
    """
    GPIO.setmode(GPIO.BOARD)

    # Output pins
    GPIO.setup(TEAM1_PIN_OUTPUT, GPIO.OUT)
    GPIO.setup(TEAM2_PIN_OUTPUT, GPIO.OUT)

    # Input pins
    GPIO.setup(TEAM1_PIN_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TEAM2_PIN_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Turn on output pins
    GPIO.output(TEAM1_PIN_OUTPUT, GPIO.HIGH)
    GPIO.output(TEAM2_PIN_OUTPUT, GPIO.HIGH)


def detect(logic):
    """
    Detect ball
    """
    if logic:
        myLow = GPIO.LOW
        myHigh = GPIO.HIGH
    else:
        myLow = GPIO.HIGH
        myHigh = GPIO.LOW

    while True:
        time.sleep(SENSITIVITY)
        ret1 = GPIO.input(TEAM1_PIN_INPUT)
        ret2 = GPIO.input(TEAM2_PIN_INPUT)
        while ret1 != myLow or ret1 != myLow:
            if ret1 == myHigh:
                while ret1 == myHigh:
                    ret1 = GPIO.input(TEAM1_PIN_INPUT)
                    time.sleep(DURATION)
                send_trigger(1)

            if ret2 == myHigh:
                while ret2 == myHigh:
                    ret2 = GPIO.input(TEAM2_PIN_INPUT)
                    time.sleep(DURATION)
                send_trigger(2)

def send_trigger(num):
    """
    Send the REST info to the server
    """
    data = {'action': 'goal',
            'team':   num.str()}
    data_json = simplejson.dumps(data)
    print data_json
    payload = {'json_payload': data_json}
    r = requests.post(URL, data=payload)
    r = request()


if __name__ == "__main__":
    send_trigger(1)
    sleep(6)
    send_trigger(2)
    sleep(1)
    send_trigger(1)
    sleep(2)
    send_trigger(1)
    sleep(4)
    send_trigger(2)
