#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request

if __name__ == '__main__':
    # Crawling URL
    CRAWLING_URL = 'http://www.thedaze.kr/product/detail.html?product_no=7662&cate_no=1&display_group=2'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    source_code_from_URL = urllib.request.urlopen(CRAWLING_URL)

    soup = BeautifulSoup(source_code_from_URL, 'html.parser')

    
    for title in soup.find_all(property = 'og:title'):
        print(title.get('content'))	# title

    for image in soup.find_all(property = 'og:image'):
        print(image.get('content'))	# image

    for price in soup.find_all(property = 'product:price:amount'):
        print(price.get('content'))	# price
