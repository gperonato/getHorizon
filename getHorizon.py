'''
Get Horizon using Elevation APIs
© All rights reserved. Ecole polytechnique fédérale de Lausanne (EPFL), Switzerland,
Laboratory of Integrated Performance in Design (LIPID), 2017-2018

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of [project] nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Created on 25 Apr 2017. Latest modification: April 21 2018

@author: Giuseppe Peronato, <giuseppe.peronato@epfl.ch>
'''

#Python2 support
from __future__ import (absolute_import, division,
                         print_function, unicode_literals)
from builtins import (
          bytes, dict, int, list, object, range, str,
          ascii, chr, hex, input, next, oct, open,
          pow, round, super,
          filter, map, zip)


import math
import simplejson
import requests
import urllib.parse
import urllib.request
import polyline
import time
import sys, os
import matplotlib.pyplot as plt
import numpy as np
import argparse
from scipy.interpolate import interp1d


#This useful when compiling with Pyinstaller.  Make sure that files are written in the bundle directory.
if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(bundle_dir)

#Default parameters
R = 6371 #Earth radius in Km


def getAPI():
    filename = "API.txt"
    try:
        API_file = open(filename, 'r')
        API = API_file.read()
        API_file.close()
        return API
    except:
        print("API key missing. Please add your Mapquest API key in a file called API.txt located in the tool directory.")
        sys.exit("")
        
def circlePoint(lat,long,angle,d):
    # from http://www.movable-type.co.uk/scripts/latlong.html
    # Destination point given distance and bearing from start point
    φ1 = math.radians(lat)
    λ1 = math.radians(long)
    brng = math.radians(angle)
    φ2 = math.asin( math.sin(φ1)*math.cos(d/R) +
                    math.cos(φ1)*math.sin(d/R)*math.cos(brng) )
    λ2 = λ1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(φ1),
                         math.cos(d/R)-math.sin(φ1)*math.sin(φ2))
    return (math.degrees(φ2), math.degrees(λ2))

def getOpenElevation(locations=""):

	URL = "https://api.open-elevation.com/api/v1/lookup"


	locations2 = []
	for loc in locations:
		dd = {}
		dd["latitude"] = loc[0]
		dd["longitude"] = loc[1]
		locations2.append(dd)
	d = {}
	d["locations"] = locations2

	headers = {'content-type': 'application/json'}
	r = requests.post(URL, json=d, headers=headers)
 
	# extracting data in json format
	results = r.json()["results"]

	elevations = [] 
	for pt in results:
		elevations.append(pt["elevation"])
	time.sleep(0.3)#minimum is 0.3

	return elevations

def getRasterElevation(filename,points):
    import rasterio
    dataset = rasterio.open(filename)
    def getRasterValue(lon,lat,dataset):
        py, px = dataset.index(lon, lat)
        window = rasterio.windows.Window(px - 1//2, py - 1//2, 1, 1)
        clip = dataset.read(window=window)
        value = clip[0][0][0]
        return value
    elevs = []
    for point in points:
        elevs.append(getRasterValue(point[1],point[0],dataset))
    return elevs

    
    
def getMapquestlevations(API,locations=""):
    encoded = polyline.encode(locations, 6)
    encoded = encoded.replace("\\","\\\\")
    url = r'http://open.mapquestapi.com/elevation/v1/profile?key={0}&shapeFormat=cmp6&latLngCollection={1}'.format(API,encoded)
    response = simplejson.load(urllib.request.urlopen(url))
    elevationprofile = response["elevationProfile"]
    elevations = []
    for pt in elevationprofile:
    	elevations.append(pt["height"])
    return elevations

# Mapzen services are discontinued as of January 2018
# def getMapzenElevations(API,locations=""):
#     encoded = polyline.encode(locations, 6)
#     encoded = encoded.replace("\\","\\\\")
#     url = r'https://elevation.mapzen.com/height?json={"range":false,"encoded_polyline":"'+encoded+'"}&api_key=' + API
#     response = simplejson.load(urllib.request.urlopen(url))
#     time.sleep(0.3)#minimum is 0.3
#     return (response["height"])


def getDistance(lat1,lon1,lat2,lon2):
    #http://www.movable-type.co.uk/scripts/latlong.html
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    Δφ = math.radians(lat2-lat1)
    Δλ = math.radians(lon2-lon1)

    a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));

    d = R * c;
    return d


def getElevationAngle(dist,ha,hb):
    #http://stackoverflow.com/questions/29858543/elevation-angle-between-positions/29868556
    if dist != 0:
        theta = dist / R;
        d1 = (R + ha) * math.cos(theta)
        d3 = (R + ha) * math.sin(theta)
        d2 = R + hb - d1;
        alpha = math.atan(d2 / d3) - theta
    else: #The angle between two points with the same coordinates is null
        alpha = 0
    return math.degrees(alpha)


def writeCSV(variable,filename,headers=[],transpose=False):
    if transpose:
        variable = [[row[i] for row in variable] for i in range(len(variable[0]))]
    csv_file = open(filename, 'w')
    if len(headers) > 0:
        csv_file.write(",".join(headers)+"\n")
    for l in range(len(variable)):
        if hasattr(variable[l], '__len__'):
            string = ""
            for p in range(len(variable[l])):
                string += str(variable[l][p])
                if p < len(variable[l])-1:
                    string += ","
        else:
            string = str(variable[l])
        csv_file.write(string+"\n")
    csv_file.close()
    print("File "+filename+" written.")
    
def writeObstructions(directions,hangles,filename):
    csv_file = open(filename, 'w')
    csv_file.write("Obstruction table in SunEye format. It can be imported into SAM.\n")
    csv_file.write("begin data\n")
    csv_file.write("Compass Heading (0-360; North=0; East=90,Elevation (0-90)\n")
    for a in range(len(hangles)):
        csv_file.write(str(directions[a])+","+str(round(hangles[a]))+"\n")
    csv_file.write(str(360)+","+str(round(hangles[0]))+"\n")#repeat North direction at the end
    csv_file.close()
    print("File "+filename+" written. You can import it into SAM as a 'Suneye obstruction table'.")

def plotPolar(direction,values,ylim,title,filename):
    angle = [math.radians(a) for a in direction]
    values.append(values[0])
    angle.append(math.radians(360))
    plt.clf()
    sp = plt.subplot(1, 1, 1, projection='polar')
    sp.set_xticklabels(['N', '', 'E', '', 'S', '', 'W', ''])
    sp.set_xlabel(title)
    sp.set_ylim(ylim)
    sp.set_theta_zero_location('N')
    sp.set_theta_direction(-1)
    sp.plot(angle, values)
    plt.savefig(filename)
    print("Image "+filename+" saved.")

Run = True
if __name__ == '__main__' and Run == True:
    
    print("")
    print("Get Horizon from online elevation services")
    print("")
    print('''This script © All rights reserved.\nEcole polytechnique fédérale de Lausanne (EPFL), Switzerland,\nLaboratory of Integrated Performance in Design (LIPID), 2017-2018''')
    print("Author: Giuseppe Peronato, <giuseppe.peronato@alumni.epfl.ch>")
    print("This script is licensed under the BSD 3-clause license.")
    print("")
    print("")
    print("See terms of use, data sources and complete credits on\nhttps://github.com/gperonato/getHorizon")
    print("")
    print("")
    

    #Initialize data
    hpoints = []
    helev = []
    hdist = []
    
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Create a horizon profile.")
        parser.add_argument("--lat", type=float, help="Latitude (decimal)",default=46.799722)
        parser.add_argument("--long", type=float, help="Longitude (decimal)", default=9.833056)
        parser.add_argument("--height", type=int, 
                             help="Height of the viewpoint with respect to the terrain in m", 
                             default=0)
        parser.add_argument("--dstep", type=float, 
                             help="The spatial resolution", 
                             default=0.1)
        parser.add_argument("--dmax", type=int, help="The range in Km", default=20)
        parser.add_argument("--astep", type=int, help="Angular resolution in degrees", default=20)
        parser.add_argument("--service", choices=['Open-Elevation', 'Mapquest', 'raster'], 
                            help="Name of elevation service (or raster)", default="Mapquest")
        parser.add_argument("--filename", type=str, help="Path to the raster file")
        args = parser.parse_args()
        globals().update(vars(args))
        
    else:
        # Collect the input from the user
        latlong = input('Enter the coordinates (lat,long) of the viewpoint (default is Davos = 46.799722,9.833056) --> ').replace(' ','')
        if not latlong:
            lat = 46.799722
            long = 9.833056
        else:
            lat = float(latlong.split(',')[0])
            long = float(latlong.split(',')[1])
            
        height = input('Enter the height of the viewpoint with respect to the terrain in m (default = 0). --> ')
        if not height:
            height = 0
        else:
            height = int(height)
        
        dstep = input('Enter the spatial resolution in Km (default = 0.1) --> ')
        if not dstep:
            dstep = 0.1
        else:
           dstep = float(dstep) 
            
        dmax = input('Enter the range in Km (default = 20) --> ')
        if not dmax:
            dmax = 20
        else:
            dmax = int(dmax)
            
        astep = input('Enter the angular resolution in degrees (default = 10). Set 1 if you want to output an obstruction table. --> ')
        if not astep:
            astep = 10
        else:
            astep = int(astep)
      	
        service = input('Elevation Service (Open-Elevation, Mapquest, or raster) (default = Mapquest) --> ')
        if not service:
            service = "Mapquest"
    
    
      	#Get API
        if service == "Mapquest":
            API = getAPI()
            
      	#Get rSRTM aster
        if service == "raster":
            filename = input('Enter the path to the SRTM raster. --> ')
        print(filename)
    
    
    #Start of script
    print("\nCalculating horizon line for {},{} \nHeight: {}\nSpatial resolution: {} Km\nRange: {} Km\nAngular resolution: {}°\n".format(lat,long,height,dstep,dmax,astep))
    
    
    #Loop over each path
    #Calls for Mapzen API 
    #Keeps in memory all the points of the path
    dpoints = []
    delevs = []
    ddists = []
    directions = []
    APIcalls = 0
    
    for angle in range(0,360,astep):
        print("Retrieving elevation data for azimuth "+str(angle)+"°")
        directions.append(angle)
        points = []
        elevs = []
        dists = []
        for dist in range(0,int(dmax*1000),int(dstep*1000)):
            points.append(circlePoint(lat,long,angle,dist/1000))
        APIcalls += 1
        if service == "Mapquest":
        	elevs = getMapquestlevations(API,points)
        elif service == "Open-Elevation":
        	elevs = getOpenElevation(points)
        elif service == "raster":
        	elevs = getRasterElevation(filename,points)
        #elevs = getMapzenElevations(API,points)
        for p in range(len(points)):
            dists.append(getDistance(lat,long,points[p][0],points[p][1]))
        dpoints.append(points)
        delevs.append(elevs)
        ddists.append(dists)
    
    #Keep only the points with maximum elevation angle
    hangles = []
    hlat = []
    hlong = []
    #ha = getGoogleElevation(str(lat)+','+str(long))/1000 #elevation of viewpoint in Km
    APIcalls += 1
    #ha = (getMapzenElevations(API,[(lat,long)])[0] + height)/1000
    if service == "Mapquest":
    	ha = (getMapquestlevations(API,[(lat,long)])[0] + height)/1000
    elif service == "Open-Elevation":
    	ha = (getOpenElevation([(lat,long)])[0] + height)/1000
    elif service == "raster":
    	ha = (getRasterElevation(filename,[(lat,long)])[0] + height)/1000

    print("Calculating horizon line from elevation data")
    for a in range(len(ddists)): #for each bearing
        angle = []
        for b in range(0,len(ddists[a])): #for each point of the path with that bearing angle
            hb = delevs[a][b]/1000 #Elevation of point in Km
            alpha = getElevationAngle(ddists[a][b], ha, hb)
            angle.append(alpha)
        maxindex = angle.index(max(angle)) #Index of point with maximum elevation angle
        hangles.append(angle[maxindex])
        hpoints.append(dpoints[a][maxindex])
        hlat.append(dpoints[a][maxindex][0])
        hlong.append(dpoints[a][maxindex][1])
        helev.append(delevs[a][maxindex])
        hdist.append(ddists[a][maxindex])
    
    #Output
    print("\nThe Elevation Service has been called {} times. Beware that there might a limit in requests.\n".format(APIcalls))
    results = [directions]+[hlat]+[hlong]+[hangles]+[helev]+[hdist]
    headers = ["azimuth","latitude","longitude","elevation angle","elevation","distance"]
    writeCSV(results,'horizon.csv',headers,True)
    
    
    if len(directions) == 360:
        writeObstructions(directions,hangles,"obstruction-table.csv")
    else: #interpolate 
        x = np.empty(max(directions)+1)
 
        x[:] = np.NAN
 
        x[directions] = hangles
 
        not_nan = np.logical_not(np.isnan(x))
        indices = np.arange(len(x))
        interp = interp1d(indices[not_nan], x[not_nan])
        writeObstructions(indices,interp(indices),"obstruction-table-interp.csv")
        
    #Plot  
    plotPolar(directions,hangles,45,"Elevation angle [°]","elevation-angle.pdf")
    plotPolar(directions,hdist,dmax,"Distance [Km]","distance.pdf")

    time.sleep(5)


