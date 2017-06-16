from pymongo import MongoClient

client = MongoClient("mongodb://l.murashov:04101576@ds155841.mlab.com:55841/hotdogs1576")
database = client["hotdogs1576"]
collection = database["hotdogs"]
collection.delete_many({})

data = []
for i,img in enumerate(open("images.txt", encoding="utf-8")):
    data.append({"name": "hotdog" + str(i), "link" : img})

collection.insert_many(data)