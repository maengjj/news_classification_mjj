from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'    # 정치
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101'    # 경제
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102'    # 사회


# 페이지 검사 > Network탭 > 아무거나 하나 선택 > Response Headers > user-agent 복붙
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}     # 딕셔너리 형태
df_titles = pd.DataFrame()
for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)     # 네이버 뉴스 섹션 주소 규칙
    resp = requests.get(url, headers=headers)        # requests 패지지 안의 get함수는 url 주소로 가서 웹서버에게 페이지를 보여달라고 요청한다. html코드로 출력해준다. 네이버에서는 이 기능을 막아놓았다. resp = response(응답)
    # print(list(resp))
    soup = BeautifulSoup(resp.text, 'html.parser')      # html 문서 형태로 바꿔준다.
    # print(soup)
    title_tags = soup.select('.cluster_text_headline')          # 뉴스 기사 제목 뽑아온다.
    titles = []
    for title_tag in title_tags:
        titles.append(title_tag.text)                           # 제목들만 골라서 뽑아 리스트 안에 넣는다.
    df_section_titles = pd.DataFrame(titles, columns=['titles'])                    # 뉴스제목과 카테고리 지정해주는 데이터프레임 만들기
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
print(df_titles)
print(df_titles.category.value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)