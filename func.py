# MongoDB driver

from pymongo import MongoClient
from pydantic import BaseModel

client = MongoClient('localhost', 27017)
db = client.smartReportDB
collection = db['report']

class Function(BaseModel) :
    latitude:str
    longitude:str
    address:str

    def addLocation(latitude,longitude,address):
        collection.insert_one({
            "lat": latitude,
            "long": longitude,
            "address": address
        })
