#i/usr/bin/python

import pandas as pd
import datetime as dt
import numpy as np

class SpeedTable:
    
    def createSpeedTable():
        
        #creating table with [[sum, count], ....] format from 0 to 167
        speedTable = []
        for i in range(0, 168):
            ele = []
            speedTable.append(ele)
            
        return speedTable;
    
    def insertTripsIntoRefTable(speedTable):
        
        finalSpeedTable = []
        dataFile = pd.read_csv('preprocessed_trips_discretised.csv')
        
#        pickupLatList = dataFile.pickup_lat
        pickupTimeList = dataFile.pickup_time
#        dropoffTime = dataFile.dropoff_time
        tripDistanceList = dataFile.trip_distance
        tripDurationList = dataFile.trip_duration
        
        index = 0
        for ele in pickupTimeList:
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

            if(len(speedTable[speedRefIndex]) == 0):
                speedTable[speedRefIndex].append(averageSpeed)
                speedTable[speedRefIndex].append(1)
            else:
                speedTable[speedRefIndex][0] += averageSpeed
                speedTable[speedRefIndex][1] += 1
            
            if(index == 2000000):
                print(speedTable)
                break
            index += 1
            
        for ele in speedTable:
            if(ele == []):
                totalAverageSpeed = 0
            else:
                totalAverageSpeed = ele[0] / ele[1]
            finalSpeedTable.append(totalAverageSpeed)
        
        #np.save('speedReferenceTable2', finalSpeedTable)
        print(finalSpeedTable)
        
            
    speedTable = createSpeedTable()
    insertTripsIntoRefTable(speedTable)       