import numpy as np 
import pandas as pd
from .server import *
from .Constants import *
import time

def data_sorting(company_code:str=None):
    #individual company data cleaning from server datas
    if company_code == None:
        datas, _,_ = Data_revive()
        cso = "stockmarket"
    else:
        datas, _,_ = Data_revive(company_code)
        cso = company_code
    df = pd.DataFrame(datas, columns=column_names)
    df1 = pd.DataFrame({
    "date":df.loc[:,"date"],
    "open":df.loc[:,'OpeningPrice'],
    "high":df.loc[:, "high"],
    "low":df.loc[:, 'low'],
    "close":df.loc[:,'LastTradingPrice'],
    "volume":df.loc[:,"Day'sVolume(Nos"],})
    df1.replace("-", 0).to_csv(f"data/csv_data/{cso}_modified.csv", index=False)
    return "success", cso


