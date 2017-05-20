from bs4 import BeautifulSoup
import urllib.request
import pymysql as mysql
import re
import sys
from konlpy.tag import Twitter
from collections import Counter

# 명사로 분리하고 갯수를 세어 반환한다.
def get_tags(text, ntags=50):
    spliter = Twitter()
    nouns = spliter.nouns(text) # 명사로 분리한다
    count = Counter(nouns) # 명사를 카운팅한다.
    return_list = []
    for n, c in count.most_common(ntags):
        temp = {'tag': n, 'count': c}
        return_list.append(temp)
    return return_list

# 크롤링을 해온다
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

# 영어 대소문자와 특수문자를 제거한다
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z0-9]', '', text) # 영어 대소문자와 숫자를 제거
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                          '', cleaned_text)
    # 특수문자를 제거하는 코드
    return cleaned_text

# 데이터베이스에서 url_list를 읽어와 크롤링을 한다.
def db_table_read_crawling(url):
    # get_text function 호출, crawling 해서 가져온 문자열
    result_text = get_text(url)

    # clean_text function 호출 후 대소문자와 숫자와 특수문자 제거된 문자열을 저장
    text = clean_text(result_text)

    # get_tags function 호출
    tags = get_tags(text, noun_count)

    # OUTPUT File
    output_file_name = 'output.txt'

    # 파일을 쓰기 모드로 오픈
    open_output_file = open(output_file_name, 'w')

    for tag in tags:
        noun = tag['tag']
        count = tag['count']
        open_output_file.write('{} {}\n'.format(noun, count))

    ### SQL문 실행하여 TABLE에서 noun이 있는지 비교하고 있다면, count값을 가져와 ++하여 넣어야한다.

    # SQL문 실행 TABLE 삽입
    sql = "Insert INTO noun_list(noun, count) VALUES (%s, %d)"
    curs.execute(sql,(noun,count))

    # 파일을 닫는다
    open_output_file.close()

noun_count = 20

# MySQL DB 연결을 한다
db = mysql.connect(host='localhost', user='root', password='root', db='capstone', charset='utf8')

# Crawling URL
#CRAWLING_URL = 'http://thezam.co.kr/'
CRAWLING_URL = 'http://www.mixxmix.com/mixxmix/product/list.html?cate_no=838'
###########################################

# 지정된 URL을 오픈하여 requset 정보를 가져옵니다
source_code_from_URL = urllib.request.urlopen(CRAWLING_URL)

soup = BeautifulSoup(source_code_from_URL, 'html.parser')

try :
    # a 태그를 가져온다.
    for link in soup.find_all('a'):
        # 하이퍼링크 주소를 가져온다.
        href = link.get('href')
        # None 체크
        if(href != None):
            # http 로 시작하는 완전한 주소를 가져온다
            if(href[0:4] == 'http'):
                print(href)
                # Connection 으로부터 Cursor 생성
                with db.cursor() as curs:
                    # SQL문 실행 Table 삽입
                    sql = "INSERT INTO url_list(url) VALUES (%s)"
                    curs.execute(sql, (href))
                db.commit()
    with db.cursor() as curs:
        # SQL문 실행 Table 목록 확인
        sql = "SELECT * FROM url_list"
        curs.execute(sql)
        # 데이타 Fetch
        rows = curs.fetchall()
        print(rows)
finally:
    db.close()