#!/usr/bin/env python

import csv

map = [[0 for i in range(380) ] for j in range(380)]
with open('coords_full.txt') as coordsfile:
    reader = csv.reader(coordsfile)
    for row in reader:
        x = int(row[0]) - 1
        y = int(row[1]) - 1
        #if (x > y):
        map[x][y] = row[2]

print "P3"
print "380 380"
print "2"
for i in range(len(map)):
    j = 379 - i
    row = (map)[j]
    print ' ',
    for k in range(len(row)):
        cell = row[k]
        if (cell == "B"):
            print "0 0 0  ",
        else:
            if (cell == "S"):
                print "1 0 1  ",
            else:
                if (j % 100 == 0 or k % 100 == 0):
                    print "0 2 2  ",
                else:
                    if (j % 10 == 0 or k % 10 == 0):
                        print "1 2 2  ",
                    else:
                        print "2 2 2  "
            

    print "#{}".format(j + 1)


            
