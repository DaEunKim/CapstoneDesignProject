# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import re
import pymysql as mysql

# image Download Class
class crawlerImageDownload:
    def imageDownlad(self, imageUrl, name, count):
        image = urllib.request.urlopen(imageUrl)

        # image 이름 : 쇼핑몰이름_개수
        fileName = 'image/' + name[0]  + '_' + str(count) + '.jpg'
        imageFile = open(fileName, 'wb')
        imageFile.write(image.read())
        imageFile.close()


# open URL
def urlOpen(url):
    source_code_from_URL = urllib.request.urlopen(url)
    soup = BeautifulSoup(source_code_from_URL, 'html.parser')
    return soup


# 카테고리의 쪽수가 몇까지 있는지 찾는 함수
def findCategoryNum(linkLine, categoryList):
    for list_number in linkLine.find_all('ol'):
        for number in list_number.find_all('li', class_='xans-record-'):
            append_str = category_link + '&page=' + str(number.get_text())

            # None 거르기
            if append_str:
                categoryList.append(append_str)
            else:
                continue



if __name__ == '__main__':
    # MySQL DB 연결
    #db = mysql.connect(host='localhost', user='root', password='root', db='capstone', charset='utf8')
    #cursor = db.cursor()
    #t = cursor.execute("SELECT * FROM url_list")

    # Crawling URL
    CRAWLING_URL = 'http://www.mixxmix.com'

    # ShoppingMal Name
    SHOP_NAME = CRAWLING_URL.split('.')[1]

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    soup = urlOpen(CRAWLING_URL)

    # 카테고리 링크 리스트 저장할 변수
    category_link_list = []
    category_name_list = []

    # 상품의 개수 파악
    index = 1

    check = 0

    for link_line in soup.find_all('ul', class_='slideSubMenu'):

        text = link_line.get_text()
        text = text.split('\n')
        # 쇼핑몰에 해당하는 품목만 가져오기
        for i in text:
            print (i)
            if i=="가방":
                check = 1
                break

        for href_line in link_line.find_all('a'):
            category_link = CRAWLING_URL + str(href_line.get('href'))

            name_str = href_line.get_text()

            #if not re.search('-', name_str):
            #    print("-------------------------------")
            #    print(name_str)
            #    category_name_list.append(name_str)
            #else:
            #    print(name_str)
            #print (re.sub('- ', '', newstr))

            print(category_link)
            print(category_name_list)

            # 옷에 해당하는 품목까지만 가져오기
            if href_line.get_text() == "가방":
                break

            soup_category = urlOpen(category_link)

            findCategoryNum(soup_category, category_link_list)

        if check == 1:
            break



    for category in category_link_list:
        # 404 Not Found 페이지 넘어가기
        try:
            soup = urlOpen(category)
        except urllib.error.HTTPError as e:
            continue

        for product in soup.find_all('li', class_='item xans-record-'):

            url = product.find('a')

            print('=====[' + str(index) + ']==========================================')

            # 상품 판매 URL
            product_url = CRAWLING_URL + url.get('href')
            print(product_url)

            # 이미지 URL
            image_url = url.find('img').get('src')
            image_url = 'http:' + image_url
            print(image_url)

            # 상품가격
            price = url.find_next('li').find_next('span').find_next('span').get_text()
            print(price)

            # 상품명
            name = product.find('span').find_next('span').find_next('span').get_text()
            print(name)

            index += 1