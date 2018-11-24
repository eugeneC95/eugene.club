from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pymysql
import time
from prettytable import PrettyTable
texts = "(C91) [Asanebou Crisis (Akaneman)] Kachiku Choukyou Soshiki CHALDEA (Fate/Grand Order) [Chiese] [不咕鸟汉化组]"
if("Chinese" in texts or "化" in texts):
    print("got")
else:
    print("nothing")
