#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request

"""  이미지 다운로드 class  """
class crawlerImageDownload:
    def imageDownlad(self, imageUrl,name):
        image = urllib.request.urlopen(imageUrl)

        fileName = 'image/'+ name[0] + '.jpg'
        imageFile = open(fileName, 'wb')
        imageFile.write(image.read())
        imageFile.close()

if __name__ == '__main__':
    # Crawling URL
    CRAWLING_URL = 'http://www.thedaze.kr/product/detail.html?product_no=7662&cate_no=1&display_group=2'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    source_code_from_URL = urllib.request.urlopen(CRAWLING_URL)

    soup = BeautifulSoup(source_code_from_URL, 'html.parser')

    
    for title in soup.find_all(property = 'og:title'):
        prd_name = title.get('content')     # title
        print(prd_name)	

    for image in soup.find_all(property = 'og:image'):
        img_url = image.get('content')      # image
        print(img_url)	

        cid = crawlerImageDownload()
        cid.imageDownlad(img_url, img_url.split('/')[-1:])

    for price in soup.find_all(property = 'product:price:amount'):
        prd_price = price.get('content')    # price
        print(prd_price)
