import request
import urllib
#from urlparse import urljoin
from scrapy.selector import Selector
import re

# 메인과 첫 수행할 웹 주소
mall_url = 'http://www.tomonari.co.kr/'
first_list_url = 'http://www.tomonari.co.kr/shop/shopbrand.html?xcode=099&type=&mcode=014&gf_ref=Yz12bk83U3o='

# 카테고리를 불러오는데 사용하는 선택자
category_list_selector = '#nav>li>ul.bber>li>a::text'
category_url_list = '#nav>li>ul.bber>li>a::attr(href)'

# 상품정보를 불러오는 데 사용하는 선택자
goods_article_selector = '.pro .pro_size_220'
goods_name_selector = '.info .pro_text_1>a::text'
goods_price_selector = '.info .pro_text>span.price::text'
goods_price_selector2 = '.info .pro_text>span.price00000::text'
goods_comment_selector = '.info .list_brand_>a::text'  # NULL OK
goods_img_src = '.info .item_ima>img.MS_prod_img_s::attr(src)'
goods_detail_url = '.info .pro_text_1>a::attr(href)'
goods_detail_html = '.de_new'

# 페이징 정보를 불러오는 데 사용하는 선택자
paging_selector = 'div.paging>.paging>li>a::text'
paging_parameter = 'page'


# URL로 페이지의 HTML을 가져온다
def fetch_page(url):
    r = request.POST(url)
    try:
        text = unicode(r.content, 'euc-kr').encode('utf-8')
    except UnicodeDecodeError as err:
        try:
            text = r.content.encode('utf-8')  # r.text
        except UnicodeDecodeError as err2:
            text = r.text
    return text


# 카테고리의 이름과 URL을 불러온다
def getCategories(url):
    html = fetch_page(url)
    sel = Selector(text=html)
    categoryList = []
    category_names = sel.css(category_list_selector).extract()
    for idx in range(0, len(category_names)):
        category_names[idx] = re.sub(r'<[^>]*?>', ' ', category_names[idx])
    category_urls = sel.css(category_url_list).extract()

    for idx in range(0, len(category_urls)):
        if category_urls[idx].startswith('/') or category_urls[idx].startswith('.'):
            category_urls[idx] = urljoin(mall_url, category_urls[idx])

        categoryList.append({
            'categoryName': category_names[idx],
            'categoryUrl': category_urls[idx]
        })

    return categoryList


# 카테고리에 속해있는 모든 상품을 가져온다
def getAllGoodsFromCategory(categoryUrl, page=1):
    html = fetch_page(categoryUrl + '&' + paging_parameter + '=' + str(page))
    sel = Selector(text=html)
    goods_list = sel.css(goods_article_selector).extract()

    paging = sel.css(paging_selector).extract()
    max_page_cnt = -1

    while True:
        try:
            max_page = int(paging[max_page_cnt])
            break
        except UnicodeEncodeError:
            max_page_cnt = max_page_cnt - 1

    if len(paging) != 0 and max_page > page:
        nextPageItem = getAllGoodsFromCategory(categoryUrl, page + 1)
        goods_list += nextPageItem
    return goods_list


# 상품 HTML에서 상품 이름과 가격, 코멘트, 상세정보 URL을 추출한다.
def extractGoodsInfo(articles=[], categoryName=''):
    print(categoryName)
    goodsList = []
    for article in articles:
        sel = Selector(text=article)
        try:
            name = re.sub(r'<[^>]*?>', ' ', sel.css(goods_name_selector).extract_first())
        except TypeError as err:
            print(sel.css(goods_name_selector).extract_first())
            continue
        try:
            price = int("".join(re.findall(r"(\d+)", sel.css(goods_price_selector).extract_first())))  # 숫자만 추출하여 정수로 변환
        except TypeError as err:
            price = int("".join(re.findall(r"(\d+)", sel.css(goods_price_selector2).extract_first())))
        comment = sel.css(goods_comment_selector).extract_first()
        detail = sel.css(goods_detail_url).extract_first()
        if detail.startswith('/') or detail.startswith('.'):
            detail = urljoin(mall_url, detail)
        img = sel.css(goods_img_src).extract_first()
        if img.startswith('/') or img.startswith('.'):
            img = urljoin(mall_url, img)
        detail_html = Selector(text=fetch_page(detail)).css(goods_detail_html).extract_first()
        goodsList.append({
            'name': name,
            'price': price,
            'comment': comment,
            # 'detail_url': detail,
            'category': categoryName,
            'image': img,
            # 'detail_html': detail_html
        })
    return goodsList


# 빠른 수집을 위한 동시성 선언
import sys

if 'threading' in sys.modules:
    del sys.modules['threading']

from gevent import monkey

monkey.patch_all()

from gevent.pool import Pool

# 카테고리별로 돌며 전체상품 추출
categories = getCategories(first_list_url)
pool = Pool(20)
goods = pool.map(lambda category:
                 extractGoodsInfo(getAllGoodsFromCategory(category['categoryUrl']), category['categoryName']),
                 categories[4:5])

# 수집한 상품명 출력
# x= 한 카테고리 / y = 한 상품
for x in goods:
    for y in x:
        print
        y['name']

# mysql(mariadb)에 입력.
"""
import mysql.connector
from mysql.connector import errorcode

try:
    config = {
            'user': 'db_user',
            'password': 'db_pw',
            'host': 'host_url',
            'database': 'db_name',
            'charset':'utf8'
    }
    cnx = mysql.connector.connect(**config)

    cursor = cnx.cursor()
    cursor.execute("SET NAMES utf8mb4;") #or utf8 or any other charset you want to handle

    cursor.execute("SET CHARACTER SET utf8mb4;") #same as above

    cursor.execute("SET character_set_connection=utf8mb4;") #same as above

    query = ('INSERT INTO goods(gname, price, gcomment, url, content_html, category, img_src) '
             'VALUES(%(name)s, %(price)s, %(comment)s, %(detail_url)s, %(detail_html)s, %(category)s, %(image)s )')

    count = 0
    for x in goods:
        for y in x:
            try:
                cursor.execute(query, y)
                cnx.commit()
            except mysql.connector.Error as err:
                print(err)

    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exists")
    else:
        print(err)
else:
    cnx.close()
"""
