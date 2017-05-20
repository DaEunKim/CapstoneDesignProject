# -*- coding: utf-8 -*-
'''

    8Seconds
    상품 총 개수 : 3270
    카테고리 : ['셔츠', '블라우스', '긴팔', '반팔', '풀오버', '카디건', '베스트', '아우터', '팬츠', '롱/미디', '미니', '원피스', '민소매']

'''
from bs4 import BeautifulSoup
import urllib.request
import pymysql as mysql


# open URL
def urlOpen(url):
    source_code_from_URL = urllib.request.urlopen(url)
    soup = BeautifulSoup(source_code_from_URL, 'html.parser')
    return soup



# 카테고리의 쪽수가 몇까지 있는지 찾는 함수
def findCategoryNum(linkLine, categoryList):
    page_number = 0
    for list_number in linkLine.find_all('div', class_='pagingWrap'):
        for number in list_number.find_all('a'):
            page_number += 1
            append_str = category_link + '&currentPage=' + str(page_number)

            # None 거르기
            if append_str:
                categoryList.append(append_str)
            else:
                continue



# 카테고리 이름 한글 -> 영어
def changeCategoryName(name):
    check_name = ['셔츠', '블라우스', '긴팔', '반팔', '풀오버', '카디건', '베스트', '아우터', '팬츠', '롱/미디', '미니', '원피스', '민소매']
    change_name = ['shirt_long', 'blouse_long', 'tee_long', 'tee_short', 'knit', 'cardigon', 'vest', 'jacket', 'cotton_trousers_long', 'casual_skirt_long', 'casual_skirt_short', 'onepiecedress_short', 'sleeveless']

    for i in range(len(check_name)):
        if check_name[i] == name:
            name = change_name[i]
            break

    return name



if __name__ == '__main__':
    # MySQL DB 연결
    db = mysql.connect(host='ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com', user='root', password='root',
                       db='forstyle', charset='utf8')

    # Connection 으로 부터 Cursor 생성
    cursor = db.cursor()

    sql = """insert into product( product_brand, product_name, product_cost, product_clothes_label, product_shopping_img_url, product_shopping_url)
             values (%s, %s, %s, %s, %s, %s)"""


    # Crawling URL
    CRAWLING_URL = 'http://www.ssfshop.com'

    # ShoppingMal Name
    SHOP_NAME = CRAWLING_URL.split('.')[1]

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    soup = urlOpen(CRAWLING_URL)

    # 카테고리별 상품의 페이지 링크들을 저장할 변수
    product_page_link_list = []

    # 상품의 개수 파악
    index = 1

    # 카테고리별 링크
    link = ['http://www.ssfshop.com/8Seconds/Shirts/list?dspCtgryNo=SFMA41A02A01&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_shirt
            'http://www.ssfshop.com/8Seconds/Blouses/list?dspCtgryNo=SFMA41A02A02&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_blouse
            'http://www.ssfshop.com/8Seconds/Long-Sleeve/list?dspCtgryNo=SFMA41A01A03&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_tee_long
            'http://www.ssfshop.com/8Seconds/Short-Sleeve/list?dspCtgryNo=SFMA41A01A02&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_tee_short
            'http://www.ssfshop.com/8Seconds/Pullovers/list?dspCtgryNo=SFMA41A03A01&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_knit
            'http://www.ssfshop.com/8Seconds/Cardigans/list?dspCtgryNo=SFMA41A03A02&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_cardigon
            'http://www.ssfshop.com/8Seconds/Vests/list?dspCtgryNo=SFMA41A03A03&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_vest
            'http://www.ssfshop.com/8Seconds/Outerwear/list?dspCtgryNo=SFMA41A07&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_outer
            'http://www.ssfshop.com/8Seconds/ssfshop/list?dspCtgryNo=SFMA41A04&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_pants
            'http://www.ssfshop.com/8Seconds/ssfshop/list?dspCtgryNo=SFMA41A05A01&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_skirt_long
            'http://www.ssfshop.com/8Seconds/Mini/list?dspCtgryNo=SFMA41A05A02&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_skirt_short
            'http://www.ssfshop.com/8Seconds/Dresses/list?dspCtgryNo=SFMA41A06&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Women_onepiecedress
            'http://www.ssfshop.com/8Seconds/Long-Sleeve/list?dspCtgryNo=SFMA42A01A03&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Men_tee_long
            'http://www.ssfshop.com/8Seconds/Short-Sleeve/list?dspCtgryNo=SFMA42A01A02&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Men_tee_short
            'http://www.ssfshop.com/8Seconds/Sleeveless/list?dspCtgryNo=SFMA42A01A01&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Men_sleeveless
            'http://www.ssfshop.com/8Seconds/Shirts/list?dspCtgryNo=SFMA42A02&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Men_shirt
            'http://www.ssfshop.com/8Seconds/Pullovers/list?dspCtgryNo=SFMA42A03A01&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Men_knit
            'http://www.ssfshop.com/8Seconds/Cardigans/list?dspCtgryNo=SFMA42A03A02&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Men_cardigon
            'http://www.ssfshop.com/8Seconds/Vests/list?dspCtgryNo=SFMA42A03A03&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Men_vest
            'http://www.ssfshop.com/8Seconds/Outerwear/list?dspCtgryNo=SFMA42A05&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=',  # Men_outer
            'http://www.ssfshop.com/8Seconds/ssfshop/list?dspCtgryNo=SFMA42A04&brandShopNo=BDMA07A01&brndShopId=8SBSS&etcCtgryNo=&ctgrySectCd=&keyword=&leftBrandNM=']  # Men_pants

    # 상품 링크
    for i in range(len(link)):
        soup_category = urlOpen(link[i])

        category_link = link[i]

        findCategoryNum(soup_category, product_page_link_list)



    for find_product_list in product_page_link_list:
        # 404 Not Found 페이지 넘어가기
        try:
            soup = urlOpen(find_product_list)
        except urllib.error.HTTPError as e:
            continue

        for find_product in soup.find_all('ul', class_='list'):

            for url in find_product.find_all('li'):

                print('=====[' + str(index) + ']==========================================')
                #쇼핑몰 이름
                #print(SHOP_NAME)

                # 상품 판매 URL
                product_url = CRAWLING_URL + url.find('a').get('href')
                #print("url : " + product_url)

                # 상품 카테고리
                category_name = soup.find('p', class_='listCnt').get_text()
                category_name = category_name.split(' (')
                category_name = category_name[0].strip()
                #print(category_name)

                # 이미지 URL
                image_url = url.find('span', class_='front').find('img').get('src')
                #print("img : " + image_url)


                # 상품가격
                get_price = url.find('span', class_='price').get_text().split()
                if not len(get_price) == 1:   # 가격 변동이 있을 경우
                    price = get_price[1]
                else:
                    price = get_price[0]

                if price == '품절':   # 품절일 경우, 제외하기
                    continue
                #print(price)

                # 상품명
                name = url.find('span', class_='name').get_text()
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

                cursor.execute(sql, ("8Seconds", name, price, category_name, image_url, product_url))

    #Connection 닫기
    db.commit()
    db.close()