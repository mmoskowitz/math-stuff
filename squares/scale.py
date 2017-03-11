#!/usr/bin/env python

import csv

with open('coords_raw.txt') as coordsfile:
    reader = csv.reader(coordsfile)
    for row in reader:
        x = int(row[0])
        y = int(row[1])
        print "{0},{1},B".format(x, y)
        print "{1},{0},B".format(x, y)
        for i in range(2, 381 / x):
            print "{0},{1},S".format(x*i, y*i)
            print "{1},{0},S".format(x*i, y*i)

            
