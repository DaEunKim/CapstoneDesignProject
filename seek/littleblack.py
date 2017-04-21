    #-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import pymysql

"""  이미지 다운로드 class  """
class crawlerImageDownload:
    def imageDownlad(self, imageUrl,name):
        image = urllib.request.urlopen(imageUrl)
        fileName = 'image/'+ name + '.jpg'
        imageFile = open(fileName, 'wb')
        imageFile.write(image.read())
        imageFile.close()

if __name__ == '__main__':
    # MySQL Connection 연결
    conn = pymysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root',db='forstyle', charset='utf8')

    
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()

    sql = """insert into product(product_brand,product_name,product_cost,product_clothes_label,product_shopping_img_url,product_shopping_url)
         values (%s, %s, %s, %s, %s, %s)"""
     
    # Crawling URL
    URL = [['http://www.littleblack.co.kr/product/list.html?cate_no=31','outer'],
           ['http://www.littleblack.co.kr/product/list.html?cate_no=24','top'],
           ['http://www.littleblack.co.kr/product/list.html?cate_no=34','knit'],
           ['http://www.littleblack.co.kr/product/list.html?cate_no=26','onepiecedress'],
           ['http://www.littleblack.co.kr/product/list.html?cate_no=25','bottom']]

    # Crawling URL
    CRAWLING_URL = 'http://www.littleblack.co.kr'
    
    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    

    for i in range(0,5):
        source_code_from_URL = urllib.request.urlopen(URL[i][0])
        soup = BeautifulSoup(source_code_from_URL, 'html.parser')
        next_page = soup.find("p",{"class","last"})
        next_page = next_page.find("a").get("href")
        temp = next_page.split('&')
        temp2 = temp[1].split('=')
        last_page = temp2[1]
        product_clothes_label = URL[i][1]
        
        for page in range(1,int(last_page)+1):
            url = URL[i][0] + "&page=" + str(page)
            source_code_from_URL = urllib.request.urlopen(url)
            soup = BeautifulSoup(source_code_from_URL, 'html.parser')
            for classid in soup.find_all("li",{"class","item xans-record-"}):
                img = classid.find("img")
                    
                #print img_url
                product_shopping_img_url = img.get("src")[2:]
                print(product_shopping_img_url)
                product_shopping_img_url='http://'+product_shopping_img_url
                    
                class_name = classid.find("p",{"class","name"})
                name = class_name.find_all('span')
                product = class_name.find("a")
                product_shopping_url = URL[i][0]+product.get("href")
                    
                #print product_url
                print(product_shopping_url)
                    
                #print product_name
                product_name = name[1].get_text()
                print(product_name)
                    
                class_cost = classid.find("ul",{"class","xans-element- xans-product xans-product-listitem"})
                if class_cost is None:
                    print("\n\n")
                    continue
                cost = class_cost.find_all('span')
                    
                #print cost
                product_cost = cost[1].get_text()
                print(product_cost)
                print("\n\n")
                curs.execute(sql,("littleblack",product_name,product_cost,product_clothes_label,product_shopping_img_url,product_shopping_url))

    # Connection 닫기
    conn.commit()
    conn.close()         
 


