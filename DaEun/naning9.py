# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os
import urllib.request
import pymysql
import re

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

    db = pymysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root',
                         db='forstyle', charset='utf8')
    cur = db.cursor()
    # t = cur.execute("SELECT * FROM product")  # sql문 실행

    t = """INSERT INTO product (product_brand, product_name, product_cost, product_shopping_img_url, product_shopping_url, product_clothes_label) VALUES (%s %s %s %s %s %s)"""

    # Crawling URL
    CRAWLING_URL = 'http://www.naning9.com'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    soup = urlOpen(CRAWLING_URL)
    # 카테고리 리스트 저장할 변수
    category_list = []

    for category in soup.find_all('div', class_='sub_lnb_wrap'):
        for link in category.find_all('a'):
            line = CRAWLING_URL + str(link.get('href'))

            if line[-1] == 'p' and line[-2] == 'h' and line[-3] == 'p':
                continue

            soup2 = urlOpen(line)

            for url1 in soup2.find_all('div', class_='cate_m_tit'):
                category_name = url1.get_text()
                #print(category_name)


            for next_page in soup2.find_all('div', class_='item-page'):
                for next_page2 in next_page.find_all('a'):
                    page = next_page2.get('href')
                    page = CRAWLING_URL + page
                #    print(page)
            # print(soup2)
            for f in soup2.find_all('li', class_='goods_list'):
                for url in f.find_all('div', class_='thumb'):
                    for product_page in url.find_all('a'):
                        product_url = CRAWLING_URL + product_page.get('href')
                        #print(product_url) #상풀구매 페이지 url

                    for product in url.find_all('img', class_='MS_prod_img_m'):#이미지 url
                        img_url = product.get('src')
                        #print(img_url)

                for product in f.find_all('li', class_='dsc'):
                    for name in product.find_all('a'):
                        product_name = name.get_text()
                        product_name = re.sub(" \n", "", product_name)
                        # print(product_name) # 상품명

                for product_price in f.find_all('li', class_='price'):
                    price = product_price.get_text()
                     #print(price)

        # cur.execute(t, ("naning9", product_name,price, img_url,product_url, category_name))
        cur.commit()
    cur.close()
    db.close()