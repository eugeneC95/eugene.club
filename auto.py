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
    if j >= 15:
        j = 1
    main(j,link)

main(1,"https://nhentai.net/?page=1")
db.close()
