import configparser
from pymongo import MongoClient
from datetime import datetime, timedelta
#import os (for dockerfile)

#Ref: https://stackoverflow.com/questions/44336280/how-to-compare-time-dates-in-string-form

global mongo1
global db
global collection


def database():
    config = configparser.ConfigParser()
    config.read('config.ini')
  
    global mongo1
    mongo1 = client = MongoClient(config['MONGODB']['MONGO_CLIENT'])
    #mongo1 = client = MongoClient(os.environ['MONGO_CLIENT']) (for dockerfile)
    global db
    db = client['bus']
    global collection
    collection = db['database']
    
#list all ETA records    
def check(inputbus, inputtime):
    query = {"Bus": inputbus, "Timestamp":{ "$regex": inputtime }}
    results = collection.find(query)    
    results_number = collection.count_documents(query)
   
    if results_number == 0:
        print("No result found")
    else:
        print("Results:")
        for result in results:
                print("At: ", result["Timestamp"][11:19])
                for record in result["data"]:
                    print("Arrival time: ", record["eta"][11:19], record["rmk_en"])
                print("_____________________________")

#calculate bus schedule based on ETA records
def time_schedule(inputbus, inputtime):
    query = {"Bus": inputbus, "Timestamp":{ "$regex": inputtime }}
    results = collection.find(query)    
    results_number = collection.count_documents(query)
    
    bustime = 0
    prev_bustime = 0
    scheduledbus = ""
   
    if results_number == 0:
        print("No result found")
    else:
        print("Results:")
        for result in results:
                
                for record in result["data"]:
                    
                    if (record["eta_seq"] == 1):
                        bustime = datetime.strptime(record["eta"][11:19],'%H:%M:%S')
                        if (prev_bustime == 0):
                            prev_bustime = bustime
                            scheduledbus = record["rmk_en"]
                        else:
                            if (bustime < prev_bustime + timedelta(minutes = 5)):
                                prev_bustime = bustime
                                scheduledbus = record["rmk_en"]
                            else:
                                print(prev_bustime.strftime("%X"), scheduledbus)
                                print("_____________________________")
                                prev_bustime = bustime
                                scheduledbus = record["rmk_en"]
                            
def menu():
    inputbus = input("Check bus no: ").upper()
    inputtime = input("Check timestamp (format: yyyy-mm-ddThh:mm:ss): ")
    #2022-01-06T08:35:51
    mode = input("Check full ETA record: a, Check bus arrival time: b:")
    if mode == "a":
        check(inputbus, inputtime)
        menu()
    elif mode == "b":
        time_schedule(inputbus, inputtime)
        menu()
    else:
        check(inputbus, inputtime)
        time_schedule(inputbus, inputtime)
        menu()

                

database()

menu()

