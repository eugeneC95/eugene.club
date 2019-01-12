from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pymysql
import time
from prettytable import PrettyTable
times = "11/28/2018, 12:34:55 AM";
# for o in range(1,25):
#     if(o >= 12):
#         times = "11/28/2018 "+str(o-12)+":00:00 "+"PM"
#     else:
#         times = "11/28/2018 "+str(o)+":00:00 "+"AM"
#     print(times)
#
#     print("\n")
time1=times.split(" ")
dates = time1[0].split(",")
fdate = dates[0].split("/")
if time1[2] == "PM":
    timed=time1[1].split(":")
    hour = int(timed[0]) + 12
    if hour >= 24:
        hour = hour - 12
    ftime = str(hour)+":"+str(timed[1])+":"+str(timed[2])
elif time1[2] == "AM":
    ftime = time1[1]
fdate = fdate[2]+"-"+fdate[0]+"-"+fdate[1]+" "+ ftime
print(fdate)
