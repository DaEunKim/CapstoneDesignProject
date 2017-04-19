# -*- coding: utf-8 -*-
'''

    Topten10
    상품 총 개수 : 2175
    카테고리 : 여성 [ALL, 신상품, ACTIVE WEAR, 자켓/코트/점퍼, 언더웨어, 온에어 발열내의, 후드/집업, 니트/가디건/스웨터, 맨투맨, 블라우스/셔츠, 라운드 티셔츠, 민소매 티셔츠, 원피스/스커트, 데님, 팬츠/레깅스, 라운지웨어, 코튼스판 캐미솔, COOL Air]
              남성 [ALL, 신상품, ACTIVE WEAR, 자켓/코트/점퍼, 언더웨어, 온에어 발열내의, 후드/집업, 맨투맨, 니트/가디건/스웨터, 라운드 티셔츠, 셔츠, 폴로 티셔츠, 데님, 팬츠, 라운지웨어, COOL Air]

'''
from bs4 import BeautifulSoup
import urllib.request
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
    for list_number in linkLine.find_all('div', class_='paging'):
        for number in list_number.find_all('a'):

            if(number.get_text() == "다음"):
                continue

            append_str = category_link + '&page=' + str(number.get_text())

            # None 거르기
            if append_str:
                categoryList.append(append_str)
            else:
                continue



if __name__ == '__main__':
    # MySQL DB 연결
    db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root', db='forstyle', charset='utf8')

    # Connection 으로 부터 Cursor 생성
    cursor = db.cursor()

    sql = """insert into demo( product_brand, product_name, product_cost, product_clothes_label, product_shopping_img_url, product_shopping_url)
         values (%s, %s, %s, %s, %s, %s)"""


    # Crawling URL
    CRAWLING_URL = 'http://www.topten10.co.kr'

    # ShoppingMal Name
    SHOP_NAME = CRAWLING_URL.split('.')[1]

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    soup = urlOpen(CRAWLING_URL)

    # 카테고리 링크 리스트 저장할 변수
    category_link_list = []

    # 상품의 개수 파악
    index = 1

    check = 0

    for link_line in soup.find_all('nav', class_='d_nav nav150701'):

        text = link_line.get_text()
        text = text.split('\n')

        # 쇼핑몰에 해당하는 품목만 가져오기
        for i in text:
            if i=="KIDS":
                check = 1
                break

        for href_line in link_line.find_all('a'):
            category_link = CRAWLING_URL + str(href_line.get('href'))

            name_str = href_line.get_text()

            # 옷에 해당하는 품목까지만 가져오기
            if href_line.get_text() == "KIDS":
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

        for product in soup.find_all('ul', class_='product_list'):

            for url in product.find_all('li'):

                print('=====[' + str(index) + ']==========================================')
                #print('=====================================================================')
                #쇼핑몰 이름
                print(SHOP_NAME)

                #상품 카테고리
                category_name = soup.find('div', class_='all fl').get_text()
                category_name = category_name.strip().split('(')[0]
                print(category_name)

                # 상품 판매 URL
                product_url = CRAWLING_URL + url.find('a').get('href')
                print("url : " + product_url)

                # 이미지 URL
                image_url = url.find('img').get('src')
                print("img : " + image_url)

                # 상품가격
                price = url.find('dl').find_next('dd').find_next('p').get_text()
                if len(price) > 10:
                    price = price.split(' ')
                    price = price[1]
                print(price)

                # 상품명
                name = url.find('dl').find_next('dt').get_text()
                name = name.strip()
                print(name)

                index += 1

                cursor.execute(sql, (SHOP_NAME, name, price, category_name, image_url, product_url))

    #Connection 닫기
    db.commit()
    db.close()