    #-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import re
import pymysql

"""  이미지 다운로드 class  """
class crawlerImageDownload:
    def imageDownlad(self, imageUrl,name):
        image = urllib.request.urlopen(imageUrl)

        fileName = 'image/'+ name[0] + '.jpg'
        imageFile = open(fileName, 'wb')
        imageFile.write(image.read())
        imageFile.close()

if __name__ == '__main__':
    # MySQL Connection 연결
    conn = pymysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root',db='forstyle', charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
  

    sql = """insert into product(product_brand,product_name,product_cost,product_shopping_img_url,product_shopping_url,product_clothes_label)
         values (%s, %s, %s, %s, %s,%s)"""

    url = [["http://www.tate.co.kr/product/list.asp?cNo=9","coat,padding,outer"],
           ["http://www.tate.co.kr/product/list.asp?cNo=8","knit,cardigon"],
           ["http://www.tate.co.kr/product/list.asp?cNo=43","mantoman"],
           ["http://www.tate.co.kr/product/list.asp?cNo=6","blouse,shirt"],
           ["http://www.tate.co.kr/product/list.asp?cNo=33","tee"],
           ["http://www.tate.co.kr/product/list.asp?cNo=7","onepiecedress,skirt"],
           ["http://www.tate.co.kr/product/list.asp?cNo=13","bottom"],
           ["http://www.tate.co.kr/product/list.asp?cNo=11","bottom"],
           ["http://www.tate.co.kr/product/list.asp?cNo=18","knit,cardigon"],
           ["http://www.tate.co.kr/product/list.asp?cNo=44","mantoman"],
           ["http://www.tate.co.kr/product/list.asp?cNo=15","shirt"],
           ["http://www.tate.co.kr/product/list.asp?cNo=16","knit,cardigon"],
           ["http://www.tate.co.kr/product/list.asp?cNo=36","tee"],
           ["http://www.tate.co.kr/product/list.asp?cNo=37","tee"],
           ["http://www.tate.co.kr/product/list.asp?cNo=20","bottom"],
           ["http://www.tate.co.kr/product/list.asp?cNo=19","bottom"],]
    
    # Crawling URL
    CRAWLING_URL = 'http://www.tate.co.kr/'
    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    source_code_from_URL = urllib.request.urlopen(CRAWLING_URL)

    soup = BeautifulSoup(source_code_from_URL, 'html.parser')
    cartegory = soup.find("nav",{"class","gnb"})
    for i in range(0,16):
        source_code_from_URL = urllib.request.urlopen(url[i][0])
        soup = BeautifulSoup(source_code_from_URL, 'html.parser')
        
        next_page = soup.find("div",{"class","paging"})
        next_page = next_page.find_all("a")
        last_page = len(next_page)-1
        product_clothes_label = url[i][1]
        if last_page == 0:
            last_page = 1
        for page in range(1,int(last_page)+1):
            page_url = url[i][0] + "&page=" + str(page)
            source_code_from_URL = urllib.request.urlopen(page_url)
            soup = BeautifulSoup(source_code_from_URL, 'html.parser')
            soup = soup.find("div",{"class","goods_list"})
            for classid in soup.find_all("li"):
                img = classid.find("img")
                
                #print img_url
                product_shopping_img_url = img.get("src")
                print(product_shopping_img_url)

    
                product = classid.find("a")
                product_shopping_url = CRAWLING_URL+product.get("href")
                
                #print product_url
                print(product_shopping_url)
                
                #print product_name
                name = classid.find("p",{"class","name"})
                product_name = name.get_text()
                print(product_name)
                
                #print cost
                cost = classid.find("p",{"class","price"})
                cost = cost.find_all("span")
                if len(cost[0])==1:
                    product_cost=cost[0].get_text("span")
                else:
                    product_cost=cost[1].get_text("span")

                print(product_cost)
                #print category_name
                print(product_clothes_label)
                curs.execute(sql,("tate",product_name,product_cost,product_shopping_img_url,product_shopping_url,product_clothes_label))
             
                
                
    # Connection 닫기
    conn.commit()
    conn.close()
             

