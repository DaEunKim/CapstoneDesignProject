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


    db = pymysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root',db='spao', charset='utf8')
    cursor = db.cursor()
    t = cursor.execute("SELECT * FROM url_list") #sql문 실행

    # Crawling URL
    CRAWLING_URL = 'http://spao.elandmall.com/main/initMain.action'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    soup = urlOpen(CRAWLING_URL)

    print(soup)


    # 카테고리 리스트 저장할 변수
    category_list = []

    for category in soup.find_all('div', class_='depth2'):
        for link in category.find_all('a'):

            line = str(link.get('href')) #+CRAWLING_URL

            if(line[0:1] =='/'):
                line = CRAWLING_URL + line
                soup2 = urlOpen(line)
            else:
                soup2 = urlOpen(line)

            for list_number in soup2.find_all('ol'):
                for number in list_number.find_all('li'):
                    append_str = line + '&page=' + str(number.get_text())
                    category_list.append(append_str)



        for category in category_list:
            soup3 = urlOpen(category)

            for product in soup3.find_all('div', class_='thumb'):

                url = product.find('span')


                product_url = CRAWLING_URL + url.get('src')
                print(product_url)  # 상품 판매 URL

                with db.cursor() as curs:
                    # SQL문 실행 Table 삽입
                    sql = "INSERT INTO spao(product_url) VALUES (%s)"
                    curs.execute(sql,(href))
                db.commit()

                product_image_url = url.find('img').get('src')
                if product_image_url[0:2] == '//':
                    product_image_url = product_image_url[3:]
                print(product_image_url)  # 상품 이미지 URL



                name = product.find('span').find_next('span')
                print(name.get_text())  # 상품명

                price = product.find('span').find_next('span').find_next('span')

                if price.get_text() == '판매가':
                    if price.find_next('span').find_next('span').find_next('span').get_text() == '할인판매가':
                        price = price.find_next('span').find_next('span').find_next('span')
                    else:
                        price = price.find_next('span')

                if price.get_text()=='소비자가':
                    if price.find_next('span').find_next('span').find_next('span').find_next('span').find_next('span').get_text() == '할인판매가':
                        price = price.find_next('span').find_next('span').find_next('span').find_next('span').find_next('span').find_next('span')
                    else:
                        price = price.find_next('span').find_next('span').find_next('span')


                print(price.get_text())  # 상품 가격
    db.close()
