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
    url = [['http://www.zemmaworld.com/product/list.html?cate_no=158', 'coat'], #코트
           ['http://www.zemmaworld.com/product/list.html?cate_no=159','jacket'], #자켓
           ['http://www.zemmaworld.com/product/list.html?cate_no=161', 'padding'], #패딩
           ['http://www.zemmaworld.com/product/list.html?cate_no=164', 'tee'], #티
           ['http://www.zemmaworld.com/product/list.html?cate_no=397', 'mantoman'], # 맨투맨
           ['http://www.zemmaworld.com/product/list.html?cate_no=397', 'hood'], # 후드
           ['http://www.zemmaworld.com/product/list.html?cate_no=254', 'knit'], #니트
           ['http://www.zemmaworld.com/product/list.html?cate_no=169','blouse'], #블라우스
           ['http://www.zemmaworld.com/product/list.html?cate_no=177', 'onepiecedress'], #원피스
           ['http://www.zemmaworld.com/product/list.html?cate_no=91', 'jeans'], # 청바지
           ['http://www.zemmaworld.com/product/list.html?cate_no=172', 'casual_skirt'], #스커트
           ['http://www.zemmaworld.com/product/list.html?cate_no=406','casual_skirt'], #스커트
           ['http://www.zemmaworld.com/product/list.html?cate_no=168', 'shirt'] #셔츠
           ]

    # Crawling URL
    CRAWLING_URL = 'http://www.zemmaworld.com'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    for i in range(0, 13):
        product_clothes_label = url[i][1]
        for j in range(1,7):
            page = url[i][0] +"&page=" + str(j)
            print(page)
            soup = urlOpen(page)
            for tm in soup.find_all('li', class_='item xans-record-'):
                img = tm.find('div', class_='thumbnail')
                sell = img.find('a')

                product_shopping_url = CRAWLING_URL + str(sell.get('href'))
                print(product_shopping_url)

                img_url = img.find_next('img')
                product_shopping_img_url = img_url.get('src')  # image url
                if (product_shopping_img_url[0:1] == '/'):
                    product_shopping_img_url = product_shopping_img_url[2:]
                    print(product_shopping_img_url)

                name = tm.find('p', class_='name')
                product_name = name.find_next('span').get_text()
                print(product_name)

                price = tm.find('ul', class_='xans-element- xans-product xans-product-listitem')
                product_cost = price.find('li').find_next('span').find_next('span').get_text()
                print(product_cost)

                # curs.execute(sql, ("zemmaworld", product_name, product_cost, product_shopping_img_url, product_shopping_url, product_clothes_label))

    conn.commit()
    conn.close()
