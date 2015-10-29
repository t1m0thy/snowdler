from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

import RPi.GPIO as GPIO ## Import GPIO Library
import time ## Import 'time' library.  Allows us to use 'sleep'

PIN = 21

GPIO.setmode(GPIO.BCM) ## Use BOARD pin numbering

def on(request, pin):
    pin = int(pin)
    GPIO.setup(pin, GPIO.OUT) ## Setup GPIO pin PIN to OUT
    GPIO.output(pin, True)
    return HttpResponse("Pin {} On".format(pin))

def off(request, pin):
    pin = int(pin)
    GPIO.setup(pin, GPIO.OUT) ## Setup GPIO pin PIN to OUT
    GPIO.output(pin, False)
    return HttpResponse("Pin {} Off".format(pin))
