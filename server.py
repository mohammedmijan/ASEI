from flask import Flask
from flask_pymongo import PyMongo
from stocks_data_collector import *
from bson.json_util import loads, dumps
import time
import Constants
# date 09-11-2021

app = Flask(__name__)
app.config["MONGO_URI"]=f"mongodb+srv://{Constants.user['user']}:{Constants.user['password']}@cluster0.fo82u.mongodb.net/StockData"
mongo = PyMongo(app)



def Company_data_saving(companies:list):
    if int(time.strftime("%H")) > 16:
        for company in companies:
            print("Started")
            print(company)
            list1 = []
            for da in data_from_dse_website(company):
                for column_name in Constants.column_names:
                    try:
                        try:
                            if column_name == "Day'sRange":
                                d = da["Day'sRange"].replace(",", "")
                                m = d.split("-")
                                s = float(m[1])-float(m[0])
                                list1.append(s)
                            else:
                                m = da[column_name].replace(",", "")
                                list1.append(float(m))
                        except:
                            list1.append(da[column_name])
                    except:
                        pass
            mongo.db.Stockdata.insert_one({"time":time.strftime("%x"),"company_name":company,
            "data":list1})
            print(list1)
            print("completed")
    else:
        print(f"Soory. It is {time.strftime('%X')} o'clock. Please, try 4 to 12 pm")

def Data_revive(company_name:list):
    for company_nam in company_name:
        datas = loads(dumps(mongo.db.Stockdata.find({"company_name":company_nam})))
        list1 = []
        for data in datas:
            list1.append(data["data"])
        print(list1)
    return list1

def Data_revive_to_all_companies():
    datas = loads(dumps(mongo.db.Stockdata.find()))
    list1 = []
    for data in datas:
        list1.append(data["data"])
    return list1

