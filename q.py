from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pymysql
import time


data ="(C88) [KAMINENDO.CORP (あかざわRED)] でれパコ (アイドルマスターシンデレラガールズ) [中国翻訳]"
auth =""
tit =""
if "[" in data:
    for l in range(len(data)):
        if "[" == data[l]:
            for m in range(l,len(data)):
                auth += data[m]
                if "]" == data[m]:
                    data = data.replace(auth,"")
                    auth =""
                    break
        if "(" in data:
            if "(" == data[l]:
                for m in range(l,len(data)):
                    tit +=data[m]
                    if ")" == data[m]:
                        data = data.replace(tit,"")
                        tit =""
                        break
        elif "[" not in data:
            data = data.replace(" ","")
            print(data)
            break
