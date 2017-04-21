# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os
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
    url = [['cate=010401', 'cardigon'], # cardigon
           ['cate=010403', 'outer'], # outer
           ['cate=010404', 'jacket'], # jacket
           ['cate=010102', 'tee_long'], # tee_long
           ['cate=010104', 'mantoman'], #mantoman
           ['cate=010103', 'hood'], #hood
           ['cate=010101', 'tee_short'],
           ['cate=010105', 'knit'],
           ['cate=0102', 'blouse'],
           ['cate=020101', 'jeans_short'],
           ['cate=020102', 'jeans_long'],
           ['cate=020103','jeans_long'],
           ['cate=020104', 'cotton_trousers_long'],
           ['cate=020105', 'leggings'],
           ['cate=010301', 'onepiecedress'],
           ['cate=010302', 'casual_skirt']
           ]

    # Crawling URL
    CRAWLING_URL = 'http://www.sonyunara.com'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    for i in range(0, 16):
        product_clothes_label = url[i][1]
        for j in range(1,5):
            page = CRAWLING_URL +"/shop/list.php?page=" + str(j)+ "&" +url[i][0]
            print(page)

            soup = urlOpen(page)
            print(soup)
            for tm in soup.find_all('div', class_='product_type01'):
                img = tm.find('ul').find_next('li')
                tmp = img.find('div', class_='thumb')
                sell = tmp.find('a')

                product_shopping_url = CRAWLING_URL + str(sell.get('href'))
                print(product_shopping_url)

                img_url = tmp.find_next('img')
                product_shopping_img_url = img_url.get('src')  # image url
                print(product_shopping_img_url)

                name = tm.find('div', class_='nameTxt')
                product_name = name.find('a').get_text()
                print(product_name)

                price = tm.find('div', class_='priceBox')
                product_cost = price.find('p').find_next('span').get_text()
                print(product_cost)

                # curs.execute(sql, ("sonyunara", product_name, product_cost, product_shopping_img_url, product_clothes_label, product_shopping_url))

    conn.commit()
    conn.close()
