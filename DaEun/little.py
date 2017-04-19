# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import re
import pymysql

"""  이미지 다운로드 class  """


class crawlerImageDownload:
    def imageDownlad(self, imageUrl, name):
        image = urllib.request.urlopen(imageUrl)

        fileName = 'image/' + name[0] + '.jpg'
        imageFile = open(fileName, 'wb')
        imageFile.write(image.read())
        imageFile.close()


if __name__ == '__main__':
    # MySQL Connection 연결
    conn = pymysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root',
                           db='forstyle', charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()

    sql = """insert into product(product_brand,product_name,product_cost,product_clothes_label,product_shopping_img_url,product_shopping_url)
         values (%s, %s, %s, %s, %s, %s)"""

    url = [["http://www.naning9.com/shop/list.php?cate=0S01", "SLEEVELESS"],
           ["http://www.naning9.com/shop/list.php?cate=0S02", "TEE"],
           ["http://www.naning9.com/shop/list.php?cate=0S04", "SHIRT&BLOUSE"],
           ["http://www.naning9.com/shop/list.php?cate=0S05", "KINT"],
           ["http://www.naning9.com/shop/list.php?cate=0S06", "HOOD"],
           ["http://www.naning9.com/shop/list.php?cate=0D", "TRAINING SET"],
           ["http://www.naning9.com/shop/list.php?cate=0T01", "JUMPER"],
           ["http://www.naning9.com/shop/list.php?cate=0T01", "JACKET"],
           ["http://www.naning9.com/shop/list.php?cate=0T01", "COAT"],
           ["http://www.naning9.com/shop/list.php?cate=0T01", "VEST"],
           ["http://www.naning9.com/shop/list.php?cate=0T01", "CARDIGAN"],
           ["http://www.naning9.com/shop/list.php?cate=0T01", "ZIPUP"],
           ["http://www.naning9.com/shop/list.php?cate=0V01", "JEANS"],
           ["http://www.naning9.com/shop/list.php?cate=0V01", "SHORT"],
           ["http://www.naning9.com/shop/list.php?cate=0V01", "LONG"],
           ["http://www.naning9.com/shop/list.php?cate=0V01", "LEGGINGS"],
           ["http://www.naning9.com/shop/list.php?cate=0U01", "SKIRT"],
           ["http://www.naning9.com/shop/list.php?cate=0U01", "DRESS"],
           ["http://www.naning9.com/shop/list.php?cate=0U01", "Flower dress"]]

    # Crawling URL
    CRAWLING_URL = 'http://www.naning9.com'
    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다

    for i in range(0, 19):
        source_code_from_URL = urllib.request.urlopen(url[i][0])
        soup = BeautifulSoup(source_code_from_URL, 'html.parser')
        product_clothes_label = url[i][1]

        temp = soup.find("div", {"class", "item-page"})
        temp = temp.find_all("a")
        page_num = int(temp[-2].get_text())

        for j in range(1, page_num + 1):
            source_url = url[i][0] + "&page=2"
            source_code_from_URL = urllib.request.urlopen(source_url)
            soup = BeautifulSoup(source_code_from_URL, 'html.parser')
            for goods in soup.find_all("div", {"class", "goods_item"}):
                product_shopping_img_url = goods.find("img", {"class", "MS_prod_img_m"}).get("src")
                print(product_shopping_img_url)

                product_shopping_url = CRAWLING_URL + goods.find("a").get("href")
                print(product_shopping_url)
                product_cost = goods.find("li", {"class", "price"}).get_text()
                product_cost = re.sub("\s", "", str(product_cost))
                print(product_cost)
                # product_name = goods.find("br").get_text()
                product_name = goods.find("li", {"class", "dsc"}).get_text()
                product_name = re.sub("\s", "", str(product_name))
                print(product_name)

                curs.execute(sql, (
                "naning9", product_name, product_cost, product_clothes_label, product_shopping_img_url,
                product_shopping_url))

    # Connection 닫기
    conn.commit()
    conn.close()
