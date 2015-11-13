import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from django.views.generic import View

# Create your views here.

import RPi.GPIO as io ## Import GPIO Library
import time ## Import 'time' library.  Allows us to use 'sleep'

logger = logging.getLogger(__name__)

FREQUENCY = 100
PIN = 21

PWM_OBJECTS = {}

io.setmode(io.BCM) ## Use BOARD pin numbering

LOOKUP = {io.IN: "IN",
          io.OUT: "OUT",
          io.SPI: "SPI",
          io.I2C: "I2C",
          io.HARD_PWM: "HARD_PWM",
          io.SERIAL: "SERIAL",
          io.UNKNOWN: "UNKNOWN"
         }
MODES = {"bcm": io.BCM,
         "board": io.BOARD}

MODE_TO_STR = {io.BCM: "BCM",
                io.BOARD: "BOARD"}

def set_input(request, pin):
    pin = int(pin)
    if pin in PWM_OBJECTS:
        del(PWM_OBJECTS[pin])
    io.setup(pin, io.IN)
    return HttpResponse("Pin {} set to INPUT".format(pin))

def on(request, pin):
    pin = int(pin)
    if pin in PWM_OBJECTS:
        del(PWM_OBJECTS[pin])
    io.setup(pin, io.OUT) ## Setup GPIO pin PIN to OUT
    io.output(pin, True)
    return HttpResponse("Pin {} On".format(pin))

def off(request, pin):
    pin = int(pin)
    if pin in PWM_OBJECTS:
        del(PWM_OBJECTS[pin])
    io.setup(pin, io.OUT) ## Setup GPIO pin PIN to OUT
    io.output(pin, False)
    return HttpResponse("Pin {} Off".format(pin))

def pwm(request, pin, duty):
    pin = int(pin)
    duty = float(duty)
    io.setup(pin, io.OUT) ## Setup GPIO pin PIN to OUT
    if pin in PWM_OBJECTS:
        PWM_OBJECTS[pin].ChangeDutyCycle(duty)
    else:
        p = io.PWM(pin, FREQUENCY)
        p.start(duty)
        PWM_OBJECTS[pin] = p
    return HttpResponse("Pin {} at duty {}".format(pin, duty))

def _handle_mode(request):
    """
    given a request, look for mode= in the query args and set the current mode to that if needed

    update the mode
    add a message to the request
    return the MODES
    """
    strmode = request.GET.get('mode', "")
    old_mode = io.getmode()
    if not strmode:
        mode = old_mode
    else:
        mode = MODES[strmode.lower()]
    if old_mode != mode:
        io.setup(3, io.gpio_function(3))  # THIS IS A HACK TO GET CLEANUP TO WORK
        io.cleanup()
        try:
            io.setmode(mode)
            messages.warning(request, "New io mode: {}.  All pins reset".format(MODE_TO_STR[mode]))
        except ValueError:
            messages.error(request, "Could not switch to new io mode: {}".format(MODE_TO_STR[mode]))
            mode = old_mode
    return mode

def mode(request):
    mode = _handle_mode(request)
    return HttpResponse(MODE_TO_STR[mode])

def index(request):
    context = {}
    mode = _handle_mode(request)
    context["mode"] = MODE_TO_STR[mode]
    if mode == io.BCM:
        MAX_PINS = 26
    else:
        MAX_PINS = 40
    pin_states = []
    for i in range(1, MAX_PINS+1):
        try:
            m = io.gpio_function(i)
            if m <= 1:
                io.setup(i, m)
                s = io.input(i)
            else:
                s = 'NA'
            pin_states.append(dict(number=i,
                                    mode=LOOKUP[m],
                                    state=s,
                                    is_input=s==io.IN,
                                    is_serial=s not in [io.IN,io.OUT],
                                    min=0,
                                    max=100,
                                    value=0))
        except ValueError:
            logging.debug("Bad pin {}".format(i))
    context["pin_states"] = pin_states
    return render(request, 'pinner.html', context)


