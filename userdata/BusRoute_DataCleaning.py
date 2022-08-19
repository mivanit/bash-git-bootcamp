##Fractal Cities project
##New programming work

##"cleans" RTD bus route data as to only include route times between 6am and 10am

import pandas as pd
import json

def main():
    #import data for stop_times
    #use clean stop times

    #import clean stop times as RTD_stoptimes, this is a very big file
    RTD_stoptimes = pd.read_csv('/Users/ryanpeterson/Documents/BusRouteNetwork/Data/gtfs_2019/clean_stop_times.csv')  
    
    #import txt to dictionary using json
    with open('bg_stopid_2019.txt') as f:
        bg_stopid_data = f.read()
    bg_stopid = json.loads(bg_stopid_data)
    
    #check to see if the trip_id has any times between 06:00:00 and 10:00:00
    time_range = ("06:00:00", "10:00:00")
    trip_id = []
    for i in RTD_stoptimes.index:
        arrival = RTD_stoptimes['arrival_time'][i]
        departure = RTD_stoptimes['departure_time'][i]
        if time_is_between(arrival, departure, time_range):
            #print(arrival, departure) #test print
            trip = RTD_stoptimes['trip_id'][i]
            if trip not in trip_id:
                trip_id.append(trip)
                #print(trip) #test print
    #print(len(trip_id)) #test print 
    
    ##after trip_id list is populated, then select for only rows in the data frame that has those trip_ids
    RTD_stoptimes = RTD_stoptimes[RTD_stoptimes['trip_id'].isin(trip_id)]
    RTD_stoptimes = RTD_stoptimes.reset_index(drop=True)
    print(RTD_stoptimes)    
    
    ##add associated block group id for each stop_id in the data frame, create new columnof bg_id
    rows = []
    for i in RTD_stoptimes.index:
        test_id = RTD_stoptimes['stop_id'][i] #stop id
        trip_id = RTD_stoptimes['trip_id'][i]
        #print(test_id) #test print
        for k in bg_stopid:
            #print(k)
            if bg_stopid[k]: ##check to see if stop_id list is empty in bg_stopid dictionary
                #print(bg_stopid[k])
                if test_id in bg_stopid[k]: ##is test id in the list of stop_ids form the dictionary
                    rows.append([trip_id, test_id, k])

    stop_bg_id = pd.DataFrame(rows, columns=["trip_id", "stop_id", "bg_id"])      
    print(stop_bg_id)
    
    #export to cdv to check manually
    stop_bg_id.to_csv('/Users/ryanpeterson/Documents/BusRouteNetwork/Data/stop_bg_id_2019.csv')
    
    
    ##below currently not working for the merge, this may not matter
    RTD_network_data = pd.merge(RTD_stoptimes, stop_bg_id, how = "left", on = ["trip_id", "stop_id"])
    
    print(RTD_network_data)
    
    #working at the moment
    RTD_network_data.to_csv('/Users/ryanpeterson/Documents/BusRouteNetwork/Data/RTD_network_2019.csv') 

#--------------------------
def time_is_between(time1, time2, time_range):
    return time_range[0] <= time1 <= time_range[1] or time_range[0] <= time2 <= time_range[1]

    
if __name__ == '__main__':
    main()