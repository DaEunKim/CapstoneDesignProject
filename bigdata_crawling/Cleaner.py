"""
 Text clean up
"""

import re

# input file
INPUT_FILE_NAME = "output.txt"

# output file
OUTPUT_FILE_NAME = "output_cleand.txt"

# Cleaning Function
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z0-9]', '', text) # 영어 대소문자와 숫자를 제거
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                          '', cleaned_text)
    # 특수문자를 제거하는 코드
    return cleaned_text

# Main Function
def main():
    # 읽기 모드로 파일을 읽는다.
    read_file = open(INPUT_FILE_NAME, 'r')
    # 쓰기 모드로 파일을 읽는다.
    write_file = open(OUTPUT_FILE_NAME, 'w')
    # 파일을 읽어와 저장한다.
    text = read_file.read()
    # clean_text function 호출 후 대소문자와 숫자와 특수문자 제거된 문자열을 저장
    text = clean_text(text)
    # 파일에 쓴다.
    write_file.write(text)
    # 파일을 닫는다.
    read_file.close()
    write_file.close()

if __name__ == "__main__":
    main()
