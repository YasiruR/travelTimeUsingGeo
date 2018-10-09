#i/usr/bin/python

import Trip as trip
import numpy as np
import pandas as pd
import datetime as dt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import scipy.stats
#import TravelTime as travelTime

class TravelTime:
    
    def __init__(self):
        self.neighbourClass = trip.Trip()        
    
    def findTravelTime(self, pickupLat, pickupLon, dropoffLat, dropoffLon, dayRequested, timeRequested): #day0 = Monday
        
        #neighbourList = trip.Trip.findNeighboursForATrip(pickupLat, pickupLon, dropoffLat, dropoffLon, timeRequested)
        
        #neighbourClass = trip.Trip()
        neighbourList = self.neighbourClass.findNeighboursForATrip(pickupLat, pickupLon, dropoffLat, dropoffLon, timeRequested)
        
        speedTable = np.load('speedReferenceTable.npy')
        
        dataFile = pd.read_csv('preprocessed_trips_discretised.csv')
        pickupTimeList = dataFile.pickup_time
        tripDurationList = dataFile.trip_duration
        
        currentSpeedRefIndex = dayRequested * 24 + timeRequested
        currentSpeedRef = speedTable[currentSpeedRefIndex]
        
        counter = 0
        totalTravelTime = 0
        for ele in neighbourList:
            
            try:
                travelTime = tripDurationList[ele]
            except KeyError:
                continue            
            
#            travelTime = tripDurationList[ele]
            neighbourTrip = pickupTimeList[ele]
            year = int(neighbourTrip[0:4])
            month = int(neighbourTrip[5:7])
            date = int(neighbourTrip[8:10])
            tripDate = dt.date(year, month, date)
            tripDay = tripDate.weekday()
            hour = int(neighbourTrip[-8:-6])            
            neighbourTripSpeedRefIndex = tripDay * 24 + hour
            
            neighbourSpeedRef = speedTable[neighbourTripSpeedRefIndex]
            
            counter += 1
            totalTravelTime += travelTime * (currentSpeedRef / neighbourSpeedRef)
            
#        print('Neighbour List : ', neighbourList)
        if(counter == 0):
            print('No neighbours found !!!')
            return None;
        else:
            estimatedTravelTime = totalTravelTime / counter
            print("Calculated Travel Time : ", estimatedTravelTime)
            return estimatedTravelTime;       
            
        
    def testOnData(self):     
        
        actualTimeList = []
        calculatedTimeList = []
        errorList = []
        
#        #configured for preprocessed_trips_discretised.csv file
        #change the range (1 500 000, 1 500 050)
#        
#        dataFile = pd.read_csv('preprocessed_trips_discretised.csv')
#        pickupLatList = dataFile.pickup_lat
#        pickupLonList = dataFile.pickup_long
#        dropoffLatList = dataFile.dropoff_lat
#        dropoffLonList = dataFile.dropoff_long
#        pickupTimeList = dataFile.pickup_time
#        tripDurationList = dataFile.trip_duration

        #configured for result_all_disc_xgboost_with_actual_geo.csv file 
        
        dataFile = pd.read_csv('result_all_disc_xgboost_with_actual_geo.csv')
        pickupLatList = dataFile.actual_pickup_lat
        pickupLonList = dataFile.actual_pickup_long
        dropoffLatList = dataFile.actual_dropoff_lat
        dropoffLonList = dataFile.actual_dropoff_long
        pickupTimeList = dataFile.pickup_time
        tripDurationList = dataFile.actual_travel_time
        
#        lastIndex = len(pickupLatList) - 1
#        print("Last Index : ", lastIndex)
#        Last Index :  1772026
        
        for index in range(0, 5):
                            
            print('\n Checking ', index, '..................')
            pickupLat = pickupLatList[index]
            pickupLon = pickupLonList[index]
            dropoffLat = dropoffLatList[index]
            dropoffLon = dropoffLonList[index]
            tripDuration = tripDurationList[index]
    
            testTrip = pickupTimeList[index]
            year = int(testTrip[0:4])
            month = int(testTrip[5:7])
            date = int(testTrip[8:10])
            tripDate = dt.date(year, month, date)
            tripDay = tripDate.weekday()
            hour = int(testTrip[-8:-6])
#            print('details : ', pickupLat, pickupLon, dropoffLat, dropoffLon, tripDay, hour)
            
            estimatedTravelTime = self.findTravelTime(pickupLat, pickupLon, dropoffLat, dropoffLon, tripDay, hour)
                                               
    #            estimatedTravelTime = TravelTime.findTravelTime(pickupLat, pickupLon, dropoffLat, dropoffLon, tripDay, hour)
            print("Actual Travel Time : ", tripDuration)
            
            if(estimatedTravelTime != None):
                errorPercentage = (abs(tripDuration - estimatedTravelTime) * 100) / tripDuration
#                print("Error Percentage : ", errorPercentage)
#                print("\n")
                
                actualTimeList.append(tripDuration)
                calculatedTimeList.append(estimatedTravelTime)
                errorList.append(errorPercentage)
        
#        print('Actual Time List : ', actualTimeList)
#        print('Calculated Time List : ', calculatedTimeList)
#        print('Error List : ', errorList)
        
        np.save('actualTimeList', actualTimeList)
        np.save('calculatedTimeList', calculatedTimeList)
        np.save('errorList', errorList)
        
        mae = mean_absolute_error(actualTimeList, calculatedTimeList)
        rmse = (mean_squared_error(actualTimeList, calculatedTimeList))**(1/2)
        spearman = scipy.stats.spearmanr(actualTimeList, calculatedTimeList)
        
        #mean absolute percentage error
        y_true, y_pred = np.array(actualTimeList), np.array(calculatedTimeList)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
               
        print('\n \nMAE : ', mae)
        print('RMSE : ', rmse)
        print('Spearman Coefficient : ', spearman)
        print('MAPE : ', mape)
        
#        with open("Output.txt", "w") as text_file:
#            text_file.write("MAE : " % mae)
#            text_file.write("RMSE : " % rmse)
#            #text_file.write("Spearman Coefficient : " % spearman)
#            text_file.write("MAPE : " % mape)
        
        print('\n \n Done !!!!!!!!!!!!!!!!!!!!')
            
    #findTravelTime(40.77042, -73.95736, 40.737445, -73.979765, 0, 3) #100th entry
    #findTravelTime(40.7694, -73.965, 40.7537, -73.977, 1, 22)
    
#    testOnData()
    
    
travelTime = TravelTime()
travelTime.testOnData()    
    