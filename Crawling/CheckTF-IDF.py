"""
형태소 분석기 : 명사 추출 및 빈도수 체크
python [모듈이름 [텍스트파일명.txt] [결과파일명.txt]
konlpy.tag : http://konlpy.org/ko/latest/
$ pip install konlpy
$ pip install JPype1
$ pip3 install konlpy
"""

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

def main(argv):
    # 입력되는 명령어 parmeter 유효성 검사
    if len(argv) != 4:
        print('python [모듈 이름 [텍스트 파일명.txt] [단어 개수] [결과파일명.txt]')
        return
    text_file_name = argv[1]
    noun_count = int(argv[2])
    output_file_name = argv[3]
    # 파일을 읽기 모드로 오픈
    open_text_file = open(text_file_name, 'r')
    # 파일에서 읽어온다.
    text = open_text_file.read()
    # get_tags function 호출
    tags = get_tags(text, noun_count)
    # 파일을 닫는다
    open_text_file.close()
    # 파일을 쓰기 모드로 오픈
    open_output_file = open(output_file_name, 'w')
    for tag in tags:
        noun = tag['tag']
        count = tag['count']
        open_output_file.write('{} {}\n'.format(noun, count))
    # 파일을 닫는다
    open_output_file.close()

if __name__ == '__main__' :
    main(sys.argv)