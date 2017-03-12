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
    CRAWLING_URL = 'http://www.littleblack.co.kr'

    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    source_code_from_URL = urllib.request.urlopen(CRAWLING_URL)

    soup = BeautifulSoup(source_code_from_URL, 'html.parser')

    #print(soup)
    
    cartegory = soup.find("div",{"class","menu_2_01"})
    
    for link in cartegory.find_all('a'):
        cart_link=link.get('href')
        cart_link= CRAWLING_URL + cart_link
        source_code_from_URL = urllib.request.urlopen(cart_link)
        soup = BeautifulSoup(source_code_from_URL, 'html.parser')

        next_page = soup.find("p",{"class","last"})
        next_page = next_page.find("a").get("href")
        temp = next_page.split('&')
        temp2 = temp[1].split('=')
        last_page = temp2[1]


        for page in range(1,int(last_page)+1):
            url = cart_link + "&page=" + str(page)
            source_code_from_URL = urllib.request.urlopen(url)
            soup = BeautifulSoup(source_code_from_URL, 'html.parser')
            for classid in soup.find_all("li",{"class","item xans-record-"}):
                img = classid.find("img")
                print(img.get("src")[2:])
                class_name = classid.find("p",{"class","name"})
                name = class_name.find_all('span')
                print(name[1].get_text())
                class_cost = classid.find("ul",{"class","xans-element- xans-product xans-product-listitem"})
                if class_cost is None:
                    print("\n\n")
                    continue
                cost = class_cost.find_all('span')
                print(cost[1].get_text())
                print("\n\n")
             
        
    """
    #img name cost http://www.littleblack.co.kr/product/list.html?cate_no=31
    for classid in soup.find_all("li",{"class","item xans-record-"}):
        img = classid.find("img")
        print(img.get("src")[2:])
        class_name = classid.find("p",{"class","name"})
        name = class_name.find_all('span')
        print(name[1].get_text())
        class_cost = classid.find("ul",{"class","xans-element- xans-product xans-product-listitem"})
        if class_cost is None:
            print("\n\n")
            continue
        cost = class_cost.find_all('span')
        print(cost[1].get_text())
        print("\n\n")
    """




