from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pymysql
import time

options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}

options.add_experimental_option("prefs",prefs)
options.add_argument("--window-size=650,150")#--start-maximized
driver = webdriver.Chrome("D:/Documents/Career/eugene.club/chromedriver.exe",options=options)

db = pymysql.connect(host='206.189.90.203',user='zun95',passwd='Hotdilvin95',db='h')
cursor = db.cursor()

def retitle(data):
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

    return data
def insert(tit,aut,page,tsrc,isrc,tp,date):
    try:
        cursor.execute("INSERT into book_data(title,author,page,t_src,i_no,i_type,pop,created_date) VALUES(%s ,%s ,%s, %s, %s, %s, %s, %s)",(tit,aut,page,tsrc,isrc,tp,'0',date))
        db.commit()
    except:
        print('error inserting')
        db.rollback()
def insert_tag(i_no,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,date,p):
    try:
        cursor.execute("INSERT into book_tag(i_no,stocking,pantyhose,purelove,wetcloth,schoolgirl,fullcolor,darkskin,footjob,length,doujinshi,manga,drug,toys,bondage,rape,created_date,breast,likes,unlikes)VALUES(%s ,%s ,%s, %s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)",(i_no,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,date,p,'0','0'))
        db.commit()
        print("tag_inserted")
    except:
        print('error inserting_tag')
        db.rollback()
def check(x,y,z,i,j,k,l,m,n,o):
    try:
        stocking,pantyhose,purelove,wetcloth,schoolgirl,fullcolor,darkskin,footjob,length,doujin,manga,drug,toys,bondage,rape,breast,likes,unlikes = "0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"
        cursor.execute("SELECT * FROM book_data WHERE t_src LIKE %s OR title LIKE %s ORDER BY created_date ASC",(x,y))
        datas = cursor.fetchall()
        cursor.execute("SELECT * FROM admin_blacklist WHERE i_no = %s",(z))
        blacks = cursor.fetchall()
        cursor.execute("SELECT * FROM book_tag WHERE i_no = %s",(z))
        tags = cursor.fetchall()
        tagsz = driver.find_elements_by_xpath("//section[@id='tags']//span[@class='tags']")
        for s in tagsz:
            if 'stocking' in s.text:
                stocking = "1"
            if 'pantyhose' in s.text:
                pantyhose = "1"
            if 'purelove' in s.text:
                purelove = "1"
            if 'wet clothes' in s.text:
                wetcloth = "1"
            if 'schoolgirl' in s.text:
                schoolgirl = "1"
            if 'full color' in s.text:
                fullcolor = "1"
            if 'dark skin' in s.text:
                darkskin = "1"
            if 'footjob' in s.text:
                footjob = "1"
            if 'doujinshi' in s.text:
                doujin = "1"
            if 'manga' in s.text:
                manga = "1"
            if 'drug' in s.text:
                drug = "1"
            if 'toys' in s.text:
                toys = "1"
            if 'bondage' in s.text:
                bondage = "1"
            if 'rape' in s.text:
                rape = "1"
            if 'breast' in s.text:
                breast = "1"
            if k >= 30:
                length = "1"
        for data in datas:
            print("Found: "+data[4])
        if len(blacks) >= 1:
            print("Data_Blacklisted")
        elif len(datas) and len(tags) >= 1:
            print("Data_Duplicated")
            print("Tag_Duplicated")
        elif len(datas) >= 1 and len(tags) == 0:
            print("Data_Duplicated")
            insert_tag(z,stocking,pantyhose,purelove,wetcloth,schoolgirl,fullcolor,darkskin,footjob,length,doujin,manga,drug,toys,bondage,rape,o,breast)
            print("tag_inserted")
        elif len(datas) == 0 and len(tags) ==0:
            insert(i,j,k,l,m,n,o)
            print("book_inserted")
            insert_tag(z,stocking,pantyhose,purelove,wetcloth,schoolgirl,fullcolor,darkskin,footjob,length,doujin,manga,drug,toys,bondage,rape,o,breast)
            print("tag_inserted")
    except:
        print ("Error getting data for check")
        driver.close()
def main(link):
    driver.get(link);
    try:
        title= driver.find_element_by_xpath("//div[@class='container']//div[@id='info']//h2").text
        title = retitle(title)
        artist= driver.find_element_by_xpath("//section[@id='tags']//div[4]//span[@class='tags']//a").text
        artist = artist.split(' (')
        page= driver.find_elements_by_xpath("//div[@class='container']//div[@class='thumb-container']")
        page=len(page)
        cover= driver.find_element_by_xpath("//div[@id='cover']//img[1]").get_attribute('data-src')
        if "png" in cover:
            type='png'
        elif "jpg" in cover:
            type='jpg'
        img_nos= cover.split("https://t.nhentai.net/galleries/")
        img_no= img_nos[1].split("/cover")
        img= str(img_no[0])
        times= driver.find_element_by_xpath("//div[@id='info']//div[2]//time").get_attribute('title')
        time1=times.split(" ")
        dates = time1[0].split(",")
        fdate = dates[0].split("/")
        if time1[2] == "PM":
            timed=time1[1].split(":")
            hour = int(timed[0]) + 12
            if hour >= 24:
                hour = hour - 24
            ftime = str(hour)+":"+str(timed[1])+":"+str(timed[2])
        elif time1[2] == "AM":
            ftime = time1[1]
        fdate = fdate[2]+"-"+fdate[0]+"-"+fdate[1]+" "+ ftime
        print(cover)
        check(cover,title,img,title,artist[0],page,cover,img,type,fdate)
    except NoSuchElementException:
        print("error")
list = []
f=open("list.txt", "r")
if f.mode == 'r':
    data = f.readlines()
    for line in data:
        main(line)
