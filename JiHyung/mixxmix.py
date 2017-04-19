# -*- coding: utf-8 -*-
'''

    mixxmix
    상품 총 개수 : 3335 -> 2902
    카테고리 : ['코트', '점퍼/블루종', '자켓/가디건', '니트', '블라우스/셔츠', '스웨트셔츠/후드', '긴팔티', '반팔티', '민소매', '원피스', '스커트', '숏팬츠', '롱팬츠']

'''
from bs4 import BeautifulSoup
import urllib.request
import pymysql as mysql

# image Download Class
class crawlerImageDownload:
    def imageDownlad(self, imageUrl, name, count):
        image = urllib.request.urlopen(imageUrl)

        # image 이름 : 쇼핑몰이름_개수
        fileName = '/var/www/html/mixxmix/' + name  + '_' + str(count) + '.jpg'
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



# 카테고리 이름 한글 -> 영어
def changeCategoryName(name):
    check_name = ['코트', '점퍼/블루종', '자켓/가디건', '니트', '블라우스/셔츠', '스웨트셔츠/후드', '긴팔티', '반팔티', '민소매', '원피스', '스커트', '숏팬츠', '롱팬츠']
    change_name = ['coat', 'jacket', 'jacket', 'knit', 'blouse', 'shirt', 'tee_long', 'tee_short', 'sleeveless', 'onepiecedress', 'casual_skirt', 'jeans_short', 'jeans_long']

    for i in range(len(check_name)):
        if check_name[i] == name:
            name = change_name[i]
            break

    return name



if __name__ == '__main__':
    # MySQL DB 연결
    # db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root',
    #                    db='forstyle', charset='utf8')
    #
    # # Connection 으로 부터 Cursor 생성
    # cursor = db.cursor()
    #
    # sql = """insert into product( product_brand, product_name, product_cost, product_clothes_label, product_shopping_img_url, product_shopping_url)
    #          values (%s, %s, %s, %s, %s, %s)"""


    # Crawling URL
    CRAWLING_URL = 'http://www.mixxmix.com'

    # ShoppingMal Name
    SHOP_NAME = CRAWLING_URL.split('.')[1]

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    soup = urlOpen(CRAWLING_URL)

    # 카테고리 링크 리스트 저장할 변수
    category_link_list = []

    # 상품의 개수 파악
    index = 1

    check = 0

    link = ['http://www.mixxmix.com/mixxmix/product/list.html?cate_no=850',  # 코트
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=851',  # 점퍼/블루종
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=852',  # 자켓/가디건
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=848',  # 니트
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=933',  # 블라우스/셔츠
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=934',  # 스웨트셔츠/후드
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=1332', # 긴팔티
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=1333', # 반팔티
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=1334', # 민소매
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=842',  # 원피스
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=841',  # 스커트
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=857',  # 숏팬츠
            'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=856']  # 롱팬츠

    # 상품 링크
    for i in range(len(link)):
        soup_category = urlOpen(link[i])

        category_link = link[i]

        findCategoryNum(soup_category, category_link_list)



    for category in category_link_list:
        # 404 Not Found 페이지 넘어가기
        try:
            soup = urlOpen(category)
        except urllib.error.HTTPError as e:
            continue

        for product in soup.find_all('li', class_='item xans-record-'):

            url = product.find('a')

            print('=====[' + str(index) + ']==========================================')
            # 쇼핑몰 이름
            print(SHOP_NAME)

            # 상품 카테고리
            categoryname = soup.find('ol').get_text()
            categoryname = categoryname.strip().split('\n')
            if len(categoryname) == 3:
                categoryname = categoryname[2]
            else:
                categoryname = categoryname[3]
            category_name = changeCategoryName(categoryname)

            print(category_name)

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
            product_name = product.find('span').find_next('span').find_next('span').get_text()
            product_name = product_name.split('/')
            if len(product_name) == 1:
                name = product_name[0]
            else:
                name = product_name[1]
            print(name)

            # # image download
            # cid = crawlerImageDownload()
            # cid.imageDownlad(image_url, name, index)

            index += 1

    #         cursor.execute(sql, (SHOP_NAME, name, price, category_name, image_url, product_url))
    #
    # # Connection 닫기
    # db.commit()
    # db.close()