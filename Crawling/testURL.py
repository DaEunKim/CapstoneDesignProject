import re
from bs4 import BeautifulSoup
import random
import urllib.request

# OUTPUT File
OUTPUT_FILE_NAME = 'output2.txt'

INPUT_FILE_NAME = open('url_list.txt')

for i in range(10):
    # Crawling URL
    line = INPUT_FILE_NAME.readline()
    print(line)

    CRAWLING_URL = line + '/product/detail.html?product_no=2948&cate_no=1&display_group=2'
    print(CRAWLING_URL)


def download_web_images(url):
    name = random.randrange(1, 1001)
    full_name = str(name) + ".jpg"
    urllib.request.urlretrieve(url, full_name)


download_web_images('http://www.imvely.com/web/product/big/201701/11857_shop1_209970.jpg')
