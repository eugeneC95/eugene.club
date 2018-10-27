from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pymysql
import time

options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}

options.add_experimental_option("prefs",prefs)
options.add_argument("--window-size=100,100")#--start-maximized
driver = webdriver.Chrome("D:/Documents/Career/eugene.club/chromedriver.exe",options=options)

link = "https://nhentai.net/g/251115/"

driver.get(link)

title= driver.find_element_by_xpath("//div[@class='container']//div[@id='info']//h2[1]").text
print("title: "+str(title))
