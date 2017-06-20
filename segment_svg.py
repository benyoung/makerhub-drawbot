#!/usr/bin/python

from svgpathtools import *
from math import *

L = 45.0                   # distance between motors in inches
inkscape_width = 744.0     # width of default inkscape doc, in whatever the heck coords inkscape uses
inkscape_height = 1052.0   # height of default inkscape doc. I think I never use this?  Wanna keep scaling 1:1
import time
import RPi.GPIO as GPIO

#steps_per_inch = 513.0  / 0.75  # made-up numbers.  bobbin circ is ~0.75 in; steppers are 513 steps/rev.
steps_per_inch = 400.0 / 4.840  # measured this, why is it so different, i do not know

class Drawbot(object):
    def __init__(self, left_len_inches, right_len_inches):
        self.set_current_string_lengths(left_len_inches, right_len_inches)

        GPIO.setmode(GPIO.BCM)
        self.motor2_enable_pin = 22 
        self.motor2_coil_A_1_pin =  5
        self.motor2_coil_A_2_pin = 6 
        self.motor2_coil_B_1_pin = 26 
        self.motor2_coil_B_2_pin = 27
         
        self.motor1_enable_pin = 16
        self.motor1_coil_A_1_pin =  4
        self.motor1_coil_A_2_pin = 17
        self.motor1_coil_B_1_pin = 23
        self.motor1_coil_B_2_pin = 24
        
        GPIO.setup(self.motor1_enable_pin, GPIO.OUT)
        GPIO.setup(self.motor1_coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.motor1_coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.motor1_coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.motor1_coil_B_2_pin, GPIO.OUT)
         
        GPIO.setup(self.motor2_enable_pin, GPIO.OUT)
        GPIO.setup(self.motor2_coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.motor2_coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.motor2_coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.motor2_coil_B_2_pin, GPIO.OUT)
         
        GPIO.output(self.motor1_enable_pin, 1)
        GPIO.output(self.motor2_enable_pin, 1)

    def _setStep(self, w1, w2, w3, w4, whichmotor):
        if whichmotor == 1:
            GPIO.output(self.motor1_coil_A_1_pin, w1)
            GPIO.output(self.motor1_coil_A_2_pin, w2)
            GPIO.output(self.motor1_coil_B_1_pin, w3)
            GPIO.output(self.motor1_coil_B_2_pin, w4)
        elif whichmotor == 2:
            GPIO.output(self.motor2_coil_A_1_pin, w1)
            GPIO.output(self.motor2_coil_A_2_pin, w2)
            GPIO.output(self.motor2_coil_B_1_pin, w3)
            GPIO.output(self.motor2_coil_B_2_pin, w4)
        else:
            raise Exception("I only have 2 motors")

    def _forwards(self, delay, steps, whichmotor):  
        for i in range(0, steps):
            self._setStep(1, 0, 1, 0, whichmotor)
            time.sleep(delay)
            self._setStep(0, 1, 1, 0, whichmotor)
            time.sleep(delay)
            self._setStep(0, 1, 0, 1, whichmotor)
            time.sleep(delay)
            self._setStep(1, 0, 0, 1, whichmotor)
            time.sleep(delay)
     
    def _backwards(self, delay, steps, whichmotor):  
        for i in range(0, steps):
            self._setStep(1, 0, 0, 1, whichmotor)
            time.sleep(delay)
            self._setStep(0, 1, 0, 1, whichmotor)
            time.sleep(delay)
            self._setStep(0, 1, 1, 0, whichmotor)
            time.sleep(delay)
            self._setStep(1, 0, 1, 0, whichmotor)
            time.sleep(delay)

    def set_current_string_lengths(self, left_len_inches, right_len_inches):
        self.left_len  = int(left_len_inches * steps_per_inch)
        self.right_len = int(right_len_inches * steps_per_inch)
 
    def step_left(self, n, delay=0.006):
        #print n
        print "L%d " % n,  # left motor control code goes in here
        if n>0:
            self._backwards(delay, n, 1) # left motor is backwards, wasn't thinking
        elif n<0:
            self._forwards(delay, -n, 1)	

    def step_right(self, n, delay=0.006):
        print "R%d " % n, 
        if n>0:
            self._forwards(delay, n, 2)
        elif n<0:
            self._backwards(delay, -n, 2)

    def move_left(self, new_left_len):    
        self.step_left(new_left_len - self.left_len)
        self.left_len = new_left_len

    def move_right(self, new_right_len):
        self.step_right(new_right_len - self.right_len)
        self.right_len = new_right_len

    def go_to(self, p): # p is a point, already in "steps" coordinates
        self.move_left(p[0])
        self.move_right(p[1])

    def trace_path(self, path):
        for p in path:
            print p
            self.go_to(p)

drawbot = Drawbot(30,30) # strings 2.5 feet long

def svg_coords_to_string_lengths(p):
    x, y = p
    a = float(x) / inkscape_width * L #inches
    h = float(y) / inkscape_width * L # inches
    len_left = sqrt(a*a + h*h) * steps_per_inch
    len_right = sqrt((L-a)*(L-a) + h*h) * steps_per_inch
    return len_left, len_right

def string_lengths_to_svg_coords(lengths):
    len_left, len_right = lengths
    l1 = float(len_left) / steps_per_inch # inches
    l2 = float(len_right) / steps_per_inch #inches
    a = 0.5 * (L + l1*l1/L - l2*l2/L)
    h = sqrt(l1*l1 - a*a)
    x = a / L * inkscape_width
    y = h / L * inkscape_width
    return (x,y)

def round_to_multiple(x, step_size):
    return step_size * int(floor(float(x)/step_size + 0.5))

# round off coords of p (ordered pair) to nearest multiple of step size
def quantize_point(p, step_size):
    u = round_to_multiple(p[0], step_size)
    v = round_to_multiple(p[1], step_size)
    return (u,v)


def quantized_path_point(path, t, increment_size):
    z = path.point(t)
    a_exact = svg_coords_to_string_lengths((z.real, z.imag))
    return quantize_point(a_exact, increment_size)

def quantize_path(path, increment_size, oversample = 5):
    total_length = path.length() / inkscape_width * L * steps_per_inch # length, in motor steps, of curve
    num_increments = int(total_length / increment_size * oversample)
    t_inc = 1/float(num_increments)
    t = 0
    quantized_path = [quantized_path_point(path, 0.0, increment_size)]
    t += t_inc
    while t < 1:
        a = quantized_path_point(path,t,increment_size)
        if a != quantized_path[-1]:
            quantized_path.append(a)
        t += t_inc
    a = quantized_path_point(path, 1.0, increment_size)
    if a != quantized_path[-1]:
        quantized_path.append(a)
    return quantized_path



def quantize_all_paths(filename, step_size=100, actually_draw=False):
    paths, attributes = svg2paths(filename)
    output = []
    for p in paths:
        if actually_draw:
            output.append(quantize_path(p, step_size))
            drawbot.trace_path(output[-1])
        else:
            output.append(quantize_path(p, step_size))

    if not actually_draw:
        outputfile = open("quantized_paths.py", "w")
        outputfile.write("paths=")
        outputfile.write(str(output))
        outputfile.close()
        

