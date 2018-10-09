#i/usr/bin/python

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy as cp

class Map:
    
    def createMapWithGrids():
        #m = Basemap(projection='lcc',
        #            lat_0 = 40.831,
        #            lon_0 = -73.9712,
        #            width = 100000,
        #            height = 75000)
        
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
          
        
        ##m.drawcoastlines()
        #m.drawcountries()
        #m.drawstates()
        #m.drawmeridians(lons)
        #m.drawparallels(lats)
        #
        #m.drawmapboundary(fill_color='aqua')
        #m.fillcontinents(color='coral',lake_color='aqua')
        #m.drawcoastlines()
        #
        ##m.bluemarble()
        #
        #plt.show()
        #plt.savefig('test.png')
        
        
#        lonIndex = min(range(len(lons)), key=lambda i: abs(lons[i]-(-74.005201)))
        
        np.save('latsGrid', lats)
        np.save('lonsGrid', lons)
        print("The map is created with grids..")
        return lats, lons;
        
        
    def createGridList():
        
        gridArray = []
        for i in range(0, 200):
            ele = []
            gridArray.append(ele)
            for j in range(0, 200):
                newEle = []
                gridArray[i].append(newEle)
        
        print('nooooo')
        print("Grid List is initialized..")
        return gridArray;
                
        
    def insertTrips(gridArray, lats, lons):
        
        dataFile = pd.read_csv('preprocessed_trips_discretised.csv')
               
        pickupGridArray = cp.deepcopy(gridArray)
        dropoffGridArray = cp.deepcopy(gridArray)
        
        pickupLatList = dataFile.pickup_lat
        pickupLonList = dataFile.pickup_long
        dropoffLatList = dataFile.dropoff_lat
        dropoffLonList = dataFile.dropoff_long
#        tripTimeList = dataFile.trip_duration
        
        
        index = 0
        for ele in pickupLatList:
            print('p : ', index)
            platIndex = min(range(len(lats)), key=lambda i: abs(lats[i]-(ele)))
            plonIndex = min(range(len(lons)), key=lambda i: abs(lons[i]-(pickupLonList[index])))
#            print(platIndex, plonIndex)
            pickupGridArray[platIndex][plonIndex].append(index)            
            index += 1
            if(index == 1500000):
                break
        print('\n')
        
        index = 0
        for ele in dropoffLatList:
            print('d : ', index)
            dlatIndex = min(range(len(lats)), key=lambda i: abs(lats[i]-(ele)))
            dlonIndex = min(range(len(lons)), key=lambda i: abs(lons[i]-(dropoffLonList[index])))
#            print(dlatIndex, dlonIndex)
            dropoffGridArray[dlatIndex][dlonIndex].append(index)
            
#            if(dropoffGridArray[dlatIndex][dlonIndex] is None):
#                dropoffGridArray[dlatIndex][dlonIndex] = index
#            else:
#                dropoffGridArray[dlatIndex][dlonIndex].append(index)
                
            index += 1
            if(index == 1500000):
                break
        
#        print('\n')
#        if(pickupGridArray is not dropoffGridArray):
#            print('different objects')
#        
#        #check for equality between 2 lists
#        flag = 0
#        flag1 = 0
#        for i in range(0, 200):
#            for j in range(0, 200):
#                #print(i, j)
#                if(len(pickupGridArray[i][j]) > 0):
#                    flag1 = 1
#                    print(i, j)
#                    print(pickupGridArray[i][j])
#                    print(dropoffGridArray[i][j])
#                    if(pickupGridArray[i][j] != dropoffGridArray[i][j]):
#                        print(pickupGridArray[i][j], dropoffGridArray[i][j])
#                        flag = 1
#                        print('\n')
#        
#        if(flag1 == 0):
#            print('All are empty')
#        
#        if(flag == 0):
#            print("All equal")    
        
        #np.save('pickupArray2', pickupGridArray)
        #np.save('dropoffArray2', dropoffGridArray)
        
        print("Files are saved successfully..")
        


    lats, lons = createMapWithGrids()
    gridArray = createGridList()    
    insertTrips(gridArray, lats, lons)
        
        
        
        
        