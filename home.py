import pymysql
import time
import requests
from bs4 import BeautifulSoup

db = pymysql.connect(host='206.189.90.203',user='zun95',passwd='Hotdilvin95',db='kesyou')
cursor = db.cursor()

def main(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text,"lxml")
    #for boxes in soup.find_all("li", class_="pd-productList__item"):
    i = 0
    for a in soup.find_all("a",class_="pd-productList__itemInner"):
        i += 1
        nlink = a['href']
        name = a.find("div",class_="pd-productList__name").string
        tag = a.find("div",class_="pd-productList__category").string
        nlink ="https://www.kanebo-cosmetics.co.jp"+nlink

        newtab = requests.get(nlink)
        newtb = BeautifulSoup(newtab.text,"lxml")
        title = newtb.find("div","pd-productDetail__name").string
        btext = newtb.find("div","pd-productDetail__lead")
        btext = str(btext).replace('<div class="pd-productDetail__lead">','')
        btext = str(btext).replace('</div>','')
        text = newtb.find("div","pd-productDetail__text")
        text = str(text).replace('<div class="pd-productDetail__text">','')
        text = str(text).replace('</div>','')
        caps = newtb.find("div","pd-productDetail__spec").findChildren("dd",recursive=True)
        image = newtb.find("div","pd-image__body").find_next('img')['src']
        image = "https://www.kanebo-cosmetics.co.jp"+str(image)
        idno = nlink.replace("https://www.kanebo-cosmetics.co.jp/products/","")
        site = newtb.find("a","c-button__act")['href']
        print(site)
        s = title.split("　")
        brand = s[0]
        tit = ""
        for title in s[1:]:
            tit = tit + title + " "
        price = str(caps[0].text)
        cap = str(caps[1].text)
        if "ノープリントプライス" in price:
            prices = "0"
        elif "オープンプライス" in price:
            prices = "0"
        else:
            prices = price.replace(" 円（税抜）","")
            prices = prices.replace(",","")
            prices = (float(prices) * 1.08)
        cursor.execute("SELECT * FROM hin WHERE id_no LIKE %s",(idno))
        datas = cursor.fetchall()
        # if len(datas) >= 1:
        #     print(str(i)+" data duplicated")
        # else:
        #     print(str(i)+" Inserting Data")
        #     cursor.execute("INSERT into hin(id_no,brand,name_jp,description_jp,price,cap,type) VALUES(%s ,%s ,%s ,%s ,%s ,%s ,%s)",(idno,brand,tit,str(btext)+str(text),prices,cap,'0'))
        #     db.commit()
        #     cursor.execute("INSERT into g (id_no,thumbnail) VALUES(%s ,%s)",(idno,image))
        #     db.commit()


        # try:
        #     print(tit)
        #     cursor.execute("INSERT into hin(id_no,brand,name_jp,description_jp,price,cap,type) VALUES(%s ,%s ,%s ,%s ,%s ,%s ,%s)",(idno,brand,tit,str(btext)+str(text),prices,cap,'0'))
        #     db.commit()
        # except:
        #     print('error inserting')
        #     db.rollback()

        # f = open('helloworld.txt','a')
        # f.write(prices)

        # f.write(str(tit) +'\n')
        # f.write('\n' + title)
        # f.write('\n' + tag)
        # f.write('\n' + nlink)
        # f.write('\n' + str(btext)+str(text))
        # for cap in caps:
        #     f.write(str(cap.text))
        # f.write('\n' + str(image))

    #     f.write('\n')
    #     f.close()
    #
    # print("\n")

main("https://www.kanebo-cosmetics.co.jp/products/search?keyword=&brand_id=&category1=2&category2%5B%5D=40&price_from=&price_to=&period=&search=1#")
#main("https://www.kanebo-cosmetics.co.jp/products/search?keyword=%E3%83%AB%E3%83%8A%E3%82%BD%E3%83%AB%E3%80%80%E3%82%B6%E3%80%80%E3%83%99%E3%83%BC%E3%82%B8%E3%83%A5%E3%82%A2%E3%82%A4%E3%82%BA&brand_id=&category1=&category2%5B%5D=3&price_from=&price_to=&period=&search=1#result")
db.close()
