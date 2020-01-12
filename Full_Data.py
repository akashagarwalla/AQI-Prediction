from bs4 import BeautifulSoup
import pandas as pd
from AQI_plot import avg_AQI
import csv
import os

def features(year,month):
    html_file = open('Data/Html_data/{}/{}.html'.format(year,month),'rb')
    html_text = html_file.read()
    
    soup = BeautifulSoup(html_text,'lxml')
    
    temp_Data = []
    for table in soup.findAll('table',{'class':'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                txt = tr.get_text()
                temp_Data.append(txt)
                
    final_Data = []
    no_features = 15
    rows = round(len(temp_Data)/no_features)
    
    for i in range(rows):
        temp1_Data = []
        for j in range(no_features):
            temp1_Data.append(temp_Data[0])
            temp_Data.pop(0)
            print(temp1_Data)
        final_Data.append(temp1_Data)
        
    length = len(final_Data)    
    final_Data.pop(length-1)
    final_Data.pop(0)
    
    for a in range(len(final_Data)):
        final_Data[a].pop(6)
        final_Data[a].pop(13)
        final_Data[a].pop(12)
        final_Data[a].pop(11)
        final_Data[a].pop(10)
        final_Data[a].pop(9)
        final_Data[a].pop(0)
    return final_Data

def data_combine(year, cs):
    for a in pd.read_csv('Data/Real_Data/Real_{}.csv'.format(year), chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist

if __name__ == '__main__':
    if not os.path.exists('Data/Real_Data'):
        os.makedirs('Data/Real_Data')
    for year in range(2013,2017):
        final_data = []
        with open('Data/Real_Data/Real_{}.csv'.format(year),'w') as csvfile:
            wr = csv.writer(csvfile,dialect='excel')
            wr.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(1,13):
                temp = features(year,month)
                final_data = final_data + temp
                
        pm2_5 = avg_AQI(year)
        if len(pm2_5) == 364:
            pm2_5.insert(364, '-')
        for i in range(len(final_data)):
            final_data[i].insert(8,pm2_5[i])
        with open('Data/Real_Data/Real_{}.csv'.format(year),'a') as csvfile:
            wr = csv.writer(csvfile,dialect='excel')
            for row in final_data:
                flag = 0
                for element in row:
                    if element == "" or element == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)
    data_2013 = data_combine(2013, 600)
    data_2014 = data_combine(2014, 600)
    data_2015 = data_combine(2015, 600)
    data_2016 = data_combine(2016, 600)
     
    total=data_2013+data_2014+data_2015+data_2016
    
    with open('Data/Real_Data/Real_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
        
        
    df=pd.read_csv('Data/Real_Data/Real_Combine.csv')
