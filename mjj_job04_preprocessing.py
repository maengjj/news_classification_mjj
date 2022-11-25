import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)                 # 줄 맞춰주기
df = pd.read_csv('./crawling_data/naver_news_titles_20221124.csv')
df.category.replace('social', 'Social', inplace=True)                   # 문자 오타 replace로 바꿔주기!
print(df.head())
print(df.category.value_counts())

X = df['title']
Y = df['category']

encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)        # 카테고리를 숫자로 라벨링!
print(labeled_Y[:5])
print(encoder.classes_)     # 몇 번으로 라벨링 되어있는지 확인 할수 있다.(보통 오름차순으로 정렬을 해서 받는다)
with open('./models/label_encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)
onehot_Y = to_categorical(labeled_Y)
print(onehot_Y[:5])

okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)          # 형태소로 바꾼후 동사원형(stem=True)으로 바꿔준다.
    if i % 100 == 0 :                           # 몇개를 했는지 알기 위해 점 찍기!
        print('.', end ='')
    if i % 1000 == 0:
        print()

stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:                                    # 형태소 하나하나 길이 > 1
            if X[j][i] not in stopwords['stopword']:            # 불용어 리스트 안에 없는것
                words.append(X[j][i])
    X[j] = ' '.join(words)              # 띄어쓰기 기준으로 join(하나의 문장으로!)

token = Tokenizer()
token.fit_on_texts(X)
tokened_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1
with open('./models/news_token.pickle', 'wb') as f:
    pickle.dump(token, f)

# 문장 길이 맞추기!
max_len = 0
for i in range(len(tokened_X)):
    if max_len < len(tokened_X[i]):
        max_len = len(tokened_X[i])
print(max_len)

X_pad = pad_sequences(tokened_X, max_len)

# 테스트 데이터 나누기
X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)

# 데이터 저장히기
xy = X_train, X_test, Y_train, Y_test
np.save('./models/news_data_max_{}_wordsize_{}.npy'.format(max_len, wordsize), xy)





