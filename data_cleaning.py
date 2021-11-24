import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import server
import Constants 
import time

def data_sorting(company_code:list=None):
    if company_code == None:
        datas = server.Data_revive_to_all_companies()
    else:
        datas = server.Data_revive(company_code)
    npa = np.array(datas)
    df = pd.DataFrame(npa, columns=Constants.column_names)
    df.replace("-", 0).to_csv("stock.csv")
    return "Success"
a = time.time()
server.Company_data_saving(Constants.companies)
print(data_sorting())
b = time.time()
print(f"{b-a}seconds")