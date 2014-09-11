from db import *

def getKey(train):
	return train["arrival_time"]

sortedTrain = sorted(trains.find(), key=getKey)

for platform in platforms:
	if platform["status"]=="ENABLED" and platform["occupancy"]=="Empty":
		