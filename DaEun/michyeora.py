# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import pymysql

"""  이미지 다운로드 class  """
class crawlerImageDownload:
    def imageDownlad(self, imageUrl, name):
        image = urllib.request.urlopen(imageUrl)

        fileName = 'image/' + name[0] + '.jpg'
        imageFile = open(fileName, 'wb')
        imageFile.write(image.read())
        imageFile.close()


def urlOpen(url):
    source_code_from_URL = urllib.request.urlopen(url)
    soup = BeautifulSoup(source_code_from_URL, 'html.parser')

    return soup


if __name__ == '__main__':

    conn = pymysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root',
                           db='forstyle', charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()

    sql = """insert into product(product_brand, product_name, product_cost, product_shopping_img_url, product_shopping_url, product_clothes_label)
                 values (%s, %s, %s, %s, %s, %s)"""

    # Crawling URL
    url = [['http://www.michyeora.com/shop/list.php?cate=07', 'outer'], #outer
           ['http://www.michyeora.com/shop/list.php?cate=0102', 'tee'], #티
           ['http://www.michyeora.com/shop/list.php?cate=0103', 'mantoman'], # 맨투맨
           ['http://www.michyeora.com/shop/list.php?cate=0104', 'knit'], #니트
           ['http://www.michyeora.com/shop/list.php?cate=02', 'blouse'], #블라우스
           ['http://www.michyeora.com/shop/list.php?cate=0303', 'cotton_trousers_long'], #바지
           ['http://www.michyeora.com/shop/list.php?cate=0304', 'cotton_trousers_short'], # 반바지
           ['http://www.michyeora.com/shop/list.php?cate=0302', ' jeans_long'], #청바지 긴거
           ['http://www.michyeora.com/shop/list.php?cate=0301', 'jeans_long'], #청바지 긴거
           ['http://www.michyeora.com/shop/list.php?cate=04', 'skirt'] #치마
           ]

    # Crawling URL
    CRAWLING_URL = 'http://www.michyeora.com'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    for i in range(0, 10):
        product_clothes_label = url[i][1]
        for j in range(1,9):
            page = url[i][0] +"&page=" + str(j)
            print(page)
            soup = urlOpen(page)
            for tm in soup.find_all('li', class_='item xans-record-'):
                img = tm.find('div', class_='box')
                sell = img.find('a')

                product_shopping_url = CRAWLING_URL + str(sell.get('href'))
                print(product_shopping_url)

                img_url = img.find_next('img')
                product_shopping_img_url = img_url.get('src')  # image url
                print(product_shopping_img_url)

                name = tm.find('p', class_='name')
                product_name = name.find('a').get_text()
                print(product_name)

                price = tm.find('ul', class_='xans-element- xans-product xans-product-listitem')
                product_cost = price.find('li').find_next('strong').find_next('span').find_next('span').get_text()
                print(product_cost)

                # curs.execute(sql, ("michyeora", product_name, product_cost, product_shopping_img_url, product_shopping_url, product_clothes_label))

    conn.commit()
    conn.close()
