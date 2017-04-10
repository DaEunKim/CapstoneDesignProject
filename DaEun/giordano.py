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
    CRAWLING_URL = 'http://www.giordano.co.kr'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    soup = urlOpen(CRAWLING_URL)

    # 카테고리 리스트 저장할 변수
    category_list = []

    for category in soup.find_all('ul', class_='depth'):
        for link in category.find_all('a'):
            line = CRAWLING_URL + str(link.get('href'))
            print(line)

            category_name = link.get_text()
            print(category_name)

            soup2 = urlOpen(line)


            for list_number in soup2.find_all('ul', class_='product_list01'):
                for number in list_number.find_all('li', class_='img'):
                    for n in number.find_all('img'):
                        line2 = str(n.get('src'))
                        print(line2)

                        product_name = line2.find('a')
                        print(product_name.get_text())

                for number2 in list_number.find_all('li', class_='subject'):
                    for n in number2.find_all('a'):
                        product_name = n.get_text()

                        print(product_name)

                for number3 in list_number.find_all('li', class_='money'):
                    product_price = number3.get_text()

                    print(product_price)

                    #
                    # for category in soup.find_all('ul', class_='gnb'):
                    #     for link in category.find_all('a'):
                    #         line = CRAWLING_URL + str(link.get('href'))
                    #
                    #         soup2 = urlOpen(line)
                    #
                    #         for list_number in soup2.find_all('ol'):
                    #             for number in list_number.find_all('li'):
                    #                 append_str = line + '&page=' + str(number.get_text())
                    #                 category_list.append(append_str)
                    #
                    # for category in soup.find_all('ul', class_='gnb2'):
                    #     for link in category.find_all('a'):
                    #         line = CRAWLING_URL + str(link.get('href'))
                    #
                    #         soup2 = urlOpen(line)
                    #
                    #         for list_number in soup2.find_all('ol'):
                    #             for number in list_number.find_all('li'):
                    #                 append_str = line + '&page=' + str(number.get_text())
                    #                 category_list.append(append_str)
                    #
                    # # print(category_list[:])
                    # for category in category_list:
                    #
                    #     soup3 = urlOpen(category)
                    #
                    #     for product in soup3.find_all('li', class_='item xans-record-'):
                    #
                    #         url = product.find('a')
                    #
                    #         product_url = CRAWLING_URL + url.get('href')
                    #         print(product_url)  # 상품 판매 URL
                    #
                    #         product_image_url = url.find('img').get('src')
                    #         if product_image_url[0] == '/':
                    #             product_image_url = product_image_url[2:]
                    #         print(product_image_url)  # 상품 이미지 URL
                    #
                    #         name = url.find_next('a')
                    #         print(name.get_text())  # 상품 가격
                    #
                    #         price = product.find('span').find_next('span').find_next('span')
                    #         if price.get_text() == '판매가':
                    #             price = price.find_next('span')
                    #         print(price.get_text())  # 상품명
