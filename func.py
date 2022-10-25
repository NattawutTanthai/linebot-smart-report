# MongoDB driver

from pymongo import MongoClient
from pydantic import BaseModel

client = MongoClient('localhost', 27017)
db = client.smartReportDB
collection = db['customer']

class function(BaseModel) :
    latitude:str
    longitude:str
    address:str
    
    async def addLocation(latitude,longitude,address):
        await collection.insert_one({
            "lat": latitude,
            "long": longitude,
            "address": address
        })
