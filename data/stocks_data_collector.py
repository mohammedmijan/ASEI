import requests
import bs4
import time
import re
from .Constants import *
"""

company_lists = "https://dhaka-stock-exchange-fastest-dse1.p.rapidapi.com/api/v1/company-list/"

headers={
'x-rapidapi-host': 'dhaka-stock-exchange-fastest-dse1.p.rapidapi.com',
    'x-rapidapi-key': '3dc30f10d3mshe1251bf3c40577cp10cef6jsn38fbdc12cb18'
  }

headers2 = {'x-rapidapi-host': 'dhaka-stock-exchange-dse.p.rapidapi.com',
    'x-rapidapi-key': '3dc30f10d3mshe1251bf3c40577cp10cef6jsn38fbdc12cb18'} #it is needed to suscribe

company_list = requests.get(company_lists, headers=headers).json()


def current_stock():
  current_stock_price_lists = []
  for company_name in company_list["data"]:
    current_stock_prices = "https://dhaka-stock-exchange-fastest-dse1.p.rapidapi.com/api/v1/current-stock-price/"
    params = {"company_trading_code" : company_name ,"duration": '1', "type": 'price'}
    current_stock_price = requests.get(current_stock_prices, params=params, headers=headers).json()
    current_stock_price_lists.append(current_stock_price)
  return current_stock_price_lists

def company_stat():
  company_stats_lists = []
  for company_name in company_list["data"]:
    company_statistics = "https://dhaka-stock-exchange-fastest-dse1.p.rapidapi.com/api/v1/company-statistics/"
    params = {"company_trading_code" : company_name ,"duration": '1', "type": 'price'}
    company_stats = requests.get(company_statistics, params=params, headers=headers).json()
    company_stats_lists.append(company_stats)
  return company_stats_lists

def company_detail():
  current_stock_price_lists = []
  for company_name in company_list["data"]:
    company_details = "https://dhaka-stock-exchange-fastest-dse1.p.rapidapi.com/api/v1/company-details/"
    params = {"company_trading_code" : company_name ,"duration": '1', "type": 'price'}
    current_stock_price = requests.get(company_details, params=params, headers=headers).json()
    current_stock_price_lists.append({company_name:current_stock_price["data"]["market_info"]})
    print(company_name)
  return current_stock_price_lists
  #return current_stock_price_lists

"""
def data_from_dse_website(company_name):
  #Scraping data from the dse url
  i = 0
  ShareHoldingPercentage = []
  list_of_data = name_of_columns_data
  url = f"https://www.dsebd.org/displayCompany.php?name={company_name}"
  r = requests.get(url)
  htmlContent = r.content
  soup = bs4.BeautifulSoup(htmlContent, "html.parser")
  soups = soup.find_all("div", class_='table-responsive')
  list_S = []
  for soup_ in soups:
    data_mixing = soup_.find_all("table", id="company")
    for data_unspliting in data_mixing:
      data_spliting = data_unspliting.find_all("tr")
      for data in data_spliting:
        da = data.text.replace(" ", "").split()
        if (da != []):
          if da[0] in list_of_data :
              list_S.append({da[i].split(".")[0]:da[i+1]})
              if len(da) > 2:
                list_S.append({da[i+2].split(".")[0]:da[i+3]})
    
          if da[0] in  ["ShareHoldingPercentage"]:
            ShareHoldingPercentage.append(da)
        
  print(ShareHoldingPercentage)
  #not completed scarping
  return list_S
    

  
          