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
def insert(tit,aut,page,tsrc,isrc,tp,date):
    try:
        cursor.execute("INSERT into post(title,author,page,t_src,i_no,i_type,created_date) VALUES(%s ,%s ,%s, %s, %s, %s, %s)",(tit,aut,page,tsrc,isrc,tp,date))
        db.commit()
    except:
        print('error inserting')
        db.rollback()
def check(x,y,z,i,j,k,l,m,n,o):
    try:
        cursor.execute("SELECT * FROM post WHERE t_src LIKE %s OR title LIKE %s ORDER BY created_date ASC",(x,y))
        datas = cursor.fetchall()
        cursor.execute("SELECT * FROM blacklist WHERE i_no = %s",(z))
        blacks = cursor.fetchall()
        for data in datas:
            print("Found data: "+data[4])
        if len(datas) >= 1:
            print("Data Already saved in DB")
        elif len(blacks) >= 1:
            print("Data Blacklisted")
        else:
            insert(i,j,k,l,m,n,o)
            print("insert new data to table")
    except:
        print ("Error getting data for check")
        driver.close()
def main(j,link):
    driver.get(link);
    time.sleep(1)
    box = driver.find_elements_by_class_name('gallery')
    for i in range(1,len(box)):
        try:
            texts = driver.find_element_by_xpath("//div[@class='container index-container']//div["+str(i)+"]//a").text
            if(("Chinese" or "化") in texts):
                link = driver.find_element_by_xpath("//div[@class='container index-container']//div["+str(i)+"]//a[1]").get_attribute("href")
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                title= driver.find_element_by_xpath("//div[@class='container']//div[@id='info']//h2").text
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
                date= driver.find_element_by_xpath("//div[@id='info']//div[2]//time").get_attribute('datetime')
                date1=date.split("T")
                date2=date1[1].split(".")
                fdate =date1[0]+" "+date2[0]
                print(cover)
                check(cover,title,img,title,artist[0],page,cover,img,type,fdate)
                time.sleep(0.5)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            else:
                print(str(i)+" no Chinese file")
        except NoSuchElementException:
            print(str(i)+"error")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    j = j+1
    link = "https://nhentai.net/?page="+str(j)
    if j >= 100:
        j = 1
        link = "https://nhentai.net/tag/stockings?page="+str(j)
        analys_author()
    main(j,link)

main(1,"https://nhentai.net/tag/stockings/?page=1")
db.close()
