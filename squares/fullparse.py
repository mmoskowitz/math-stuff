#!/usr/bin/env python

import csv, sys

filename = "young.txt"
size = 380
zoom = 1

mode = "default"

args = sys.argv

args.pop(0)

if (len(args) > 0):
    size = int(args.pop(0))

if (len(args) > 0):
    zoom = int(args.pop(0))

if (len(args) > 0):
    mode = args.pop(0)

#size = 380 
maxes = [[0 for i in range(size) ] for j in range(size)]
cats = [['' for i in range(size) ] for j in range(size)]

mode_dict = {}

#possible cats:
#  square
#  trivial
#  scaled trivial
#  basic
#  scaled basic
#  vertical
#  scaled vertical
#  nontrivial
#  scaled nontrivial

def add_to_dict(mode, cat_list, color):
    if (mode not in mode_dict):
        mode_dict[mode] = {}
    for cat in cat_list.split():
        mode_dict[mode][cat] = color

tmode = "default"
add_to_dict(tmode, "b", "1 0 0")
add_to_dict(tmode, "sb", "2 0 0")
add_to_dict(tmode, "v n", "0 0 0")
add_to_dict(tmode, "sv sn", "1 1 1")
tmode = "basic"
add_to_dict(tmode, "b", "0 0 0")
add_to_dict(tmode, "sb", "1 1 1")
tmode = "trivial"
add_to_dict(tmode, "t s", "0 0 0")
add_to_dict(tmode, "st", "1 1 1")
tmode = "nontrivial"
add_to_dict(tmode, "n v", "0 0 0")
add_to_dict(tmode, "sn sv", "1 1 1")



#convert from numerical (1-based) to python (0-based)
def set(x, y, max, val):
    if (x > size or y > size):
        return
    maxes[x - 1][y - 1] = max
    cats[x - 1][y - 1] = val
def gmax(x, y):
    if (y > x):
        (x,y) = (y,x)
    return maxes[x - 1][y - 1]
def gcat(x, y):
    return cats[x - 1][y - 1]

def is_trivial(x,y,num = 0):
    """Indicates whether the decomposition includes non-trivial items"""
    if (y > x):
        (x,y) = (y,x)
    if (num == 0):
        num = gmax(x,y)
    debug("checking {} {} {}".format(x, y, num))
    if (gcat(x,y) in ("square", "trivial", "scaled trivial")):
        debug("trivial as {}".format(gcat(x,y)))
        return True
    nx = x - num
    if (1 in (num, x-num)):
        debug("trivial as 1")
        return True
    if (y in (num, x-num)):
        debug("removing square")
        return (is_trivial(x-y, y))
    else:
        debug("splitting")
        if (is_trivial(x-num, y) and is_trivial(num, y)):
            lmax = max(gmax(x-num, y), gmax(num, y))
            debug ("checking {} vs. {}".format(lmax,y))
            if (lmax == y):
                return is_trivial(x-y, y)
            
        else:
            debug ("nontrivial")
            return False
def debug(text):
    sys.stderr.write(text + "\n")


           
def get_color(x,y,cat):
    code = "".join([word[0] for word in cat.split()])
    if (code in mode_dict[mode]):
        return mode_dict[mode][code]
    elif (x % 100 == 0 or y % 100 == 0):
        return "0 1 1"
    elif (x % 10 == 0 or y % 10 == 0):
        return "1 2 2"
    else:
        return "2 2 2"

def printpbm():
    print "P3"
    print size * zoom, size * zoom
    print "2"

    for rx in range(size):
        x = size - 1 - rx
        for zx in range(zoom):
            for y in range(size):
                for zy in range(zoom):
                    cat = gcat(x,y)
                    if (y > x):
                        cat = gcat(y,x)
                    color = get_color(x,y,cat)
                    print color + "  ",
            print

    

with open(filename) as coordsfile:
    for line in coordsfile:
        line = line.strip()
        (coords, value) = line.split(" -> ")
        (x,y) = [int(n) for n in coords.split(',')]
        if (x > size or y > size):
            continue
        (count, result) = line.split(" : ")
        if (result.startswith("square")):
            set(x,y,y,"square")
        elif (result.startswith("basic")):
            solution = result.split(" ")[-1].strip(",")
            items = solution.split(",")
            bmax = max([int(n.split(":")[1]) for n in items])
            set(x,y,bmax,"basic")
        elif (result.startswith("scale")):
            scale = int(result.split(" ")[-1])
            (sx, sy) = [n/scale for n in (x,y)]
            smax = gmax(sx,sy)
            cat = gcat(sx,sy)
            if (not(cat.startswith("scaled "))):
                cat = "scaled " + cat
            set(x,y,scale * smax, cat)
        elif (result.startswith("vertical")):
            cat = "vertical"
            split = int(result.split(" ")[-1])
            vmax = max (gmax(x, y-split), gmax(x, split))
            set(x,y, vmax, cat)
        elif (result.startswith("horizontal")):
            split = int(result.split(" ")[-1])
            if (is_trivial(x,y,split)):
                set(x,y,y,"trivial")
            else:
                set(x,y,y,"nontrivial")
        else:
            pass
            
printpbm()
