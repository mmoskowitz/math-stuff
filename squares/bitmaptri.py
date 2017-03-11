#!/usr/bin/env python

import csv

map = [[0 for i in range(380) ] for j in range(380)]
with open('coords_full.txt') as coordsfile:
    reader = csv.reader(coordsfile)
    for row in reader:
        x = int(row[0]) - 1
        y = int(row[1]) - 1
        if (x > y):
            map[x][y] = 1

print "P1"
print "380 380"
for i in range(len(map)):
    j = 379 - i
    row = (map)[j]
    print ' ',
    for cell in row:
        print cell,
    print "#{}".format(j + 1)


            
