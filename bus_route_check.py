import requests
import json

#https://data.gov.hk/tc-data/dataset/hk-td-tis_21-etakmb

#get stations with names json list
s = requests.get(
     'https://data.etabus.gov.hk/v1/transport/kmb/stop')
    
kmbstop = s.json()
stations = kmbstop['data']

#print dict
def get_all_values(nested_dictionary):
    for key, value in nested_dictionary.items():
        if type(value) is dict:
            get_all_values(value)
        else:
            print(key, ":", value)

#check station with code for a bus route
def stationcode(inputbus):
    
    r = requests.get(
        'https://data.etabus.gov.hk/v1/transport/kmb/route-stop')
    
    routestop = r.json()
    routes = routestop['data']    
    found = 0
    busdict = {}
    seq = 1

    print("-----------------------------------------")
    #print("{:<6}{:<6}{:<20}{:<0}".format("Bound", "Seq" , "Station_code" , "Station_name"))      
        
    for item in routes:        
        if item['route'] == inputbus:
            
            found = 1      
            
            #put bus stop info indct
            dictitem = busdict.get(item['bound'], dict())
            dictitem[item['seq']] = item['stop']
            busdict[item['bound']] = dictitem
        
            #match station code with station name
            for station in stations:
                if station['stop'] == item['stop']:
                    station_name = station['name_tc']   
                     
            #print bus stop info
            print("{:<6}{:<6}{:<20}{:<0}".format(item['bound'], item['seq'], item['stop'], station_name))

    #print bus stop dict
    #if found == 1:
    #    get_all_values(busdict)
                


    if found == 0:
        print("No result for this bus no. ")
     
    print("-----------------------------------------")   
        
    

       
#station value from: https://data.etabus.gov.hk/v1/transport/kmb/stop 
#crosscheck with https://data.etabus.gov.hk/v1/transport/kmb/route-stop 

def menu():
    inputbus = input("Check bus no: ")
    inputbus = str(inputbus.upper())
    stationcode(inputbus)
    
    
    
menu()

