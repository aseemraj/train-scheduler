from db import *

deleteTrain("12501")
deleteTrain("12483")
deleteTrain("12481")
deleteTrain("13763")

addTrain("Mandore Exp.","12483","19:30","West","NOT_ARRIVED")
addTrain("Suryanagari Exp.","12481","17:30","East","NOT_ARRIVED")
addTrain("Howrah Exp.","12501","05:20","West","WAITING")
addTrain("Rajdhani Exp.","13763","12:00","East","DEPARTED")


for train in trains.find():
	print train