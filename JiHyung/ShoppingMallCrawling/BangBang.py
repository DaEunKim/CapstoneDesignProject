# -*- coding: utf-8 -*-
'''

    BangBang
    상품 총 개수 : 346
    카테고리 : ['아우터', '티셔츠', '셔츠', '셔츠/블라우스', '스웨터/가디건', '팬츠', '팬츠/레깅스', '스커트/원피스']

'''
from bs4 import BeautifulSoup
import urllib.request
import pymysql as mysql

# image Download Class
class crawlerImageDownload:
    def imageDownlad(self, imageUrl, name, count):
        image = urllib.request.urlopen(imageUrl)

        # image 이름 : 쇼핑몰이름_개수
        fileName = '/var/www/html/topten/' + name  + '_' + str(count) + '.jpg'
        imageFile = open(fileName, 'wb')
        imageFile.write(image.read())
        imageFile.close()


# open URL
def urlOpen(url):
    source_code_from_URL = urllib.request.urlopen(url)
    soup = BeautifulSoup(source_code_from_URL, 'html.parser')
    return soup



# 카테고리 이름 한글 -> 영어
def changeCategoryName(name):
    check_name = ['아우터', '티셔츠', '셔츠', '셔츠/블라우스', '스웨터/가디건', '팬츠', '팬츠/레깅스', '스커트/원피스']
    change_name = ['jacket', 'tee_short', 'shirt_long', 'shirt_long', 'knit', 'jeans_short', 'jeans_long', 'onepiecedress_short']

    for i in range(len(check_name)):
        if check_name[i] == name:
            name = change_name[i]
            break

    return name



if __name__ == '__main__':
    # MySQL DB 연결
    # db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root', db='forstyle', charset='utf8')
    #
    # # Connection 으로 부터 Cursor 생성
    # cursor = db.cursor()
    #
    # sql = """insert into product( product_brand, product_name, product_cost, product_clothes_label, product_shopping_img_url, product_shopping_url)
    #      values (%s, %s, %s, %s, %s, %s)"""


    # Crawling URL
    CRAWLING_URL = 'http://www.bangbangmall.com'

    # ShoppingMal Name
    SHOP_NAME = CRAWLING_URL.split('.')[1]

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    soup = urlOpen(CRAWLING_URL)

    # 상품의 개수 파악
    index = 1

    link = ['http://www.bangbangmall.com/sproduct/productList.asp?ct1=WO&ct2=OT',  # Women_outer
            'http://www.bangbangmall.com/sproduct/productList.asp?ct1=WO&ct2=TS',  # Women_tee
            'http://www.bangbangmall.com/sproduct/productList.asp?ct1=WO&ct2=CS',  # Women_shirt/blouse
            'http://www.bangbangmall.com/sproduct/productList.asp?ct1=WO&ct2=ST',  # Women_knit
            'http://www.bangbangmall.com/sproduct/productList.asp?ct1=WO&ct2=PT',  # Women_pants
            'http://www.bangbangmall.com/sproduct/productList.asp?ct1=WO&ct2=SK',  # Women_onepiece
            'http://www.bangbangmall.com/sproduct/productList.asp?ct1=MA&ct2=OT',  # Men_outer
            'http://www.bangbangmall.com/sproduct/productList.asp?ct1=MA&ct2=TS',  # Men_tee
            'http://www.bangbangmall.com/sproduct/productList.asp?ct1=MA&ct2=CS',  # Men_shirt
            'http://www.bangbangmall.com/sproduct/productList.asp?ct1=MA&ct2=ST',  # Men_knit
            'http://www.bangbangmall.com/sproduct/productList.asp?ct1=MA&ct2=PT']  # Men_pants



    for find_product_list in link:
        # 404 Not Found 페이지 넘어가기
        try:
            soup = urlOpen(find_product_list)
        except urllib.error.HTTPError as e:
            continue

        for find_product in soup.find_all('ul', class_='prodList'):

            for url in find_product.find_all('li'):

                print('=====[' + str(index) + ']==========================================')
                #쇼핑몰 이름
                #print(SHOP_NAME)

                # 상품 판매 URL
                product_url = CRAWLING_URL + url.find('a').get('href')
                #print("url : " + product_url)


                # 상품 카테고리
                # 404 Not Found 페이지 넘어가기
                try:
                    cate_soup = urlOpen(product_url)
                except urllib.error.HTTPError as e:
                    continue

                category_name = cate_soup.find('h3').get_text()
                category_name = category_name.split('> ')
                category_name = category_name[1]
                #print(category_name)

                # 이미지 URL
                image_url = CRAWLING_URL + url.find('img').get('src')
                #print("img : " + image_url)

                # 상품가격
                price = url.find('div', class_='prodName').find_next('p', class_='priceNum').get_text()
                #print(price)

                # 상품명
                name = url.find('div', class_='prodName').find_next('a').get_text()
                #print(name)


                # 카테고리 이름 한글 -> 영어로
                rename = changeCategoryName(category_name)
                if rename == 0:
                    continue
                else:
                    category_name = rename


                # 출력
                print(SHOP_NAME)
                print(category_name)
                print("url : " + product_url)
                print("img : " + image_url)
                print(price)
                print(name)


                index += 1

    #             cursor.execute(sql, ("bangbang", name, price, category_name, image_url, product_url))
    #
    # #Connection 닫기
    # db.commit()
    # db.close()