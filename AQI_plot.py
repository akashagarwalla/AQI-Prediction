# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:10:13 2020

@author: Akash Agarwalla
"""

import pandas as pd
import matplotlib.pyplot as plt

def avg_AQI(year):
    cnt = 0
    average = []
    for rows in pd.read_csv('Data/AQI_Data/aqi{}.csv'.format(year),chunksize=24):
        avg = 0.0
        hrly_aqi = 0
        data = []
        df = pd.DataFrame(data=rows)
        for index,row in df.iterrows():
            data.append(row['PM2.5'])
        for i in data:
            if type(i) is float or type(i) is int:
                hrly_aqi = hrly_aqi + i
            elif type(i) is str:
                if i!= 'NoData' and i!='PwrFail' and i!='InVld' and i!= '---':
                    temp = float(i)
                    hrly_aqi = hrly_aqi + temp
        avg = hrly_aqi/24
        cnt += 1
        average.append(avg)
    
    if is_leap_year(year) == True:
        average.insert(365,'-')
        
    return average

def is_leap_year (year):
  return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0) 

 
if __name__ == '__main__':
    aqi_2013 = avg_AQI(2013)
    aqi_2014 = avg_AQI(2014)
    aqi_2015 = avg_AQI(2015)
    aqi_2016 = avg_AQI(2016)
    
    plt.plot(range(0,len(aqi_2013)),aqi_2013,label = '2013_AQI data')
    plt.plot(range(0,len(aqi_2014)),aqi_2014,label = '2014_AQI data')
    plt.plot(range(0,len(aqi_2015)),aqi_2015,label = '2015_AQI data')
    plt.plot(range(0,len(aqi_2016)),aqi_2016,label = '2016_AQI data')
    plt.xlabel('Day')
    plt.ylabel('PM 2.5')
    plt.legend(loc = 'upper right')
    plt.show()