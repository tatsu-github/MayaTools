# calculate distance from camera 
using focal length and horizontal aperture, object height
from maya import cmds
import math

cam = 'renderCam'
f_length = cmds.getAttr(cam+'.focalLength')
h_aperture = cmds.getAttr(cam+'.horizontalFilmAperture')
aov = (2 * math.atan((h_aperture * 25.4 * 0.5) / f_length)) * 57.29578
tangent = math.tan(math.radians(aov / 2))
obj_height = 0.085
distance = obj_height/tangent
