#!/usr/bin/env python
#
# Infinite Resistor Grid Approximation Generator
# Generates degenerate cases of an "infinite" grid of resistors.
# Designed to be used with HSPICE, maybe others.
#
# Matthew Beckler - matthew at mbeckler dot org
# For more details, visit http://www.mbeckler.org/resistor_grid/

import sys
import numpy
import os

resistivity = .00000007     #resistivity
x_Length = int(input("How long is the X directoin of your sheet?(mm) "))
y_Length = int(input("How long is the Y direction of your sheet?(mm) "))
thickness = float(input("How thick is your material?(mm) "))
divisions = int(input("How many divisions: "))

x_Res_Length = x_Length/divisions      #length of a division in x direction
y_Res_Length = y_Length/divisions      #length of a division in y direction

#resistance of a resistor parallel to X axis - need to convert to meters from mm
x_Resistance = (resistivity*(x_Length/1000))/((y_Res_Length/1000)*(thickness/1000))

#resistance of a resistor parallel to Y axis - need to convert to meters from mm
y_Resistance = (resistivity*(y_Length/1000))/((x_Res_Length/1000)*(thickness/1000))

#names file X length x Y length x thickness with number of divisions per axis
folder = ("%d mm x %d mm x %.2f" % (x_Length,y_Length,thickness))
if(os.path.exists(folder)):
    None
else:
    os.mkdir(folder)

file = open(("%d mm x %d mm x %.2f/%d divisions per axis.net" % (x_Length,y_Length,thickness,divisions)),'w')

    #replaced by divisions
# long_side = int(input("Length of Long Side:"))

    #not needed
# if long_side < 2:
#     print("Usage: %s long_side" % sys.argv[0])
#     sys.exit(1)

    #not needed
# short_side = long_side - 1

    #not needed
# if long_side < 3 or long_side % 2 == 0:
#     print ("long_side must be odd and >= 3!")
#     sys.exit(1)

array = numpy.zeros((divisions, divisions))
node_id = 1 # start at 1 so we still have 0 (ground)
power_Node = int(divisions/10)     #puts power node 10% of the way in
gnd_Node = int(divisions*.9)       #puts gnd node 10% in from the far edge
# gnd_node_y = divisions / 2 + 1
# gnd_node_x = (divisions + 1) / 2 + 1
# vin_node_y = divisions / 2
# vin_node_x = (divisions - 1) / 2
vin_node_id = 0 # to be changed
for y in range(1, divisions + 1):
    for x in range(1, divisions + 1):
        if y == gnd_Node and x == gnd_Node:
            this_node_id = 0
        else:
            this_node_id = node_id
            node_id += 1

        if y == power_Node and x == power_Node:
            vin_node_id = this_node_id

        array[y-1,x-1] = this_node_id

#print array
file.write(("%d mm x %d mm x %.2f with %d divisions per axis\n" % (x_Length,y_Length,thickness,divisions)))
# print("EXAMPLE PSpice")
resistor_id = 0
for y in range(1, divisions + 1):
    for x in range(1, divisions + 1):
        # add horizontal resistor from here to the right
        if x + 1 <= divisions:
            file.write(("R%d %d %d %d\n" % (resistor_id, array[y-1,x-1], array[y-1,x],x_Resistance)))
            # print ("R%d %d %d 1" % (resistor_id, array[y-1,x-1], array[y-1,x]))
            resistor_id += 1
        # add vertical resistor from here downward
        if y + 1 <= divisions:
            file.write ("R%d %d %d %d\n" % (resistor_id, array[y-1,x-1], array[y,x-1],y_Resistance))
            # print ("R%d %d %d 1" % (resistor_id, array[y-1,x-1], array[y,x-1]))
            resistor_id += 1

file.write("VIN %d 0 DC 1\n" % vin_node_id)
file.write(".OP\n")
file.write(".END\n")
# print ("VIN %d 0 DC 1" % vin_node_id)
# print (".OP")
# print (".END")
