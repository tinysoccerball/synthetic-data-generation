import math
import numpy as np
import json
from scipy.spatial import distance

#Implement a smarter filepath location system. For now they are hard coded
cube = "C:\\Users\\jpbg2\\OneDrive\\Documents\\cube.obj"
female_face = "C:\\Users\\jpbg2\\OneDrive\\Documents\\NoseProject\\Sample3D\\Sample3D\\female_head_1.obj"
jso = "C:\\Users\\jpbg2\\OneDrive\\Documents\\NoseProject\\OguzhanTopsakal\\OguzhanTopsakal.JSON"

#rewrite this entire thing. 
# Immediatelety split, look at first element to determine line and then append the rest
vlines = []
vtlines = []
vnlines  = []
flines= []
glines= []
usemtl = ""
commentlines = []
olines = []
mlines = ""
with open(cube) as file:
    obj = file.readlines()
    for line in obj:
        if line[0] == "v":
            if line[1] == " ":
                vlines.append(line[2:])
            if line[1] == "t":
                vtlines.append(line[3:])
            if line[1] == "n":
                vnlines.append(line[3:])
        if line[0] == "f":
            flines.append(line[2:])
        if line[0] == "g":
            glines.append(line[2:])
        if line[0] == "#":
            commentlines.append(line[2:])
        if line[0] == "u":
            usemtl = line[7:]
        if line[0] == "o":
            olines.append(line[2:])
        if line[0] == "m":
            mlines = (line[6:])

newv = []
for line in vlines:
    line = line[:-2]
    line = line.split()
    newv.append(line)
newv = np.array(newv)
vlines = newv.astype(float)

newvt = []
for line in vtlines:
    line = line[:-2]
    line = line.split()
    newvt.append(line)
newvt = np.array(newvt)
vtlines = newvt.astype(float)

newvn = []
for line in vnlines:
    line = line[:-1]
    line = line.split()
    newvn.append(line)
newvn = np.array(newvn)
vnlines = newvn.astype(float)
'''
print("VLINES")
print("_______________")
print(vlines)
print("VNLINES")
print("_______________")
print(vnlines)
print("VTLINES")
print("_______________")
print(vtlines)
print("JSON")
print("_______________")
'''
with open(jso, encoding = 'utf-8') as f:
        face_data = json.load(f)

jso_rows = []

for feature in face_data["features"]:
        jso_rows.append((feature["xVal"], feature["yVal"], feature["zVal"]))

jso_rows = np.array(jso_rows)
#print(jso_rows)

#this takes the points and compares their distance to the landmark. Closest point to the landmark is added to selected points.
#There are faster ways to calculate this. Currently prety inefficient but not too bad.
selected_points = []
index_array = []
my_array = np.array([])
#print("Results")
for landmark_point, landmark in enumerate(jso_rows):
    dist = float('inf')
    for index, point in enumerate(vlines):
        i = distance.euclidean(landmark, point)
        if i < dist:
            dist = i
            holding = index
    selected_points.append(holding)
    index_array.append(vlines[holding])
    newline = [index_array, *point]
    np.append(my_array, index_array)
'''
print(len(vlines))
print(len(obj))
print(len(jso_rows))
print(len(selected_points))
print(selected_points)
print(flines)
'''

#this is the actual vertex manipulation. We are moving the second vertex's along the y axis by a value of -2. Very basic stuff here
vlines[1][1] -= 2

def makefile():
    with open ("C:/Users/jpbg2/OneDrive/Documents/NoseProject/newfile.obj", 'w') as outfile:
        for line in commentlines:
            outfile.write('# ' + line)
        outfile.write("mtllib " + mlines)
        for line in olines:
            outfile.write('o ' + str(line))
        for line in vlines:
            #outfile.write('v', str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[2]) + '\n')
            outfile.write("v {} {} {}\r".format(str(format(line[0], '.6f')), str(format(line[1], '.6f')), str(format(line[2], '.6f'))))
        for line in vtlines:
            #outfile.write('vt', str(line[0]) + ' ' + str(line[1]) + '\n')
            outfile.write("vt {} {}\r".format(str(format(line[0], '.6f')), str(format(line[1], '.6f'))))
        for line in vnlines:
            #outfile.write('vn', str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[2]) + '\n')
            outfile.write("vn {} {} {}\r".format(str(format(line[0], '.6f')), str(format(line[1], '.6f')), str(format(line[2], '.6f'))))
        outfile.write("usemtl " + usemtl)
        outfile.write("s off\n")
        for line in flines:
            outfile.write("f " + line)

#this poor doesnt work like I need it to
def prop_smooth(height, width, x):
    afterwards = []
    offsets = []
    for point in vlines:
        offset = distance.euclidean(x, point)
        offsets.append(offset)
        if offset<=width and offset>=(-width):
            y = (height * (math.cos((offset*math.pi)/width) + 1))/2
        elif offset>width or offset<(-width):
            y = 0
        afterwards.append(y)
    print((offsets))
    return afterwards

xvals = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

makefile()