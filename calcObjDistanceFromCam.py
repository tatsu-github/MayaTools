# calculate distance from camera 
# using focal length and horizontal aperture, object height
from maya import cmds
import math

cam = 'renderCam'
obj_height = 0.085

# if get obj_height from bounding box size
obj_name = 'target_name'
min_val = cmds.getAttr(obj_name + '.boundingBoxMin')
max_val = cmds.getAttr(obj_name + '.boundingBoxMax')
obj_height = abs(min_val[0][1]) + abs(max_val[0][1])

f_length = cmds.getAttr(cam+'.focalLength')
h_aperture = cmds.getAttr(cam+'.horizontalFilmAperture')
aov = math.degrees(2 * math.atan((h_aperture * 25.4 * 0.5) / f_length))
tangent = math.tan(math.radians(aov / 2))
distance = obj_height/tangent
