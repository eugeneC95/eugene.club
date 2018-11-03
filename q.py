from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pymysql
import time


data ="[三生万] 嫦娥造反记 (连载中)"
auth =""
tit =""
if "[" in data:
    for l in range(len(data)):
        if "[" not in data and "(" not in data:
            data = data.replace(" ","")
            break
        elif "[" == data[l]:
            for m in range(l,len(data)):
                auth += data[m]
                if "]" == data[m]:
                    data = data.replace(auth,"")
                    auth =""
                    break
        elif "(" in data:
            if "(" == data[l]:
                for m in range(l,len(data)):
                    tit +=data[m]
                    if ")" == data[m]:
                        data = data.replace(tit,"")
                        tit =""
                        break

print(data)
