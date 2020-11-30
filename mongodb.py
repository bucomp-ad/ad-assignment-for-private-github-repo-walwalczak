from pymongo import MongoClient

client = MongoClient("mongodb+srv://dbAdmin:Password01@cluster0.chzl0.mongodb.net/AdvancedDev?retryWrites=true&w=majority")
db = client["AdvancedDev"]