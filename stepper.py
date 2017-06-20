#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from random import randint
 
GPIO.setmode(GPIO.BCM)
 
motor2_enable_pin = 22 
motor2_coil_A_1_pin =  5
motor2_coil_A_2_pin = 6 
motor2_coil_B_1_pin = 26 
motor2_coil_B_2_pin = 27
 
motor1_enable_pin = 18
motor1_coil_A_1_pin =  4
motor1_coil_A_2_pin = 17
motor1_coil_B_1_pin = 23
motor1_coil_B_2_pin = 24
 
GPIO.setup(motor1_enable_pin, GPIO.OUT)
GPIO.setup(motor1_coil_A_1_pin, GPIO.OUT)
GPIO.setup(motor1_coil_A_2_pin, GPIO.OUT)
GPIO.setup(motor1_coil_B_1_pin, GPIO.OUT)
GPIO.setup(motor1_coil_B_2_pin, GPIO.OUT)
 
GPIO.setup(motor2_enable_pin, GPIO.OUT)
GPIO.setup(motor2_coil_A_1_pin, GPIO.OUT)
GPIO.setup(motor2_coil_A_2_pin, GPIO.OUT)
GPIO.setup(motor2_coil_B_1_pin, GPIO.OUT)
GPIO.setup(motor2_coil_B_2_pin, GPIO.OUT)
 
GPIO.output(motor1_enable_pin, 1)
GPIO.output(motor2_enable_pin, 1)
 
def forward(delay, steps, whichmotor):  
  for i in range(0, steps):
    setStep(1, 0, 1, 0, whichmotor)
    time.sleep(delay)
    setStep(0, 1, 1, 0, whichmotor)
    time.sleep(delay)
    setStep(0, 1, 0, 1, whichmotor)
    time.sleep(delay)
    setStep(1, 0, 0, 1, whichmotor)
    time.sleep(delay)
 
def backwards(delay, steps, whichmotor):  
  for i in range(0, steps):
    setStep(1, 0, 0, 1, whichmotor)
    time.sleep(delay)
    setStep(0, 1, 0, 1, whichmotor)
    time.sleep(delay)
    setStep(0, 1, 1, 0, whichmotor)
    time.sleep(delay)
    setStep(1, 0, 1, 0, whichmotor)
    time.sleep(delay)
 
  
def setStep(w1, w2, w3, w4, whichmotor):
    if whichmotor == 1:
        GPIO.output(motor1_coil_A_1_pin, w1)
        GPIO.output(motor1_coil_A_2_pin, w2)
        GPIO.output(motor1_coil_B_1_pin, w3)
        GPIO.output(motor1_coil_B_2_pin, w4)
    elif whichmotor == 2:
        GPIO.output(motor2_coil_A_1_pin, w1)
        GPIO.output(motor2_coil_A_2_pin, w2)
        GPIO.output(motor2_coil_B_1_pin, w3)
        GPIO.output(motor2_coil_B_2_pin, w4)
    else:
	raise Exception("I only have 2 motors")

def r(n, delay=0.006):
    if n>0:
	forward(delay, n, 2)
    elif n<0:
        backwards(delay, -n, 2)

def l(n, delay=0.006):
    if n>0:
	forward(delay, n, 1)
    elif n<0:
        backwards(delay, -n, 1)	


def spiral(loops=10, scale=10):
    for n in range(1,loops+1):
	steps = 2*scale*n
	r(steps)
	l(steps)
	r(-steps-scale)
	l(-steps-scale)

#while True:
#    delay = 4
#
#    steps = randint(50,200)
#    whichmotor = randint(1,2)
#    print "motor %d going forward %d steps" % (whichmotor, steps)
#    forward(int(delay) / 1000.0, int(steps), whichmotor)
#
#    whichmotor = randint(1,2)
#    steps = randint(50,200)
#    print "motor %d going backward %d steps" % (whichmotor, steps)
#    backwards(int(delay) / 1000.0, int(steps), whichmotor)


