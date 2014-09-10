import pymongo

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e 
db = conn.mydb
db = conn['station']
trains = db.train
platforms = db.platform
outer_lines = db.outer_lines

print db.collection_names()

def addTrain(name,code,arrival_time,direction,status):
    train = {"name":name,"code":code,"arrival_time":arrival_time,"direction":direction,"status":status}
    trains.insert(train)

def getTrainList():
    return trains

def deleteTrain(code):
    trains.remove({"code":code})

def getTrain(code):
    return trains.find({"code":code})

def updateTrainArrivalTime(code,time):
    trains.update({"code":code},{'$set':{"arrival_time":time}})

def addPlatform(number,status,occupany,code):
    platform = {"number":number,"status":status,"occupany":occupany,"code":code}
    platforms.insert(platform)

def getPlatformList():
    return platforms

def updatePlatformStatus(number,status):
    platforms.update({"number":number},{'$set':{"status":status}})

def updatePlatformOccupancy(number,occupany):
    platforms.update({"number":number},{'$set':{"occupany":occupany}})

def addOuterLines(number,occupany,code):
    outer_line = {"number":number,"occupany":occupany,"code":code}
    outer_lines.insert(outer_line)

def updateOuterLines(number,occupany):
    outer_lines.update({"number":number},{'$set':{"occupany":occupany}})