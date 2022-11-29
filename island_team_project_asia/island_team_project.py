# 요기요 크롤링
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import re


# url입력
driver = webdriver.Chrome('./chromedriver.exe') # 크롬드라이버 경로 설정
url = "https://www.yogiyo.co.kr/" # 사이트 입력
driver.get(url) # 사이트 오픈
driver.maximize_window() # 전체장
time.sleep(1) # 2초 지연


place = ['신림동길 14'] # , '역삼로7길 16'
category = ['1인분 주문', '프렌차이즈', '치킨', '피자/양식', '중국집', '한식', '일식/돈까스',
            '족발/보쌈', '야식', '분식', '카페/디저트']

df_restaurant = pd.DataFrame()

for i in place:
    # 검색창 선택
    xpath = '''//*[@id="search"]/div/form/input'''  # 검색창
    element = driver.find_element('xpath', xpath)
    element.clear()
    time.sleep(1)

    # 검색창 입력
    #value = input("지역을 입력하세요")
    element.send_keys(i)
    time.sleep(1)

    # 조회버튼 클릭
    search_xpath = '''//*[@id="button_search_address"]/button[2]'''
    driver.find_element('xpath', search_xpath).click()

    time.sleep(1)

    # 검색 후 콤보상자 선택
    search_xpath = '//*[@id="search"]/div/form/ul/li[3]/a'
    search = driver.find_element('xpath', search_xpath)
    search.click()
    time.sleep(1)

    # 조회버튼 클릭
    for j in range(11):
        search_xpath = '''//*[@id="category"]/ul/li[{}]/span'''.format(j+3)
        driver.find_element('xpath', search_xpath).click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # 스크롤을 가장 아래로 내린다
        pre_height = driver.execute_script("return document.body.scrollHeight") # 현재 스크롤 위치 저장
        while True :
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # 스크롤을 가장 아래로 내린다
            time.sleep(2)   # 스크롤 내려기 위한 sleep...
            cur_height = driver.execute_script("return document.body.scrollHeight")  # 현재 스크롤을 저장한다.
            if pre_height == cur_height :
                break
            pre_height = cur_height
        time.sleep(1)

        # 페이지 소스 출력
        html = driver.page_source
        html_source = BeautifulSoup(html, 'html.parser')

        # 데이터 추출
        restaurant_names = html_source.find_all("div", class_="restaurant-name ng-binding")  # 업체명
        result_lists = []

        # 데이터 배열
        for restaurant_name in restaurant_names:
            restaurant_name = restaurant_name.text
            restaurant_name = re.compile('[^가-힣A-Za-z0-9- ]').sub(' ', restaurant_name)
            restaurant_name = restaurant_name.split('-')
            result_lists.append(restaurant_name[0])  # 업체명
        time.sleep(1)

        # 데이터 프레임 만들기(업체명과 카테고리 지정)
        df_section_titles = pd.DataFrame(result_lists, columns=['restaurant_name'])
        df_section_titles['category'] = category[j]
        df_restaurant = pd.concat([df_restaurant, df_section_titles], axis='rows', ignore_index=True)


        df_restaurant.to_csv('./island_team_models/crawling_data.csv', index=False)

    time.sleep(1)


# # 페이지 소스 출력
# html = driver.page_source
# html_source = BeautifulSoup(html, 'html.parser')
#
# # 데이터 추출
# restaurant_name = html_source.find_all("div", class_ = "restaurant-name ng-binding") #업체명
# result_list = []
# result_list = df.DataFrame
#
# #데이터 배열
# for i in restaurant_name :
#     result_list.append(i.string) # 업체명
# time.sleep(1)


driver.close() # 크롬드라이버 종료

print(df_restaurant)
print(df_restaurant.category.value_counts())

print(df_restaurant.head(20))
