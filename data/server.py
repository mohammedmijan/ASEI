from flask import Flask
from flask_pymongo import PyMongo
from .stocks_data_collector import *
from bson.json_util import loads, dumps
import time
from .Constants import *
import certifi
# date 09-11-2021

app = Flask(__name__)
app.config["MONGO_URI"]=f"mongodb+srv://{user['user']}:{user['password']}@cluster0.fo82u.mongodb.net/stockdata2"
mongo = PyMongo(app , tlsCAFile=certifi.where())



def Company_data_saving(companies:list):
    #save data to server
    if int(time.strftime("%H")) > 16:
        for company in companies:
            print("Started")
            print(company)
            list1 = []
            for da in data_from_dse_website(company):
                for column_name in column_names:
                    try:
                        try:
                            if column_name == "Day'sRange":
                                d = da["Day'sRange"].replace(",", "")
                                m = d.split("-")
                                skt = float(m[1])-float(m[0])
                                list1.append(skt)
                                list1.append(float(m[1]))
                                list1.append(float(m[0]))
                            else:
                                m = da[column_name].replace(",", "")
                                list1.append(float(m))
                        except:
                            if column_name != "Day'sRange":
                                list1.append(da[column_name])
                            pass
                    except:
                        pass
            mongo.db.Stockdata.insert_one({"time":time.strftime("%x"),"company_name":company,
            "data":list1})
            print("completed")
    else:
        print(f"Soory. It is {time.strftime('%X')} o'clock. Please, try 4 to 12 pm")

def Data_revive(company_name:str=None):
    #individual company data retrive from server
    if company_name:
        datas = loads(dumps(mongo.db.Stockdata.find({"company_name":company_name})))
    else:
        datas = loads(dumps(mongo.db.Stockdata.find()))
    list_2 = []
    i = 0
    for data in datas:
        if len(data["data"]) == 23:
            list1 = [da for da in data["data"]]
            list1.append(data['time'])
            list_2.append(list1)
        else:
            i+=1
            
    return list_2, datas, i
            

    

