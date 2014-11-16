#!/usr/bin/python2
#-*- coding: utf-8 -*-
#
# The gsp speed calculator [gsc.py] uses the csv reader to fix nmea strings
#
import csv
import math

class GPSConverter(object):
    '''
    GPS Converter class which is able to perform convertions between the 
    CH1903 and WGS84 system.
    '''
    # Convert CH y/x/h to WGS height
    def CHtoWGSheight(self, y, x, h):
        # Converts militar to civil and to unit = 1000km
        # Axiliary values (% Bern)
        y_aux = (y - 600000) / 1000000
        x_aux = (x - 200000) / 1000000
        # Process height
        h = (h + 49.55) - (12.60 * y_aux) - (22.64 * x_aux)
        return h

    # Convert CH y/x to WGS lat
    def CHtoWGSlat(self, y, x):
        # Converts militar to civil and to unit = 1000km
        # Axiliary values (% Bern)
        y_aux = (y - 600000) / 1000000
        x_aux = (x - 200000) / 1000000
        # Process lat
        lat = (16.9023892 + (3.238272 * x_aux)) + \
                - (0.270978 * pow(y_aux, 2)) + \
                - (0.002528 * pow(x_aux, 2)) + \
                - (0.0447 * pow(y_aux, 2) * x_aux) + \
                - (0.0140 * pow(x_aux, 3))
        # Unit 10000" to 1 " and converts seconds to degrees (dec)
        lat = (lat * 100) / 36
        return lat

    # Convert CH y/x to WGS long
    def CHtoWGSlng(self, y, x):
        # Converts militar to civil and to unit = 1000km
        # Axiliary values (% Bern)
        y_aux = (y - 600000) / 1000000
        x_aux = (x - 200000) / 1000000
        # Process long
        lng = (2.6779094 + (4.728982 * y_aux) + \
                + (0.791484 * y_aux * x_aux) + \
                + (0.1306 * y_aux * pow(x_aux, 2))) + \
                - (0.0436 * pow(y_aux, 3))
        # Unit 10000" to 1 " and converts seconds to degrees (dec)
        lng = (lng * 100) / 36
        return lng

    # Convert decimal angle (degrees) to sexagesimal angle (degrees, minutes
    # and seconds dd.mmss,ss)
    def DecToSexAngle(self, dec):
        degree = int(math.floor(dec))
        minute = int(math.floor((dec - degree) * 60))
        second = (((dec - degree) * 60) - minute) * 60
        # Output: dd.mmss(,)ss
        return degree + (float(minute) / 100) + (second / 10000)
		
    # Convert sexagesimal angle (degrees, minutes and seconds dd.mmss,ss) to seconds
    def SexAngleToSeconds(self, dms):
        degree = 0 
        minute = 0 
        second = 0
        degree = math.floor(dms)
        minute = math.floor((dms - degree) * 100)
        second = (((dms - degree) * 100) - minute) * 100
        # Result in degrees sex (dd.mmss)
        return second + (minute * 60) + (degree * 3600)

    # Convert sexagesimal angle (degrees, minutes and seconds "dd.mmss") to decimal angle (degrees)
    def SexToDecAngle(self, dms):
        # Extract DMS
        # Input: dd.mmss(,)ss
        degree = 0
        minute = 0
        second = 0
        degree = math.floor(dms)
        minute = math.floor((dms - degree) * 100)
        second = (((dms - degree) * 100) - minute) * 100
        # Result in degrees dec (dd.dddd)
        return degree + (minute / 60) + (second / 3600)
    
    # Convert WGS lat/long (° dec) and height to CH h
    def WGStoCHh(self, lat, lng, h):
        # Converts degrees dec to sex
        lat = self.DecToSexAngle(lat)
        lng = self.DecToSexAngle(lng)
        # Converts degrees to seconds (sex)
        lat = self.SexAngleToSeconds(lat)
        lng = self.SexAngleToSeconds(lng)
        # Axiliary values (% Bern)
        lat_aux = (lat - 169028.66) / 10000
        lng_aux = (lng - 26782.5) / 10000
        # Process h
        h = (h - 49.55) + (2.73 * lng_aux) + (6.94 * lat_aux)
        return h

    # Convert WGS lat/long (° dec) to CH x
    def WGStoCHx(self, lat, lng):
        # Converts degrees dec to sex
        lat = self.DecToSexAngle(lat)
        lng = self.DecToSexAngle(lng)
        # Converts degrees to seconds (sex)
        lat = self.SexAngleToSeconds(lat)
        lng = self.SexAngleToSeconds(lng)
        # Axiliary values (% Bern)
        lat_aux = (lat - 169028.66) / 10000
        lng_aux = (lng - 26782.5) / 10000
        # Process X
        x = ((200147.07 + (308807.95 * lat_aux) + \
            + (3745.25 * pow(lng_aux, 2)) + \
            + (76.63 * pow(lat_aux,2))) + \
            - (194.56 * pow(lng_aux, 2) * lat_aux)) + \
            + (119.79 * pow(lat_aux, 3))
        return x

	# Convert WGS lat/long (° dec) to CH y
    def WGStoCHy(self, lat, lng):
        # Converts degrees dec to sex
        lat = self.DecToSexAngle(lat)
        lng = self.DecToSexAngle(lng)
        # Converts degrees to seconds (sex)
        lat = self.SexAngleToSeconds(lat)
        lng = self.SexAngleToSeconds(lng)
        # Axiliary values (% Bern)
        lat_aux = (lat - 169028.66) / 10000
        lng_aux = (lng - 26782.5) / 10000
        # Process Y
        y = (600072.37 + (211455.93 * lng_aux)) + \
            - (10938.51 * lng_aux * lat_aux) + \
            - (0.36 * lng_aux * pow(lat_aux, 2)) + \
            - (44.54 * pow(lng_aux, 3))
        return y

    def LV03toWGS84(self, east, north, height):
        '''
        Convert LV03 to WGS84 Return a array of double that contain lat, long,
        and height
        '''
        d = []
        d.append(self.CHtoWGSlat(east, north))
        d.append(self.CHtoWGSlng(east, north))
        d.append(self.CHtoWGSheight(east, north, height))
        return d
        
    def WGS84toLV03(self, latitude, longitude, ellHeight):
        '''
        Convert WGS84 to LV03 Return an array of double that contaign east,
        north, and height
        '''
        d = []
        d.append(self.WGStoCHy(latitude, longitude))
        d.append(self.WGStoCHx(latitude, longitude))
        d.append(self.WGStoCHh(latitude, longitude, ellHeight))
        return d

class GPRMC(object):
    ''' Data object to store the nmea string. 

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
    TIME    = 0  # Timestamp
    VAL     = '' # Validity 
    LAT     = 0  # Current latitude
    LAT_NS  = '' # Direciton of latitude [N or S]
    LON     = 0  # Current longitude
    LON_EW  = '' # Direction of longitude [E or W]
    SPEED   = 0  # Current speed
    COURSE  = 0  # Current course
    DATE    = 0  # Datestamp
    VAR     = 0  # Variation
    VAR_EW  = '' # Direction of the Variation [E or W]
    CHECK   = '' # Checksum

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
        for words in gprmc:
            for j, word in enumerate(words.split(',')):
                if(j == 1 and word):
                    self.TIME = int(round(float(word)))
                if(j == 2):
                    self.VAL = word
                if(j == 3 and word):
                    lat = float(word)
                    lat = lat/100
                    self.LAT = lat
                if(j == 4):
                    self.LAT_NS = word
                if(j == 5 and word):
                    lon = float(word)
                    lon = lon/100
                    self.LON = lon
                if(j == 6):
                    self.LON_EW = word
                if(j == 7 and word):
                    self.SPEED = float(word)
                if(j == 8 and word):
                    self.COURSE = float(word)
                if(j == 9 and word):
                    self.DATE = int(word)
                if(j == 10 and word):
                    self.VAR = float(word)
                if(j == 11):
                    self.VAR_EW = word
                if(j == 12):
                    self.CHECK = word
    
    def generateGPRMC(self):
        ''' Generate the objects gprmc sentence. '''
        gprmc = ''
        gprmc += "$GPRMC"
        gprmc += ','
        gprmc +=  str(self.getTime())
        gprmc += ','
        gprmc +=  str(self.getValidity())
        gprmc += ','
        gprmc +=  str(self.getLatitude())
        gprmc += ','
        gprmc +=  str(self.getDirectionOfLatitude())
        gprmc += ','
        gprmc +=  str(self.getLongitude())
        gprmc += ','
        gprmc +=  str(self.getDirectionOfLongitude())
        gprmc += ','
        gprmc +=  str(self.getSpeed())
        gprmc += ','
        gprmc +=  str(self.getCourse())
        gprmc += ','
        gprmc +=  str(self.getDate())
        gprmc += ','
        gprmc +=  str(self.getVariation())
        gprmc += ','
        gprmc +=  str(self.getDirectionOfVariation())
        gprmc += ','
        gprmc +=  str(self.getChecksum())
        return gprmc

if __name__ == "__main__":
    converter = GPSConverter()
    data = []
    
    # Read file
    inputfile = "Test.csv"
    outputfile = "Out.csv"
    lines = csv.reader(open(inputfile, 'r'))

    # Generate a List of filled GPRMC objects
    for i, line in enumerate(lines):
        data.append(GPRMC())
        data[i].parseGPRMC(line)
    
    # Open a new csv file and write [time,lat,lon] to it.    
    with open(outputfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Iterate over each object in the list
        for stuff in data:
            print "[DEBUG]: " + stuff.generateGPRMC()
            data = converter.WGS84toLV03(stuff.getLatitude(), stuff.getLongitude(), 0)
            writer.writerow([stuff.getTime(), data[0], data[1]])
