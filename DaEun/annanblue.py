# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os
import urllib.request
import pymysql

def urlOpen(url):
    source_code_from_URL = urllib.request.urlopen(url)
    soup = BeautifulSoup(source_code_from_URL, 'html.parser')
    return soup


if __name__ == '__main__':

    conn = pymysql.connect(host = 'ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root',
                           password='root', db='forstyle', charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()

    sql = """insert into product(product_brand, product_name, product_cost, product_shopping_img_url, product_shopping_url, product_clothes_label) values (%s, %s, %s, %s, %s, %s)"""

    # Crawling URL
    url = [['http://www.annanblue.com/shop/shopbrand.html?type=O&xcode=001&sort=&page=', 'coat'],
           ['http://www.annanblue.com/shop/shopbrand.html?type=X&xcode=025&mcode=003&sort=&page=', 'cardigon'],
           ['http://www.annanblue.com/shop/shopbrand.html?type=X&xcode=025&mcode=002&sort=&page=', 'knit'],
           ['http://www.annanblue.com/shop/shopbrand.html?type=X&xcode=026&mcode=001&sort=&page=', 'shirt_long'],
           ['http://www.annanblue.com/shop/shopbrand.html?type=X&xcode=019&mcode=001&sort=&page=', 'tee_short'],
           ['http://www.annanblue.com/shop/shopbrand.html?type=X&xcode=019&mcode=002&sort=&page=', 'sleeveless'],
           ['http://www.annanblue.com/shop/shopbrand.html?type=X&xcode=024&sort=&page=', 'cotton_trousers_long'],
           ['http://www.annanblue.com/shop/shopbrand.html?type=O&xcode=029&sort=&page=', 'suit_skirt_long'],
           ['http://www.annanblue.com/shop/shopbrand.html?type=O&xcode=004&sort=&page=', 'onepiecedress_long'],
           ['http://www.annanblue.com/shop/shopbrand.html?type=X&xcode=021&sort=&page=', 'jeans_long']
           ]

    # Crawling URL
    CRAWLING_URL = 'http://www.annanblue.com/'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    for i in range(0, 10):
        product_clothes_label = url[i][1]
        for j in range(1,2):

            page = url[i][0] +str(j)
            print(page)
            soup = urlOpen(page)
            for tm in soup.find_all('div', class_='prd_list_style'):
                for img in tm.find_all('li'):
                    tmp= img.find('div', class_='box')
                    try:
                        sell = tmp.find('a')
                        product_shopping_url = CRAWLING_URL + str(sell.get('href'))
                        print(product_shopping_url)


                        img_url = tmp.find_next('img')
                        product_shopping_img_url = CRAWLING_URL + img_url.get('src')  # image url

                        print(product_shopping_img_url)

                        name = tmp.find('div', class_='name')
                        product_name = name.get_text()
                        print(product_name)

                        price = tmp.find('ul')
                        price = price.find('li', class_='prd-price')
                        try:
                            product_cost = price.get_text()
                        except:
                            product_cost = "-"
                        print(product_cost)

                        # curs.execute(sql, ("annanblue", product_name, product_cost, product_shopping_img_url, product_shopping_url, product_clothes_label))

                    except:
                        sell = "None"





    conn.commit()
    conn.close()
