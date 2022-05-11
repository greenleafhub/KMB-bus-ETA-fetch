import requests
import time
#import os (use os commands for building container via dockerfile)

#https://data.gov.hk/tc-data/dataset/hk-td-tis_21-etakmb

import configparser
from pymongo import MongoClient

global mongo1
global db
global collection


def database():
    config = configparser.ConfigParser()
    config.read('config.ini')
  
    global mongo1
    mongo1 = client = MongoClient("mongodb://localhost:27017/bus") #localhost
    #mongo1 = client = MongoClient(config['MONGODB']['MONGO_CLIENT']) #link in separated config.ini file 
    #mongo1 = client = MongoClient(os.environ['MONGO_CLIENT']) #for building container, link in separated dockerfile
    global db
    db = client['bus-kmb']
    global collection
    collection = db['database']




def callAPI(bus, station, station_name):
        
    for busno in bus:
        
        r = requests.get(
            f'https://data.etabus.gov.hk/v1/transport/kmb/eta/{station}/{busno}/1')

        api = r.json()

        print(busno, station_name, " Called at:", api['generated_timestamp'])
        print("----------------------------------------")
        
        arrivaltime = api['data']

        for item in arrivaltime:
            print(item['eta_seq'],item['eta'], item['rmk_en'], item['dest_tc'])
        
        print("----------------------------------------")
        post = {"Timestamp": api['generated_timestamp'], "Bus": busno, "Station": station_name, "Station_code": station, "data": arrivaltime}
        x = collection.insert_one(post)
    
    print("----------------------------------------")

       
database()

#Check station value from buscheck.py

while(True):
    
    bus = ["286X"]
    station = "BE58B5A4B0E76EF7"
    station_name =  '海福花園'
    callAPI(bus, station, station_name)    
  
    bus = ["286X"]
    station = "480DB16994F8FFEE"
    station_name =  '青沙公路轉車站 (A5)'
    callAPI(bus, station, station_name)

    bus = ["280X"]
    station = "480DB16994F8FFEE" 
    station_name = '青沙公路轉車站 (A3)'
    callAPI(bus, station, station_name)
    
    bus = ["280X"]
    station = "FE56DD70DEDE0395" 
    station_name = '聖安德烈堂 (S48)'
    callAPI(bus, station, station_name)
    
    bus = ["81"]
    station = "DF10BE627F25E7DD" 
    station_name = '油麻地寧波街 (N28)'
    callAPI(bus, station, station_name)

    

    time.sleep(60)