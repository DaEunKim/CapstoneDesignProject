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
    url = [['http://www.thedaze.kr/product/list.html?cate_no=59', 'coat'],
           ['http://www.thedaze.kr/product/list.html?cate_no=60', 'padding'],
           ['http://www.thedaze.kr/product/list.html?cate_no=56', 'jacket'],
           ['http://www.thedaze.kr/product/list.html?cate_no=55', 'cardigon'],
           ['http://www.thedaze.kr/product/list.html?cate_no=57', 'outer'],
           ['http://www.thedaze.kr/product/list.html?cate_no=120', 'tee_short'],
           ['http://www.thedaze.kr/product/list.html?cate_no=75', 'knit'],
           ['http://www.thedaze.kr/product/list.html?cate_no=73', 'mantoman'],
           ['http://www.thedaze.kr/product/list.html?cate_no=119', 'tee_long'], # 스트라이프
           ['http://www.thedaze.kr/product/list.html?cate_no=77', 'shirt_short'],
           ['http://www.thedaze.kr/product/list.html?cate_no=78', 'shirt_long'],
           ['http://www.thedaze.kr/product/list.html?cate_no=79', 'blouse_long'],
           ['http://www.thedaze.kr/product/list.html?cate_no=97', 'cotton_trousers_long'],
           ['http://www.thedaze.kr/product/list.html?cate_no=93', 'jeans_short'],
           ['http://www.thedaze.kr/product/list.html?cate_no=89', 'jeans_long'],
           ['http://www.thedaze.kr/product/list.html?cate_no=94', 'leggings'],
           ['http://www.thedaze.kr/product/list.html?cate_no=91', 'jeans_long'],
           ['http://www.thedaze.kr/product/list.html?cate_no=92', 'jeans_long'],
           ['http://www.thedaze.kr/product/list.html?cate_no=90', 'cotton_trousers_long'],
           ['http://www.thedaze.kr/product/list.html?cate_no=96', 'melbbang'],
           ['http://www.thedaze.kr/product/list.html?cate_no=100', 'casual_skirt'],
           ['http://www.thedaze.kr/product/list.html?cate_no=101', 'casual_skirt'],
           ['http://www.thedaze.kr/product/list.html?cate_no=103', 'casual_skirt'],
           ['http://www.thedaze.kr/product/list.html?cate_no=35', 'onepiecedress_long']
           ]

    # Crawling URL
    CRAWLING_URL = 'http://www.thedaze.kr'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    for i in range(0, 24):
        product_clothes_label = url[i][1]
        for j in range(1,3):

            page = url[i][0] + "&page=" +str(j)
            print(page)
            soup = urlOpen(page)
            for tm in soup.find_all('div', class_='xans-element- xans-product xans-product-listnormal'):
                for img in tm.find_all('li'):
                    tmp= img.find('div', class_='box')
                    try:
                        sell = tmp.find('a')
                        product_shopping_url = CRAWLING_URL + str(sell.get('href'))
                        print(product_shopping_url)


                        img_url = tmp.find_next('img')
                        product_shopping_img_url = img_url.get('src')  # image url
                        if (product_shopping_img_url[0:2] == '//'):
                            product_shopping_img_url = product_shopping_img_url[2:]
                        print(product_shopping_img_url)

                        name = img.find('div', class_='product_contents_info')
                        product_name = name.find('p', class_='name').find_next('a').find_next('span').get_text()
                        print(product_name)

                        price = name.find('ul', class_='xans-element- xans-product xans-product-listitem')
                        price = price.find('li').find_next('strong').find_next('span').find_next('span')
                        try:
                            product_cost = price.get_text()
                        except:
                            product_cost = "-"
                        print(product_cost)


                    except:
                        sell = "None"



                    # curs.execute(sql, ("thedaze", product_name, product_cost, product_shopping_img_url, product_shopping_url, product_clothes_label))

    conn.commit()
    conn.close()
