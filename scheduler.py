from db import *

'''
def getKey(train):
	return train["arrival_time"]

sortedTrain = sorted(trains.find(), key=getKey)

for platform in platforms:
	if platform["status"]=="ENABLED" and platform["occupancy"]=="Empty":
'''

class Scheduler():

	def __init__(self):

		self.trainSchedule = []
		for train in getTrainList().find():
			self.trainSchedule.append({"Code": train["code"],"Direction": train["direction"], "Type": train["type"], "Status": train["status"], "Scheduled_Arrival_Time": train["arrival_time"], "Platform_Arrival_Time": train["arrival_time"], "IsWaiting": False, "WaitLocation": 0, "WaitTime": 0, "PlatformNumber": 0, "PlatformTime": 0})

		self.platformSchedule = []
		for platform in getPlatformList().find():
			self.platformSchedule.append({"Number": platform["number"], "Status": platform["status"], "Occupancy": platform["occupancy"], "Code": platform["code"]})

		self.sideLineSchedule = []
		for i in range (1,11):
			if i<6:
				self.sideLineSchedule.append({"Number": i, "Occupancy": "EMPTY", "Code": "0", "Location": "LEFT"})
			else:
				self.sideLineSchedule.append({"Number": i, "Occupancy": "EMPTY", "Code": "0", "Location": "RIGHT"})


		for train in self.trainSchedule:
			if train["Type"]=="Passing":
				train["PlatformTime"] = 5
			else:
				train["PlatformTime"] = 15

		for train in self.trainSchedule:
			print self.timeToInt(train["Scheduled_Arrival_Time"])



	def makeSchedule(self):

		for self.timer in range(0,60*24 + 1):

			self.schedulingPlatformTrains()
			self.schedulingWaitingTrains()
			self.schedulingIncomingTrains()



	def schedulingPlatformTrains(self):
		for train in self.trainSchedule:

			if train["Status"]=="ON_PLATFORM":
				currentTrain = self.getTrain(train["Code"])

				if train["PlatformTime"]==0:
					currentPlatform = self.getPlatform(train["PlatformNumber"])

					currentTrain["Status"] = "DEPARTED"
					currentTrain["PlatformNumber"] = 0

					currentPlatform["Code"] = 0
					currentPlatform["Occupancy"] = "EMPTY"
				else:
					currentTrain["PlatformTime"] = currentTrain["PlatformTime"] - 1


	def schedulingWaitingTrains(self):
		for train in self.trainSchedule:

			if train["Status"]=="WAITING":
				currentTrain = self.getTrain(train["Code"])



	def schedulingIncomingTrains(self):
		i=1





	def getTrain(self,code):
		for train in self.trainSchedule:
			if train["Code"]==code:
				return train

	def getPlatform(self,number):
		for platform in self.platformSchedule:
			if platform["Number"]==number:
				return platform

	def getSideLine(self,number):
		for sideLine in self.sideLineSchedule:
			if sideLine["Number"]==number:
				return sideLine

	def timeToInt(self,timeString):
		timeList = timeString.split(':')
		return(60*int(timeList[0]) + int(timeList[1]))

	def intToTime(self,timeInt):
		return(str(int(timeInt/60)) + ":" + str(timeInt%60))

Scheduler().makeSchedule()

		