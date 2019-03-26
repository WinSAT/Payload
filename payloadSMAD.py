import math
from math import atan, asin, acos, sin, cos, tan, degrees, radians, pi, sqrt

#Focal length and sensor parameters
altitude = 500 #altitude in km
sensorSize = 4 #sensor size in mm
imageR = (sensorSize/2.0)/1000 #imaging radius in m(of sensor)
focalLength = 0.025 #focal length in m
groundRadius = (imageR*(altitude*1000))/focalLength #max ground radius in m (cicular)
dectectorArea = pi*(imageR**2) #area of sensor
fovDiameter = 2*atan(imageR/focalLength) #angular diameter of FOV in radians
areaG = pi*(groundRadius**2) #ground object FOV in m squared (circular)

print ("\nSensor size is {:.2f} mm".format(sensorSize))
print ("\nFocal length is {:.2f} mm".format(focalLength*1000))
print ("\nGround radius is {:.2f} km".format(groundRadius/1000))
print ("\nCicular ground are is {:.2f} km squared".format(areaG/1E6))

#orbit and earth area parameters
radiusE = 6378.14 #earth radius in KM
orbitP = (1.658669E-4)*(sqrt((radiusE+altitude)**3)) #orbit time in min
velocityG = (2*pi*radiusE)/(orbitP*60) #ground velcity in km/s
angularR = asin(radiusE/(radiusE+altitude)) #angular radius of earth (p)
horizonMax= sqrt(((radiusE+altitude)**2)-(radiusE**2)) #max horizontal distance/ without focal lenght and sensor constraint
earthAngularR = 90 - math.degrees(angularR) 
latitudeSSP = 42.0 # latitude of sub-satellite point
longitudeSSP =-83.0 
latitudeTarget = 42.312659 #latitude of target
longitudeTarget = -83.056033
angularTarget = acos(sin(latitudeSSP)*sin(latitudeTarget)+cos(latitudeSSP)*cos(latitudeTarget)*cos(longitudeSSP-longitudeTarget))# angle calc from earth center to target
maxLook = atan((sin(angularR)*sin(angularTarget))/(1-sin(angularR)*cos(angularTarget))) #max angular field, without sensor and coal length contraint, to target from satellite
elevation = acos(sin(maxLook)/sin(angularR)) #elevation angle
ecaMax = 90 - math.degrees(elevation) - math.degrees(maxLook) #earth central angle maximum
slantRange = radiusE*(sin(angularTarget)/sin(maxLook)) #slant range to target
IA = 90 - math.degrees(elevation) # incident angle
yMax = 150 #along tack ground sampling distance, not sure where to find this value, in m
xMax = yMax/cos(IA) #across track ground sampling

print ("\nOrbit time is {:.2f} min".format(orbitP))
print ("\nGround velocity is {:.2f} km/s".format(velocityG))
print ("\nElevation is {:.2f} deg for entered target".format(math.degrees(elevation)))
print ("\nIncident angle is {:.2f} deg for entered target".format(IA))

#instantaneous field of view and data rate parameters
iFOV = (yMax/1000.0)/slantRange #instantaneous fov
Y = math.degrees(iFOV)*(math.degrees(angularR)) #best track resolution
zC = (2*math.degrees(maxLook))/math.degrees(iFOV) #ground pixel size
zA = velocityG/Y #number of swaths without gaps at nadir 
z = zC*zA # pixels recorded in one second
nbits = 8 #enter number of bits
dataRate = (z*nbits)/(1E6) #data rate in Mbps
numberPixel = 256 #number of pixels for integration (unsure where to get this value)
pixelInt = (Y/velocityG)*(numberPixel/zC) #pixel integration time
pixelWidth = 30E-6 #specify width for square dectors, micro meters
Q = 1; #specify image quality, 1 is standard
opWavelength = 4.2E-6 #specify operating wavelength in micrometers
aperatureD = 0.0024 #aperature in m
pixelSize = ((2.44*opWavelength*focalLength)/aperatureD)*Q #pixel size in m

print ("\nNumber of bits is {}".format(nbits))
print ("\nData rate is {:.2f} Mbps".format(dataRate))
print ("\nPixel size is {:.2f} micrometer".format(pixelSize*100000))



