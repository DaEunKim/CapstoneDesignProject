#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request

class crawlerImageDownload:
    def imageDownlad(self, imageUrl,count):
        image = urllib.request.urlopen(imageUrl)

        fileName = 'image/image_'+ str(count) + '.jpg'
        imageFile = open(fileName, 'wb')
        imageFile.write(image.read())
        imageFile.close()

if __name__ == '__main__':
    # Crawling URL
    #CRAWLING_URL = 'http://thezam.co.kr'
    CRAWLING_URL = 'http://www.michyeora.com'
    #########################################

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    source_code_from_URL = urllib.request.urlopen(CRAWLING_URL)

    soup = BeautifulSoup(source_code_from_URL, 'html.parser')

    index = 0

    for item in soup.find_all('img'):
        src = str(item['src'])

        # 제외할 단어
        if ("icon" in src) or ("upload" in src) or ("discount" in src) or ("event" in src):
            continue;
        # 포함할 단어
        elif ("shopimage" in src) or ("shop1" in src) or ("product" in src) or ("goods" in src):
            if (src[0:11] == 'about:blank'):
                continue
            if (src[0:5] == 'https'):
                continue
            elif (src[0:7] == 'http://'):
                src = src
            elif (src[0:2] == '//'):
                src = 'http:' + src
            elif (src[0:1] == '/'):
                src = 'http://www.michyeora.com/' + src #########################
            print(str(index) + ')\t' + src)
            cid = crawlerImageDownload()
            cid.imageDownlad(src, index)
            index += 1