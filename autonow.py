from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pymysql
import time
import schedule

# coding: utf-8
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
    datas = []
    if "(" or "[" in data:
        for l in range(len(data)):
            if "[" == data[l]:
                for m in range(l,len(data)):
                    auth += data[m]
                    if "]" == data[m]:
                        datas.append(auth)
                        auth = ""
                        break
            elif "(" == data[l]:
                for m in range(l,len(data)):
                    auth += data[m]
                    if ")" == data[m]:
                        datas.append(auth)
                        auth = ""
                        break
        try:
            for i in range(len(datas)):
                data = data.replace(datas[i],"")
            data = data.replace(" ","")
            return data
        except Exception as e:
            print("retitle error")
def insert(tit,aut,page,tsrc,isrc,tp,date):
    try:
        cursor.execute("INSERT into book_data(title,author,page,t_src,i_no,i_type,pop,created_date) VALUES(%s ,%s ,%s, %s, %s, %s, %s, %s)",(tit,aut,page,tsrc,isrc,tp,'0',date))
        db.commit()
    except:
        print('error inserting')
        db.rollback()
def insert_tag(i_no,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,date,p,q):
    try:
        cursor.execute("INSERT into book_tag(i_no,stocking,pantyhose,purelove,wetcloth,schoolgirl,fullcolor,darkskin,footjob,length,doujinshi,manga,drug,toys,bondage,rape,created_date,breast,loli,likes,unlikes)VALUES(%s ,%s ,%s, %s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s)",(i_no,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,date,p,q,'0','0'))
        db.commit()
        print("tag_inserted")
    except:
        print('error inserting_tag')
        db.rollback()
def check(x,y,z,i,j,k,l,m,n,o):
    try:
        stocking,pantyhose,purelove,wetcloth,schoolgirl,fullcolor,darkskin,footjob,length,doujin,manga,drug,toys,bondage,rape,breast,loli,likes,unlikes = "0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"
        cursor.execute("SELECT * FROM book_data WHERE t_src LIKE %s OR title LIKE %s ORDER BY created_date ASC",(x,y))
        datas = cursor.fetchall()
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
            if 'loli' in s.text:
                loli = "1"
            if k >= 30:
                length = "1"
        if len(datas) and len(tags) >= 1:
            print("Data_Duplicated")
            print("Tag_Duplicated")
        elif len(datas) <= 0 and len(tags) <=0:
            insert(i,j,k,l,m,n,o)
            print("book_inserted")
            insert_tag(z,stocking,pantyhose,purelove,wetcloth,schoolgirl,fullcolor,darkskin,footjob,length,doujin,manga,drug,toys,bondage,rape,o,breast,loli)
            print("tag_inserted")
    except:
        print ("Error getting data for check")
        driver.close()
def main(j,link):
    driver.get(link);
    box = driver.find_elements_by_class_name('gallery')
    for i in range(1,len(box)):
        try:
            texts = driver.find_element_by_xpath("//div[@class='container index-container']//div["+str(i)+"]//a").text
            if("Chinese" in texts or "化" in texts):
                link = driver.find_element_by_xpath("//div[@class='container index-container']//div["+str(i)+"]//a[1]").get_attribute("href")
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                title= driver.find_element_by_xpath("//div[@class='container']//div[@id='info']//h2").text
                title = retitle(title)
                try:
                    artist= driver.find_element_by_xpath("//section[@id='tags']//div[4]//span[@class='tags']//a").text
                except NoSuchElementException:
                    artist= driver.find_element_by_xpath("//section[@id='tags']//div[5]//span[@class='tags']//a").text
                artist = artist.split(' (')
                page= driver.find_elements_by_xpath("//div[@class='container']//div[@class='thumb-container']")
                page=len(page)
                cover= driver.find_element_by_xpath("//div[@id='cover']//img[1]").get_attribute('data-src')
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
                        hour = hour - 12
                    ftime = str(hour)+":"+str(timed[1])+":"+str(timed[2])
                elif time1[2] == "AM":
                    ftime = time1[1]
                fdate = fdate[2]+"-"+fdate[0]+"-"+fdate[1]+" "+ ftime
                link += "1/"
                driver.get(link)
                bg = driver.find_element_by_xpath("//img[@class='fit-horizontal']").get_attribute('src')
                if "png" in bg:
                    type='png'
                elif "jpg" in bg:
                    type='jpg'
                check(cover,title,img,title,artist[0],page,cover,img,type,fdate)
                time.sleep(0.1)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            print(str(i)+"\n")
        except NoSuchElementException:
            print(str(i)+"error")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
j = 0
while(j < 50):
    j += 1
    print("Page" + str(j))
    main(j,"https://nhentai.net/?page="+str(j))
driver.close()
