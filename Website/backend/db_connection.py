from pymongo import MongoClient
from mongoengine import connect  

mongo_uri = "mongodb+srv://busfinderadmin:busfinderadmin@cluster0.ovm5f5a.mongodb.net/"
client = MongoClient(mongo_uri)

db = client["BusFleetManagement"]

connect(db="BusFleetManagement", host=mongo_uri)
