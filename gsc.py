#!/usr/bin/python2
#
# The gsp speed calculator [gsc.py] uses the csv reader to fix nmea strings
#
import csv

class GPRMC(object):
    ''' Data object to temporary store the nmea string. 

	Explenation of the GPRMC NMEA Data string:
	$GPRMC,220516,A,5133.82,N,00042.24,W,173.8,231.8,130694,004.2,W*70
    	      1   2    3    4   5      6    7    8    9     10    11 12
	1   220516     Time Stamp
	2   A          validity - A-ok, V-invalid
	3   5133.82    current Latitude
	4   N          North/South
	5   00042.24   current Longitude
	6   W          East/West
	7   173.8      Speed in knots
	8   231.8      True course
	9   130694     Date Stamp
	10  004.2      Variation
	11  W          East/West
	12  *70        checksum
    '''
    
    # Object Fields
    TIME    = 0 # Timestamp
    VAL     = ''# Validity 
    LAT     = 0 # Current latitude
    LAT_NS  = ''# Direciton of latitude [N or S]
    LON     = 0 # Current longitude
    LON_EW  = ''# Direction of longitude [E or W]
    SPEED   = 0 # Current speed
    COURSE  = 0 # Current course
    DATE    = 0 # Datestamp
    VAR     = 0 # Variation
    VAR_EW  = 0 # Direction of the Variation [E or W]
    CHECK   = 0 # Checksum

    # Get/Set functions 
    def setTime(self, time):
        self.TIME = time
    def getTime(self):
        return self.TIME

    def setValidity(self, val):
        self.VAL = val
    def getValidity(self):
        return self.VAL

    def setLatitude(self, lat):
        self.LAT = lat
    def getLatitude(self):
        return self.LAT

    def setDirectionOfLatitude(self, latns):
        self.LAT_NS = latns
    def getDirectionOfLatitude(self):
        return self.LAT_NS

    def setLongitude(self, lon):
        self.LON = lon
    def getLongitude(self):
        return self.LON

    def setDirectionOfLongitude(self, lonew):
        self.LON_EW = lonew
    def getDirectionOfLongitude(self):
        return self.LON_EW

    def setSpeed(self, speed):
        self.SPEED = speed
    def getSpeed(self):
        return self.SPEED

    def setCourse(self, course):
        self.COURSE = course
    def getCourse(self):
        return self.COURSE

    def setDate(self, date):
        self.DATE = date
    def getDate(self):
        return self.DATE

    def setVariation(self, var):
        self.VAR = var
    def getVariation(self):
        return self.VAR

    def setDirectionOfVariation(self, varew):
        self.VAR_EW = varew
    def getDirectionOfVariation(self):
        return self.VAR_EW

    def setChecksum(self, checksum):
        self.CHECK = checksum
    def getChecksum(self):
        return self.CHECK

    # Helper functions
    def parseGPRMC(self, gprmc):
        ''' Parses a gprmc string an sets the objects values accordingly.'''

    def generateGPRMC(self):
        ''' Generate the objects gprmc sentence. '''
        return gprmc

if __name__ == "__main__":
    try:
	Testfile="/home/aaron/GPS_ZUGKRAFTMESSUNG/20140910_Guellen/GPS_Guellen.txt"
	sentences = csv.reader(open(Testfile, 'r'))
	
	# for each line in the file
	for line in sentences:
		# if the line isn't empty and begins with '$GPRMC' 
    		if line and line[0].strip() == '$GPRMC':
        		for word in line:
        			print word
        		print "_____________________"

    except Exception as e:
        print e
    finally:
        print "[DEBUG]: Cleanup done, exiting."


