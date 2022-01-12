import requests
import time
#import os (use os commands for building container via dockerfile)

import configparser
from pymongo import MongoClient

global mongo1
global db
global collection


def database():
    config = configparser.ConfigParser()
    config.read('config.ini')
  
    global mongo1
    mongo1 = client = MongoClient(config['MONGODB']['MONGO_CLIENT']) #link in separated config.ini file 
    #mongo1 = client = MongoClient(os.environ['MONGO_CLIENT']) #for building container, link in separated dockerfile
    global db
    db = client['bus']
    global collection
    collection = db['database']

bus = ["280X"]
station = "F3433105FE5F6865"
#https://data.etabus.gov.hk/v1/transport/kmb/stop "青沙公路轉車站 (A3)"'
#crosscheck with https://data.etabus.gov.hk/v1/transport/kmb/route-stop 

def callAPI(bus, station):
        
    for busno in bus:
        
        r = requests.get(
            f'https://data.etabus.gov.hk/v1/transport/kmb/eta/{station}/{busno}/1')

        api = r.json()

        print("Called at:", api['generated_timestamp'])
        print("______________________________________")
        
        arrivaltime = api['data']

        for item in arrivaltime:
            print(item['eta_seq'],item['eta'], item['rmk_en'])
        
        post = {"Timestamp": api['generated_timestamp'], "Bus": busno, "Station": station, "data": arrivaltime}
        x = collection.insert_one(post)

       
database()

while(True):
    callAPI(bus,station)
    time.sleep(60)