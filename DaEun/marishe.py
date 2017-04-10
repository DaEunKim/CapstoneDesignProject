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
    # Crawling URL
    CRAWLING_URL = 'http://www.marishe.com/main.mari'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    soup = urlOpen(CRAWLING_URL)
    # 카테고리 리스트 저장할 변수
    category_list = []

    for category in soup.find_all('ol', class_='rankpop'):
        for link in category.find_all('a'):


            if(link.get('href')[0:1]=='/'):
                line = 'http://www.marishe.com' + str(link.get('href'))
            else:
                line = 'http://www.marishe.com/' + str(link.get('href'))

            #print(line)
            category_name = link.get_text()
            #print(category_name)
            # soup2 = urlOpen(line)

            # print(soup2)
            soup2 = urlOpen('http://www.marishe.com/main.mari?tag_img_map=%EC%9B%90%ED%94%BC%EC%8A%A4&tag_no=141&orderby=xbuycnt&tag_top=A&tag_no_s=596')
            for url in soup2.find_all('div', class_='contents3'):
                print(url)
                for product in url.find_all('p', class_='tit'):
                    product_name = product.get_text()
                    print(product_name)

                for product_price in url.find_all('p', class_='price'):
                    print(product_price.get_text())

                for img_url in url.find_all('p', class_='psre'):
                    img_url2 = img_url.find('a').find_next('src')
                    print(img_url2)
                        # line2 = str(img_url2.get('src'))
                        # print(line2)

                #     product_name = line2.find('a')
                #     print(product_name.get_text())
                #
                #     for number2 in list_number.find_all('li', class_='subject'):
                #         for n in number2.find_all('a'):
                #             product_name = n.get_text()
                #
                #         print(product_name)
                #
                # for number3 in list_number.find_all('li', class_='money'):
                #     product_price = number3.get_text()
                #
                #     print(product_price)
                #
