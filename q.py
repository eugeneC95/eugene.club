from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pymysql
import time

db = pymysql.connect(host='206.189.90.203',user='zun95',passwd='Hotdilvin95',db='h')
cursor = db.cursor()

def analys_author():
    i = 0
    j = 0
    print("program started")
    cursor.execute("SELECT * FROM author")
    authors = cursor.fetchall()
    for author in authors:
        i += 1
        artist = author[1]
        print("auth "+str(i)+" artist: "+str(artist))
        cursor.execute("SELECT * FROM post")
        posts = cursor.fetchall()
        for post in posts:
            j += 1
            print("post "+str(j)+" artist: "+str(post[2]))
            if str(artist) == str(post[2]):
            #artist are post data,author[1] are author data
            #[1] is eng [2] is japanese
                print(str(post[2]+" to "+str(author[2])))
                try:
                    cursor.execute("UPDATE post SET author = %s WHERE author = %s",(author[2],post[2]))
                    db.commit()
                    print("UPDATE DONE.")
                except:
                    print("error UPDATE")
                    db.rollback()
        j = 0
analys_author()
db.close()
