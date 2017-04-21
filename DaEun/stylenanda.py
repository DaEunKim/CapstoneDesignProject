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
    url = [['http://www.stylenanda.com/product/list03.html?cate_no=117', 'blouse'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=492', 'tee_long'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=581', 'shirt_long'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=118', 'knit'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=580', 'mantoman'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=116', 'tee_short'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=505', 'sleeveless'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=121', 'cardigon'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=120', 'jacket'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=539', 'windscreen'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=582', 'riderjacket'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=124', 'coat'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=123', 'vest'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=583', 'padding'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=538', 'mustangjacket'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=132', 'cotton_trousers_long'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=129', 'jeans_long'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=127', 'cotton_trousers_short'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=251', 'leggings'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=570', 'casual_skirt'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=571', 'casual_skirt'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=569', 'casual_skirt'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=573', 'onepiecedress_long'],
           ['http://www.stylenanda.com/product/list03.html?cate_no=572', 'onepiecedress_short']
           ]

    # Crawling URL
    CRAWLING_URL = 'http://www.stylenanda.com'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    for i in range(0, 24):
        product_clothes_label = url[i][1]
        for j in range(1,3):

            page = url[i][0] + "&page=" +str(j)
            print(page)
            soup = urlOpen(page)
            for tm in soup.find_all('div', class_='xans-element- xans-product xans-product-listnormal ec-base-product'):
                for img in tm.find_all('li'):
                    tmp= img.find('div', class_='box')
                    sell = tmp.find('a')
                    product_shopping_url = CRAWLING_URL + str(sell.get('href'))
                    print(product_shopping_url)


                    img_url = tmp.find_next('img')
                    product_shopping_img_url = img_url.get('src')  # image url
                    if(product_shopping_img_url[0:2]=='//'):
                        product_shopping_img_url = product_shopping_img_url[2:]
                    print(product_shopping_img_url)

                    name = img.find('div', class_='information2')
                    product_name = name.find('p', class_='name').find_next('span').get_text()
                    print(product_name)

                    price = name.find('p', class_='price')
                    try:
                        product_cost = price.get_text()
                    except:
                        product_cost ="-"
                    print(product_cost)

                    # curs.execute(sql, ("stylenanda", product_name, product_cost, product_shopping_img_url, product_shopping_url, product_clothes_label))

    conn.commit()
    conn.close()
