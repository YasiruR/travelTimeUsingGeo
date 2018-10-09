#i/usr/bin/python

import numpy as np

class Trip:
    
    def findNeighboursForATrip(self, pickupLat, pickupLon, dropoffLat, dropoffLon, timeRequested):
        
        neighbourList = []
        pickupGridArray = np.load('pickupArray.npy')
        dropoffGridArray = np.load('dropoffArray.npy')
        lats = np.load('latsGrid.npy')
        lons = np.load('lonsGrid.npy')
        
        platIndex = min(range(len(lats)), key=lambda i: abs(lats[i]-(pickupLat)))
        plonIndex = min(range(len(lons)), key=lambda i: abs(lons[i]-(pickupLon)))
        pSelectedTrips = pickupGridArray[platIndex][plonIndex]
        
        dlatIndex = min(range(len(lats)), key=lambda i: abs(lats[i]-(dropoffLat)))
        dlonIndex = min(range(len(lons)), key=lambda i: abs(lons[i]-(dropoffLon)))
        dSelectedTrips = dropoffGridArray[dlatIndex][dlonIndex]
        
#        print('Pickup neighbours : ', pSelectedTrips)
#        print('\n')
#        print('Dropoff neighbours : ', dSelectedTrips)
#        print('\n')
             
#        for i in range(20, 40):
#            print(pickupGridArray[20][i])
#            print(dropoffGridArray[20][i])
#            print('\n')
        
        for ele in pSelectedTrips:
            if(ele in dSelectedTrips):
                neighbourList.append(ele)
                
#        print("Neighbour List : ", neighbourList)
        return neighbourList;

        
#    findNeighboursForATrip(40.77042, -73.95736, 40.737445, -73.979765, 0)
#    findNeighboursForATrip(40.77042, -73.95736, 40.77042, -73.95736, 0)
        
     