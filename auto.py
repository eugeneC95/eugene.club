from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pymysql
import time

options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}

options.add_experimental_option("prefs",prefs)
options.add_argument("--window-size=100,150")#--start-maximized
driver = webdriver.Chrome("D:/Documents/Career/eugene.club/chromedriver.exe",options=options)

db = pymysql.connect(host='206.189.90.203',user='zun95',passwd='Hotdilvin95',db='h')
cursor = db.cursor()
def insert(tit,aut,page,tsrc,isrc,tp,date):
    try:
        cursor.execute("INSERT into post(title,author,page,t_src,i_src,i_type,created_date) VALUES(%s ,%s ,%s, %s, %s, %s, %s)",(tit,aut,page,tsrc,isrc,tp,date))
        db.commit()
    except:
        print('error inserting')
        db.rollback()
def check(x,i,j,k,l,m,n,o):
    try:
        cursor.execute("SELECT * FROM post WHERE t_src LIKE %s ORDER BY created_date ASC",(x))
        datas = cursor.fetchall()
        if len(datas) > 1:
            print("Data Already saved in DB")
        else:
            #donothings
            insert(i,j,k,l,m,n,o)
            print("insert new data to table")
    except:
        print ("Error getting data for check")
        driver.close()
def main(j):
    #link = "https://nhentai.net/tag/stockings/?page="+str(j)
    link = "https://nhentai.net/?page="+str(j)
    driver.get(link);
    time.sleep(1)
    box = driver.find_elements_by_class_name('gallery')
    for i in range(1,len(box)):
        try:
            texts = driver.find_element_by_xpath("//div[@class='container index-container']//div["+str(i)+"]//a").text
            print(texts)
            if("Chinese" in texts):
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
                img= "https://i.nhentai.net/galleries/"+str(img_no[0])+"/"
                date= driver.find_element_by_xpath("//div[@id='info']//div[2]//time").get_attribute('datetime')
                date1=date.split("T")
                date2=date1[1].split(".")
                fdate =date1[0]+" "+date2[0]
                print(cover,img)
                check(cover,title,artist[0],page,cover,img,type,fdate)
                time.sleep(0.5)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                print("\n")
            else:
                print(str(i)+"no Chinese file")
        except NoSuchElementException:
            print(str(i)+"error")
for j in range(1,15):
    if j == 11:
        j=1
    main(j)
    j = j+1