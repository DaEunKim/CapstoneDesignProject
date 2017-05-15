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
    url = [['http://www.hanstyle.tv/shop/shopbrand.html?type=X&xcode=025&mcode=001&sort=&page=', 'tee_short'],
           ['http://www.hanstyle.tv/shop/shopbrand.html?type=X&xcode=025&mcode=003&sort=&page=', 'blouse_long'],
           ['http://www.hanstyle.tv/shop/shopbrand.html?type=X&xcode=026&mcode=001&sort=&page=', 'suit_skirt_long'],
           ['http://www.hanstyle.tv/shop/shopbrand.html?type=X&xcode=026&mcode=002&sort=&page=', 'cotton_trousers_long'],
           ['http://www.hanstyle.tv/shop/shopbrand.html?type=X&xcode=027&mcode=001&sort=&page=', 'onepiecedress_long'],
           ['http://www.hanstyle.tv/shop/shopbrand.html?type=X&xcode=003&mcode=001&sort=&page=', 'coat'],
           ['http://www.hanstyle.tv/shop/shopbrand.html?type=X&xcode=003&mcode=003&sort=&page=', 'cardigon'],
           ['http://www.hanstyle.tv/shop/shopbrand.html?type=X&xcode=003&mcode=002&sort=&page=', 'jacket']
           ]

    # Crawling URL
    CRAWLING_URL = 'http://www.hanstyle.tv/'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    for i in range(0, 8):
        product_clothes_label = url[i][1]
        for j in range(1,4):

            page = url[i][0] +str(j)
            print(page)
            soup = urlOpen(page)
            for tm in soup.find_all('div', class_='basic_prod_wrap normal_product'):
                for img in tm.find_all('div', class_='item_row clearWrap'):
                    for cir in img.find_all('div', class_='normal_item'):
                        tmp= cir.find('div', class_='prod_thumb')
                        sell = tmp.find('a')
                        product_shopping_url = CRAWLING_URL + str(sell.get('href'))
                        print(product_shopping_url)


                        img_url = sell.find_next('img')
                        product_shopping_img_url = CRAWLING_URL + img_url.get('src')  # image url

                        print(product_shopping_img_url)

                        name = cir.find('div', class_='spac_wrap')
                        product_name = name.find_next('div', class_='prod_name').find_next('a').get_text()
                        print(product_name)

                        price = name.find('div', class_='prod_price')
                        try:
                            price = price.find('span')
                            product_cost = price.get_text()
                        except:
                            product_cost = "-"
                        print(product_cost)

                        # curs.execute(sql, ("hanstyle", product_name, product_cost, product_shopping_img_url, product_shopping_url, product_clothes_label))


    conn.commit()
    conn.close()
