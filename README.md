# KMB bus ETA fetch
 Fetch arrival time estimation data (ETA) and store in mongoDB, and use the ETA history to generate the bus schedule.
  
busfetch.py: 
Fetch bus ETA of a bus route at a certain station every minute, and store data on MongoDB. Data collected every minute are marked by Timestamp, bus route, bus station (16 character code).
 
busread.py: 
Read the ETA data stored in MongoDB and generate bus schedule of the certain station based on ETA data. Search within the database with bus station and timestamp.
(to-do: search with both bus station and bus route to avoid confusion) 
Scheduled bus record are marked as it often indicates the bus never arrived if it is marked at "scheduled" even when it's supposed to arrived at station.

bus_route_check.py:
Search corresponding bus stop code easily by listing all bus stops in a route.
 
To run the python files, a separate config.ini file needs to be prepared for storing the link to MongoDB database.
