import math
from math import atan, tan, degrees, radians, pi, sqrt

altitude = 400 #altitude in km
hAspect = 4.0 #horizontal aspect ratio
vAspect = 3.0 #vertical aspect ratio
focal_length = 20 #focal length in mm
sensor_size = 4.0 #sensor size in mm (diagonal)
  
FOV = 2*atan(sensor_size/(2*focal_length)) #FOV calculation using sensor diagonal and focal length

dAspect = sqrt(hAspect*hAspect + vAspect*vAspect) #using pythagorean to find the equivalent diagonal aspect

vFOV = (FOV/dAspect)*vAspect #using ratios of aspects to determine vertical field of view 
hFOV = (FOV/dAspect)*hAspect

hFOV_kmeter= tan(hFOV)*altitude #converting radians into km
vFOV_kmeter= tan(vFOV)*altitude

print"\nvFOV = %.2f deg\nhFOV = %.2f deg\nFOV = %.2f deg\n"% (math.degrees(vFOV), math.degrees(hFOV), math.degrees(FOV))
print"focal length = %.2fmm\nsensor size = %dmm\nthe area is %.2f x %.2f km\n"% (focal_length, sensor_size, hFOV_kmeter, vFOV_kmeter)
  

  
