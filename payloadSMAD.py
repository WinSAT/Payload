import satellite
from math import atan, asin, acos, sin, cos, tan, degrees, radians, pi, sqrt
import numpy as np

EARTH_RADIUS = 6378.14e3 #[m]

FireSatParams = {
	'altitude': 700.0e3, #[m]
	'nadirAngleMaxDeg': 57.9, #eta [deg] - max target range from sat to off-nadir target
	'alongTrackGSD_ECAMax': 68.0, #Y_max [m] - max along-track Ground Sampling Distance; design param
	'pixelBitEncodeNum': 8, #B [num] - num of bits used to encode each pixel

}

WinSATParams = {
	'altitude': 500.0e3, #[m]
	'nadirAngleMaxDeg': 25.0, #eta [deg] - max target range from sat to off-nadir target
	'alongTrackGSD_ECAMax': 50.0, #Y_max [m] - max along-track Ground Sampling Distance @ ECAMax; design param
}

FireSat = satellite.Satellite(FireSatParams)
FireSat.set(calculateOrbitalParamters(FireSat.altitude))

def calculateOrbitalParamters(sat):
	#circular orbit - in mins
	results = {}
	results["orbitalPeriod"] = (1.658669e-4)*(6378.14+sat.altitude)**(1.5) #p [mins]
	results["angularVelocity"] = 6.0/results["orbitalPeriod"] #omega [deg/s] ; <= 0.071 deg/s (max angular vel for circular orbit)
	results["groundTrackVelocity"] = 2*np.pi*EARTH_RADIUS/results['orbitalPeriod'] #V_g [m/s] ; <= 7905.0 m/s for circular orbit
	results["nodeShift"] = (results['orbitalPeriod']/1436.0)*360.0 #dL [deg] - spacing between sucessive node crossings on the equator
	return results

def calculateSensorViewingParams(sat):
	#TODO: This func assumes spherical model of earth, eventually will use earthOblatenessModel()
	results = {}
	results["earthAngularRadius"] = np.arcsin(EARTH_RADIUS/(EARTH_RADIUS+sat.altitude)) #p [rad] - angular radius of spherical earth wrt spacecraft pov
	results["maxHorizonDistance"] = EARTH_RADIUS*np.tan(np.deg2rad(90.0)-results['earthAngularRadius']) #D_max [m] - distance to horizon
	results["elevationAngleMin"] = np.arccos(np.sin(np.deg2rad(sat.nadirAngleMaxDeg)) / np.sin(results["earthAngularRadius"])) #epsilon_min [rad] - at target between spacecraft and local horizontal
	results["incidenceAngleMax"] = (np.pi/2) - results['elevationAngleMin']
	results["earthCentralAngle"] = (np.pi/2) - np.deg2rad(sat.nadirAngleMaxDeg) - results['elevationAngleMin'] #lambda [rad] - at center of earth from subsatellite point to nadirMax
	results["distanceToMaxOffNadir"] = EARTH_RADIUS*np.sin(results['earthCentralAngle'])/np.sin(np.deg2rad(sat.nadirAngleMaxDeg)) #Dn_max [m] - i.e. Slant range; distance from satellite to max off-nadir target
	results["swathWidthAngle"] = 2*results['earthCentralAngle'] #[rad] - determines coverage
	return results

def calculatePixelDataParams(sat):
	results = {}
	results["IFOV"] = sat.alongTrackGSDMax / sat.distanceToMaxOffNadir #IFOV [rad] - Instantaneous Field of View; one pixel width
	results["acrossTrackGSD_ECAMax"] = sat.alongTrackGSD_ECAMax / np.cos(sat.incidenceAngleMax) #X_max [m] - max across-track Ground Sampling Distance @ ECAMax
	results["acrossTrackGSD_Nadir"] = sat.IFOV * sat.altitude #X [m] - across-track Ground Sampling Distance @ Nadir
	results["alongTrackGSD_Nadir"] = sat.IFOV * sat.altitude #Y [m] - along-track Ground Sampling Distance @ Nadir
	results["crossTrackPixelNum"] = 2*np.deg2rad(sat.nadirAngleMaxDeg)/results['IFOV'] #Z_c [num] - num of across-track pixels
	results["alongTrackSwathNumRate"] = sat.groundTrackVelocity / results['alongTrackGSD_Nadir'] #Z_a [num/s] - num of swaths recorded per sec
	results["pixelRecordRate"] = results['crossTrackPixelNum'] * results['alongTrackSwathNumRate'] #Z [num/s] - num of pixels recorded per sec
	results["dataRate"] = results['pixelRecordRate'] * sat.pixelBitEncodeNum #DR [Mbps] - data rate
	return results




def earthOblatenessModeling(satVectorEFF):
	f = 1/298.257 # f - earth flattening factor ; f = (R_e - R_p) / R_e : R_e (equatorial radius) ~ 6378.140, R_p (polar radius)
	a = np.sqrt(np.dot(satVectorEFF**2,[1,1,(1 - earthFlattening)**2])) #a - equatorial radius, c - polar radius
	#lat (lambda), long (phi) = geocentric lat, long of the observers (sats) position
	#azi = azimuth angle of the horizon vector
	R = a*(1-f) / np.sqrt(1 - (2 - f)*f*np.cos(lat)**2) #Earth Radius to local surface
	d = np.linalg.norm(satVectorEFF) #distance from earth center to satellite in EFF
	term1 = (((d**2 - R**2)/a**2)*(1 + ((2-f)*f*R**2*np.cos(lat)**2*np.sin(azi)**2 / (1-f)**2*a**2)))**0.5
	earthAngularRadius = 1.0 / np.arctan(term1 + ((2-f)*f*R**2*np.sin(azi) / 2*(1-f)**2)*a**2)
	'''
	H = np.sqrt(np.sum(satVectorEFF**2)-a**2) #init estimate (assumes spherical earth)
	#iteratively compute max distance to horizon
	for n in range(10):
		H = np.sqrt(np.sum([]))
	'''



#Focal length and sensor parameters
altitude = 500 #altitude in km
sensorSize = 4.0 #sensor size in mm
vAspect = 3.0 #vertical aspect of sensor mm
hAspect = 4.0
lensFormat = 6.0 #lens format in mm
imageR = (sensorSize/2.0)/1000 #imaging radius in m(of sensor)
focalLength = 0.016 #focal length in m
groundRadius = (imageR*(altitude*1000))/focalLength #max ground radius in m (cicular)
dectectorArea = pi*(imageR**2) #area of sensor
fovDiameter = 2*atan(imageR/focalLength) #angular diameter of FOV in radians
areaG = pi*(groundRadius**2) #ground object FOV in m squared (circular)
diagonalLength = (sensorSize/lensFormat)*(2*(groundRadius/1000)) #ground radius adjusted for sensor size and lens radius 
ratio = diagonalLength/(sensorSize/1.0E6) #finding ratio of area to sensor hypotenous
sensorDiagonal = sqrt((hAspect**2)+(vAspect**2)) #finding sensor diagonal
sensorRatio = sensorSize/sensorDiagonal #the ratio of the given sensor size to the ratio based on its aspects
sensorH = hAspect*sensorRatio
sensorV = vAspect*sensorRatio
horizontalArea = ratio*(sensorH/1.0E6)
verticalArea = ratio*(sensorV/1.0E6)

print ("\nSensor size is {:.2f} mm".format(sensorSize))
print ("Focal length is {:.2f} mm".format(focalLength*1000))
print ("Ground radius is {:.2f} km".format(groundRadius/1000))
print ("The ground area taken by sensor is {:.2f} x {:.2f} km".format(horizontalArea, verticalArea))


#orbit and earth area parameters
latitudeSSP = 42.0 # enter latitude of sub-satellite point
longitudeSSP =-83.0 
latitudeTarget = 42.312659 # enter latitude of target
longitudeTarget = -83.056033
radiusE = 6378.14 #earth radius in KM
orbitP = (1.658669E-4)*(sqrt((radiusE+altitude)**3)) #orbit time in min
velocityG = (2*pi*radiusE)/(orbitP*60) #ground velcity in km/s
angularR = asin(radiusE/(radiusE+altitude)) #angular radius of earth (p)
horizonMax= sqrt(((radiusE+altitude)**2)-(radiusE**2)) #max horizontal distance/ without focal lenght and sensor constraint
earthAngularR = 90 - math.degrees(angularR) 
angularTarget = acos(sin(latitudeSSP)*sin(latitudeTarget)+cos(latitudeSSP)*cos(latitudeTarget)*cos(longitudeSSP-longitudeTarget))# angle calc from earth center to target
maxLook = atan((sin(angularR)*sin(angularTarget))/(1-sin(angularR)*cos(angularTarget))) #max angular field, without sensor and coal length contraint, to target from satellite
elevation = acos(sin(maxLook)/sin(angularR)) #elevation angle
ecaMax = 90 - math.degrees(elevation) - math.degrees(maxLook) #earth central angle maximum
slantRange = radiusE*(sin(angularTarget)/sin(maxLook)) #slant range to target
IA = 90 - math.degrees(elevation) # incident angle
yMax = 150 #along tack ground sampling distance, not sure where to find this value, in m
xMax = yMax/cos(IA) #across track ground sampling

print ("\nOrbit time is {:.2f} min".format(orbitP))
print ("Ground velocity is {:.2f} km/s".format(velocityG))
print ("Elevation is {:.2f} deg for entered target".format(math.degrees(elevation)))
print ("Incident angle is {:.2f} deg for entered target".format(IA))

#instantaneous field of view and data rate parameters
numberPixel = 256 #number of pixels for integration (unsure where to get this value)
pixelWidth = 30E-6 #specify width for square dectors, micro meters
Q = 1; #specify image quality, 1 is standard
opWavelength = 4.2E-6 #specify operating wavelength in micrometers
aperatureD = 0.0024 #aperature in m
nbits = 8 #enter number of bits
iFOV = (yMax/1000.0)/slantRange #instantaneous fov
Y = math.degrees(iFOV)*(math.degrees(angularR)) #best track resolution
zC = (2*math.degrees(maxLook))/math.degrees(iFOV) #ground pixel size
zA = velocityG/Y #number of swaths without gaps at nadir 
z = zC*zA # pixels recorded in one second
dataRate = (z*nbits)/(1E6) #data rate in Mbps
pixelInt = (Y/velocityG)*(numberPixel/zC) #pixel integration time
pixelSize = ((2.44*opWavelength*focalLength)/aperatureD)*Q #pixel size in m

print ("\nNumber of bits is {}".format(nbits))
print ("Data rate is {:.2f} Mbps".format(dataRate))
print ("Pixel size is {:.2f} micrometer".format(pixelSize*100000))



