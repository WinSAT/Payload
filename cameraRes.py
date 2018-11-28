resolution  = 20.0   #: desired resolution in meters per pixel
sensor_size =   5.0   #: mm (ignore aspect ratio)
altitude    = 500e3   #: CubeSat altitude in meters

from numpy import *

satellite = {
	"altitude": 400e3,
	"cameraArea": 40e3, #area of image
}

camera = {
	"sizeOfSensor": 1.19e-6, #one pixel
	"focalLength": 4.02e-3, #lens
	"resolutions": [[1920,1080],[2560,1440],[3840,2160]]

}

from math import atan, tan, degrees

print 

IFOV = 2.0*arctan2(camera['sizeOfSensor']*4,(2*camera['focalLength']))

featureSize = 2.0*satellite['altitude']*tan((IFOV/3600.0)/2.0)


print IFOV, featureSize
# some common camera resolutions
pixelcount = [2**10, 2**11, 2**12] # 1 MP to 16 MP

'''
# nessisary IFOV for given resolution
ifov = 2 * atan(satellite['resolution']/(2*satellite['altitude']))

print "**Camera specs for seeing at %0.0f m/px**\n" % (resolution)
print " Camera resolution | Pixel Size [&mu;m] | Focal Length [mm] | FOV [&deg;] | 35 mm equiv. Lens "
print " ----------------- | -----------------: | ----------------: | ----------: | ----------------: "
for res in pixelcount:
    pixel_size = sensor_size / float(res)
    focal_length = pixel_size / (2*tan(ifov/2.0))
    fov = 2 * atan(sensor_size / (2*focal_length))
    film = 36 / (2*tan(fov/2.0))
    
    print """  %d&times;%d  | %18.2f | %17.1f | %11.1f | %14.0f mm
""" % (res, res, pixel_size*1000, focal_length, degrees(fov), film),
'''