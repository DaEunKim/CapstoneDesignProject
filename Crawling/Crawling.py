
"""
 python3 Mac OS X
 urllib : sudo pip3 install urllib
 lxml : sudo pip3 install lxml
"""

from bs4 import BeautifulSoup
import urllib.request

# OUTPUT File
OUTPUT_FILE_NAME = 'output.txt'

# Crawling URL
CRAWLING_URL = 'http://thezam.co.kr/product/detail.html?product_no=2948&cate_no=1&display_group=2'

# Crawling Function
def get_text(CRAWLING_URL):
    # 지정된 URL을 오픈하여 requset 정보를 가져옵니다
    source_code_from_URL = urllib.request.urlopen(CRAWLING_URL)
    # lxml parsor 를 이용합니다
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    # 더 잠 사이트에서 p 태그를 가져옵니다
    for item in soup.find_all('p',align="center"):
        text = text + str(item.find_all(text=True))+' '

    return text

# Main Function
def main():
    # 파일을 쓰기 모드로 open
    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    # get_text function 호출, crawling 해서 가져온 문자열
    result_text = get_text(CRAWLING_URL)
    # 파일에 write
    open_output_file.write(result_text)
    # 파일을 닫는다
    open_output_file.close()


if __name__ == '__main__':
    main()
