#!/usr/bin/python

from svgpathtools import *
from math import *

def round_to_multiple(x, step_size):
    return step_size * int(floor(float(x)/step_size + 0.5))

# round off coords of p (complex number) to nearest multiple of step size
def quantize_point(p, step_size):
    x = round_to_multiple(p.real, step_size)
    y = round_to_multiple(p.imag, step_size)
    return (x,y)

def quantize_path(path, step_size, t0=0.0, t1=1.0):
    a_true = path.point(t0)
    a = quantize_point(a_true, step_size)

    b_true = path.point(t1)
    b = quantize_point(b_true, step_size) 

    step = (b[0]-a[0], b[1]-a[1])
    if abs(step[0]) <= step_size and abs(step[1]) <= step_size:
        if path.length(t0,t1) < 1.5 * step_size:
            return [a, b]
    t_mid = (t0 + t1)/2
    head = quantize_path(path, step_size, t0, t_mid)
    tail = quantize_path(path, step_size, t_mid, t1)
    return head + tail[1:]

def quantize_all_paths(filename, step_size=10):
    paths, attributes = svg2paths(filename)
    output = []
    for p in paths:
        output.append(quantize_path(p, step_size))
    outputfile = open("quantized_paths.py", "w")
    outputfile.write("paths=")
    outputfile.write(str(output))
    outputfile.close()
        

