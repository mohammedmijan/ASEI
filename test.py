from data import *
from data import Constants


server.Company_data_saving(companies=Constants.companies)
for ccc in Constants.Engineering_companies:
    print(data_sorting(ccc))

for ccc in Constants.It_companies:
    print(data_sorting(ccc))