from pymongo import MongoClient

x = MongoClient()['stox']

for i in x.AA_history.find():
	print i
