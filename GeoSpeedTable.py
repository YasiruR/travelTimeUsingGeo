#i/usr/bin/python

import pandas as pd
import datetime as dt
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

class GeoSpeedTable:
    
    def createMapWithGrids():
        
        fig, ax = plt.subplots()
        
        m = Basemap(
            projection='mill',
            llcrnrlat= 40.6968,
            llcrnrlon= -74.0224,
            urcrnrlat= 40.8964, 
            urcrnrlon= -73.8927,
            resolution='h',
            ax = ax,
            )
        
        llcrnrlon = -74.0224
        llcrnrlat = 40.6968
        x0, y0 = m(llcrnrlon, llcrnrlat)
        
        x = np.arange(200)*200+x0
        y = np.arange(200)*200+y0
        
        lons, lats = m(x,y,inverse=True)
        
        print('Map created with grids....')
        return lats, lons;
    
    def createGeoSpeedTable():
        
        #creating table with [[sum, count], ....] format from 0 to 167
        speedTable = []
        for i in range(0, 168):
            ele = []
            speedTable.append(ele)
        
        #assigning each grid with a speed table
        gridArray = []
        for i in range(0, 200):
            ele = []
            gridArray.append(ele)
            for j in range(0, 200):
                gridArray[i].append(speedTable)
                
        print("Empty geo-speed list is initialized....") 
            
        return gridArray;
    
    def insertTripsIntoRefTable(geoSpeedTable, lats, lons):
        
        dataFile = pd.read_csv('preprocessed_trips_discretised.csv')
        
        pickupTimeList = dataFile.pickup_time
        tripDistanceList = dataFile.trip_distance
        tripDurationList = dataFile.trip_duration
        pickupLatList = dataFile.pickup_lat
        pickupLonList = dataFile.pickup_long
        dropoffLatList = dataFile.dropoff_lat
        dropoffLonList = dataFile.dropoff_long
        
        index = 0
        for ele in pickupTimeList:
            
            print('Checking index ', index)
            #getting the day of the week (Monday = 0)
            year = int(ele[0:4])
            month = int(ele[5:7])
            date = int(ele[8:10])
            tripDate = dt.date(year, month, date)
            tripDay = tripDate.weekday()
            
            #getting time requested           
            hour = int(ele[-8:-6])

            speedRefIndex = (tripDay * 24) + hour
            #calculating in km per hour
            averageSpeed = (tripDistanceList[index] * 3600) / tripDurationList[index]
            
            #adding speed to the pickup grid
            pLatIndex = min(range(len(lats)), key=lambda i: abs(lats[i]-(pickupLatList[index])))
            pLonIndex = min(range(len(lons)), key=lambda i: abs(lons[i]-(pickupLonList[index])))
            if(len(geoSpeedTable[pLatIndex][pLonIndex][speedRefIndex]) == 0):
                geoSpeedTable[pLatIndex][pLonIndex][speedRefIndex].append(averageSpeed)  
                geoSpeedTable[pLatIndex][pLonIndex][speedRefIndex].append(1)
            else:
                geoSpeedTable[pLatIndex][pLonIndex][speedRefIndex][0] += averageSpeed
                geoSpeedTable[pLatIndex][pLonIndex][speedRefIndex][1] += 1
                
            #adding speed to the dropoff grid
            #NOTE: since average is taken again adding twice does not matter
            dLatIndex = min(range(len(lats)), key=lambda i: abs(lats[i]-(dropoffLatList[index])))
            dLonIndex = min(range(len(lons)), key=lambda i: abs(lons[i]-(dropoffLonList[index])))
            if(len(geoSpeedTable[dLatIndex][dLonIndex][speedRefIndex]) == 0):
                geoSpeedTable[dLatIndex][dLonIndex][speedRefIndex].append(averageSpeed)  
                geoSpeedTable[dLatIndex][dLonIndex][speedRefIndex].append(1)
            else:
                geoSpeedTable[dLatIndex][dLonIndex][speedRefIndex][0] += averageSpeed
                geoSpeedTable[dLatIndex][dLonIndex][speedRefIndex][1] += 1                
            
            if(index == 2000000):
                break
            index += 1
            
        print('\nCompleted adding all the trips upto ', index, ' !!!')
        print('\nStarting the finalization of Speed Table.... \n')
        
        #Re-initializing gridArray for finalized speedTable
        finalGeoSpeedTable = []
        for i in range(0, 200):
            ele = []
            finalGeoSpeedTable.append(ele)

        
        counter = 0
        for ele in geoSpeedTable:
            print('Finalizing lat ', counter)
            x = 0
            for subSpeedTable in ele:
                print('lon ', x)
                finalSubSpeedTable = []
                for timeSlot in subSpeedTable:
                    if(timeSlot == []):
                        totalAverageSpeed = 0
                    else:
                        totalAverageSpeed = timeSlot[0] / timeSlot[1]
                    finalSubSpeedTable.append(totalAverageSpeed)                 
                finalGeoSpeedTable[x].append(finalSubSpeedTable)
                x += 1           
        
        np.save('geoSpeedReferenceTable', finalGeoSpeedTable)
        print(finalGeoSpeedTable)
        print('\nGEO-SPEED TABLE IS CREATED !!!!!!!!!!!!!!!!!!!')
        
    lats, lons = createMapWithGrids()
    geoSpeedTable = createGeoSpeedTable()
    insertTripsIntoRefTable(geoSpeedTable, lats, lons)
