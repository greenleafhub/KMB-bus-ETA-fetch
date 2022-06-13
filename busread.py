import configparser
from pymongo import MongoClient
from datetime import datetime, timedelta
import csv
# import os (for dockerfile)

# Ref: https://stackoverflow.com/questions/44336280/how-to-compare-time-dates-in-string-form

global mongo1
global db
global collection


def database():
    config = configparser.ConfigParser()
    config.read('config.ini')

    global mongo1
    mongo1 = client = MongoClient("mongodb://localhost:27017/")  # localhost
    # mongo1 = client = MongoClient(config['MONGODB']['MONGO_CLIENT']) #link in separated config.ini file
    # mongo1 = client = MongoClient(os.environ['MONGO_CLIENT']) (for dockerfile)
    global db
    db = client['bus-kmb']
    global collection
    collection = db['database']

# list all ETA records


def check(inputroute, inputstation, inputtime):
    query = {"Bus": {"$regex": inputroute}, "Station": {
        "$regex": inputstation}, "Timestamp": {"$regex": inputtime}}
    results = collection.find(query)
    results_number = collection.count_documents(query)

    if results_number == 0:
        print("No result found")
    else:
        print("Results for ", inputroute, " at ",
              inputstation, " on ", inputtime)
        for result in results:
            print("At: ", result["Timestamp"][11:19])
            for record in result["data"]:
                if record["eta"] is not None:
                    print("Arrival time: ",
                          record["eta"][11:19], record["rmk_en"])
            print("_____________________________")

# calculate bus schedule based on ETA records


def time_schedule(inputroute, inputstation, inputtime):
    query = {"Bus": {"$regex": inputroute}, "Station": {
        "$regex": inputstation}, "Timestamp": {"$regex": inputtime}}
    results = collection.find(query)
    results_number = collection.count_documents(query)

    bustime = 0
    prev_bustime = 0
    scheduledbus = ""

    if results_number == 0:
        print("No result found")
    else:
        print("Results for ", inputroute, " at ",
              inputstation, " on ", inputtime)
        for result in results:

            for record in result["data"]:

                if (record["eta_seq"] == 1) and (record["eta"] is not None):
                    # read bustime in the recoreded minute
                    bustime = datetime.strptime(
                        record["eta"][11:19], '%H:%M:%S')

                    # set up first prev_bustime if first record
                    if (prev_bustime == 0):
                        prev_bustime = bustime
                        prev_timestamp = result["Timestamp"][11:19]
                        scheduledbus = record["rmk_en"]
                    else:

                        if (bustime < prev_bustime + timedelta(minutes=5)):
                            prev_bustime = bustime
                            prev_timestamp = result["Timestamp"][11:19]
                            scheduledbus = record["rmk_en"]
                        else:
                            # if current next bus > previous next bus + 5 min recorded

                            # assume bus just left in the previous minute
                            print(prev_timestamp, scheduledbus)

                            # choose this if assume bus ETA delayed and bust actually left earlier
                            # print(prev_bustime.strftime("%X"), scheduledbus)

                            prev_bustime = bustime
                            prev_timestamp = result["Timestamp"][11:19]
                            scheduledbus = record["rmk_en"]

# write to csv file


def csv_time_schedule(inputroute, inputstation):

    datetext = ['01', '02', '06', '07', '08', '09', '10']
    dct = {}

    for i in datetext:

        inputtime = '2022-06-{}'.format(i)
        i = (int(i))

        query = {"Bus": {"$regex": inputroute}, "Station": {
            "$regex": inputstation}, "Timestamp": {"$regex": inputtime}}
        results = collection.find(query)
        results_number = collection.count_documents(query)

        bustime = 0
        prev_bustime = 0
        scheduledbus = ""

        # save data to a list to print to csv later
        dct[i] = []
        if results_number == 0:
            dct[i].append("No result found")
        else:
            for result in results:

                for record in result["data"]:

                    if (record["eta_seq"] == 1) and (record["eta"] is not None):
                        # read bustime in the recoreded minute
                        bustime = datetime.strptime(
                            record["eta"][11:19], '%H:%M:%S')

                        # set up first prev_bustime if first record
                        if (prev_bustime == 0):
                            prev_bustime = bustime
                            prev_timestamp = result["Timestamp"][11:19]
                            scheduledbus = record["rmk_en"]
                        else:

                            if (bustime < prev_bustime + timedelta(minutes=5)):
                                prev_bustime = bustime
                                prev_timestamp = result["Timestamp"][11:19]
                                scheduledbus = record["rmk_en"]
                            else:
                                # if current next bus > previous next bus + 5 min recorded

                                # assume bus just left in the previous minute
                                str_prev_timestamp = str(prev_timestamp)
                                dct[i].append([str_prev_timestamp +
                                               ', ' + scheduledbus])

                                # choose this if assume bus ETA delayed and bust actually left earlier
                                # print(prev_bustime.strftime("%X"), scheduledbus)

                                prev_bustime = bustime
                                prev_timestamp = result["Timestamp"][11:19]
                                scheduledbus = record["rmk_en"]

    #print(inputroute, inputstation)
    # print(dct[1])

    # write to csv file

    with open('F:/python/bus/alldata_{}.csv'.format([inputroute + inputstation]), 'w') as f:
        w = csv.writer(f)
        for i in dct:
            w.writerow(dct[i])


def printall():
    inputroute = ["286X", "286X", "280X", "280X", "81"]
    inputstation = [
        '海福花園', '青沙公路轉車站', '青沙公路轉車站', '聖安德烈堂', '油麻地寧波街']
    for i, j in zip(inputroute, inputstation):
        csv_time_schedule(i, j)
    print('done!')


def menu():
    inputroute = input("Check route: ")
    inputroute = str(inputroute.upper())
    inputstation = input("Check station: ")
    inputtime = input("Check timestamp (format: yyyy-mm-ddThh:mm:ss): ")
    # 2022-01-06T08:35:51
    mode = input(
        "Check full ETA record: a, Check bus arrival time: b:, Check all bus arrival time: c:     ")
    if mode == "a":
        check(inputroute, inputstation, inputtime)
        menu()
    elif mode == "b":
        time_schedule(inputroute, inputstation, inputtime)
        menu()
    elif mode == 'c':
        printall()
    else:
        menu()


database()

menu()
