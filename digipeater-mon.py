import sys
import RPi.GPIO as GPIO
import time
import psutil
import subprocess
from subprocess import call

LED_GREEN = 22
LED_YELLOW = 27
PUSHBUTTON = 17

def setOutput(gpio, flag):
    GPIO.output(gpio, flag)

def setupIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_YELLOW, GPIO.OUT)
    GPIO.setup(PUSHBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    setOutput(LED_GREEN, False)
    setOutput(LED_YELLOW, False)

def alternateLEDs():
    for x in range(0, 5):
        setOutput(LED_GREEN, True)
        setOutput(LED_YELLOW, False)
        time.sleep(0.2)
        setOutput(LED_GREEN, False)
        setOutput(LED_YELLOW, True)
        time.sleep(0.2)

    setOutput(LED_YELLOW, False)

def flashLEDs():
    for x in range(0, 5):
        setOutput(LED_GREEN, True)
        setOutput(LED_YELLOW, True)
        time.sleep(0.2)
        setOutput(LED_GREEN, False)
        setOutput(LED_YELLOW, False)
        time.sleep(0.2)

def isButtonPressed(gpio):
    if GPIO.input(gpio) == GPIO.LOW:
        return True
    else:
        return False

def isDirewolfRunning():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == "direwolf":
            return True
    
    return False


keepRunning = True
direwolfRunning = False

setupIO()
alternateLEDs()

while keepRunning:
     
    if isDirewolfRunning():
        if direwolfRunning == False:
            direwolfRunning = True
            setOutput(LED_GREEN, True)
    else:
        if direwolfRunning == True:
            direwolfRunning = False
            setOutput(LED_GREEN, False)

    if isButtonPressed(PUSHBUTTON):
        flashLEDs();
        setOutput(LED_YELLOW, True)
        call("sudo shutdown now --poweroff", shell=True)
        keepRunning = False;

    time.sleep(3)
