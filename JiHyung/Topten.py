# -*- coding: utf-8 -*-
'''

    Topten10
    상품 총 개수 : 1170
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
        fileName = '/var/www/html/topten/' + name  + '_' + str(count) + '.jpg'
        imageFile = open(fileName, 'wb')
        imageFile.write(image.read())
        imageFile.close()


# open URL
def urlOpen(url):
    source_code_from_URL = urllib.request.urlopen(url)
    soup = BeautifulSoup(source_code_from_URL, 'html.parser')
    return soup


# 카테고리의 쪽수가 몇까지 있는지 찾는 함수
def findCategoryNum(linkLine, categoryList, ForM):
    for i in range(1, ForM):
        append_str = category_link + '&page=' + str(i)

        # None 거르기
        if append_str:
            categoryList.append(append_str)
        else:
            continue



# 카테고리 이름 한글 -> 영어
def changeCategoryName(name):
    check_name = ['코트', '캐주얼 아우터', '레인코트', '윈드브레이커',
                  '스웨터/가디건', '캐주얼셔츠', '리넨셔츠', '셔츠/블라우스', '데일리 리넨셔츠', '후드티/후드집업', '티셔츠(긴팔)', '티셔츠(반팔)', '콜라보 티셔츠', '원피스',
                  '데님', '치노', '슬랙스', '슬랙스 / 치노팬츠', '반바지', '그 외 팬츠', '스커트',
                  '래쉬가드',
                  '브리프', '브라 & SHORTS', '쿨에어', '베이직 패키지 티셔츠', '기타 언더웨어',
                  '라운지 웨어', '라운지팬츠', '액티브 웨어',
                  '가방', '신발', '벨트', '양말', '모자']
    change_name = ['coat', 'jacket', 0, 'windscreen',
                   'cardigon', 'shirt', 'shirt', 'shirt', 'shirt', 'hood', 'tee_long', 'tee_short', 'tee_short', 'onepiecedress',
                   'jeans_long', 'cotton_trousers_long', 'cotton_trousers_long', 'cotton_trousers_long', 'cotton_trousers_short', 'cotton_trousers_long', 'casual_skirt',
                   0,
                   0, 0, 0, 0, 0,
                   0, 'cotton_trousers_long', 0,
                   0, 0, 0, 0, 0]

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
    CRAWLING_URL = 'http://www.topten10.co.kr'

    # ShoppingMal Name
    SHOP_NAME = CRAWLING_URL.split('.')[1]

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    soup = urlOpen(CRAWLING_URL)

    # 상품 링크 리스트 저장할 변수
    product_link_list = []

    # 상품의 개수 파악
    index = 1

    check = 0

    link = ['http://www.topten10.co.kr/product/list.asp?cNo=1',  # Women
            'http://www.topten10.co.kr/product/list.asp?cNo=2']  # Men

    Female = 27
    Male = 36

    # 상품 링크
    for i in range(len(link)):
        soup_category = urlOpen(link[i])

        category_link = link[i]

        if i == 0:
            findCategoryNum(soup_category, product_link_list, Female)
        else:
            findCategoryNum(soup_category, product_link_list, Male)



    for find_product_list in product_link_list:
        # 404 Not Found 페이지 넘어가기
        try:
            soup = urlOpen(find_product_list)
        except urllib.error.HTTPError as e:
            continue

        for find_product in soup.find_all('ul', class_='goods_list'):

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

                category_name = cate_soup.find('ul', class_='container_12').find_next('li').find_next('li').find_next('li').find_next('li').find_next('li').get_text()
                #print(category_name)

                # 이미지 URL
                image_url = url.find('img').get('src')
                #print("img : " + image_url)

                # 상품가격
                price = url.find('div', class_='price').find_next('p', class_='sale_price').get_text()
                #print(price)

                # 상품명
                name = url.find('div', class_='g_name').find_next('p').find_next('a').get_text()
                #print(name)


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

    #             cursor.execute(sql, ("topten", name, price, category_name, image_url, product_url))
    #
    # #Connection 닫기
    # db.commit()
    # db.close()