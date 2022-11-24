from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
# pages = [167, 377, 505, 71, 94, 73]         # 원 데이터의 페이지 수
pages = [101, 101, 101, 71, 94, 73]           # 데이터의 불균형은 적당히 맞춰준다. 여기서는 100페이지로 맞춰주고 100페이지가 안되면 마지막 페이지는 뺴준다.(마지막 페이지는 기사수가 20개가 안되기 때문)

options = webdriver.ChromeOptions()
# options.add_argument('headless')          # 브라우저를 안보여준다. 메모리상에 돌아가고 있긴 하다.
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver', options=options)        # 주소의 규칙성이 없어 접근이 힘들때 사용한다. 직접 클릭을 해준다.
df_title = pd.DataFrame()

for i in range(0, 6):                # category
    titles = []
    for j in range(1, 11):     # pages
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
        driver.get(url)
        time.sleep(0.2)
        for k in range(1, 5):                                                             # x_path의 규칙성을 파악하여 코드를 짜준다.
            for l in range(1, 6):
                x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l)  # 크롬-개발자도구-기사제목-우클릭-copy-Copy xpath
                try:
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ', title)
                    titles.append(title)
                except NoSuchElementException as e:                                           # 에러가 났다면 그 이유 분석
                    x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)     # 중간에 에러가 났을때 (xpath가 다르다)
                    title = driver.find_element('xpath', x_path).text
                    title = re.compile('[^가-힣 ]').sub(' ', title)
                    titles.append(title)
                except:
                    print('error', i, j, k, l)
        if j % 10 == 0:                 # 오류가 났을때 데이터가 날라갈 위험이 있기 때문에 중간중간 저장을 해준다.
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_section_title['category'] = category[i]
            df_title = pd.concat([df_title, df_section_title], ignore_index=True)
            df_title.to_csv('./crawling_data/crawling_data_{}_{}.csv'.format(category[i], j), index=False)
            titles = []

