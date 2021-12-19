from flask import Flask, jsonify
from data import *
import data.Constants as con

app = Flask(__name__)

@app.route("/")
def welcome():
    return jsonify({
        "WelcomeNote":"Welcome to the AIIM-Trading",
        "NOTE":"(route_for_saving_data) route run only for one time per day.",
        "route_for_saving_data":"/saving_data",
        "all data":"/all_data"})

@app.route("/saving_data")
def data_scraping_and_saving_to_server():
    #scraping from dse and save the necessary data to server
    a = time.time()
    server.Company_data_saving(companies=con.companies) #save the datas
    b = time.time()
    return jsonify({"result":"success","Consuming_time":b-a})

@app.route("/all_data")
def all_data_from_server():
    _, datas,_23_data_doesnot_exist=server.Data_revive()
    return jsonify({"_data_no":len(datas), "23_data_doesnot_exist":_23_data_doesnot_exist})

if __name__ == "__main__":
    app.run(debug=True, port=4699)
