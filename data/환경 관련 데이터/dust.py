# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:02:09 2025

@author: Admin
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

### 데이터 수집 ####
## 미세먼지 데이터 ##
dust = pd.read_excel('./data/환경 관련 데이터/dust.xlsx')
dust.shape # (744, 7)

dust.info()

### 데이터 가공 ###
# 컬럼의 이름을 영문으로 변경
dust.rename(columns = {'날짜' :'date', '아황산가스':'so2',
                       '일산화탄소': 'co', '오존' : 'o3',
                       '이산화질소':'no2'}, inplace=True)

# 날짜 데이터에서 년도-월-일만 추출
# '2021-01-01 01' => '2021-01-01'
dust['date']=dust['date'].str[:11]

#날짜 컬럼의 자료형을 날짜형으로 변환,
# date       744 non-null    object => datetime54[ns]
dust['date'] = pd.to_datetime(dust['date'])


# 날짜 컬럼에서 년도, 월, 일을 추출하여 각각 새로운 컬럼으로 추가
# 후; 여러 년도로 분석 시 필요할 수도 있기 때문에
dust['year'] = dust['date'].dt.year
dust['month'] = dust['date'].dt.month
dust['day'] = dust['date'].dt.day

# 새롭게 추가된 컬럼 순서 재정렬
dust = dust[['date', 'year', 'month', 'day', 'so2', 'co', 'o3', 'no2', 'PM10', 'PM2.5']]

### 데이터 전처리 ###
# 각 컬럼별(변수) 결측치(null) 수 확인
dust.isnull().sum()
'''
date      0
year      0
month     0
day       0
so2       4
co        4
o3        4
no2       4
PM10     19
PM2.5     5
dtype: int64
'''

# 시계열분석이므로 null값을 이전 시간의 값을 기준으로 채워줌
# 결측값을 옆 뱡향 혹은 뒷 방향으로 채우기
dust=dust.fillna(method='pad')

# 이전값이 없는 경우 혼자 Nan은 20으로 채워줌
dust.fillna(20, inplace=True)

# dust['month'] = dust['month'].astype(int)

#### 날씨 데이터 ####
file_path = './data/환경 관련 데이터/weather.xlsx'
weather = pd.read_excel(file_path)

weather.info()

### 데이터 가공 ###
# 분석에 필요 없는 컬럼 제거 
weather.drop('지점', axis = 1, inplace=True)
weather.drop('지점명', axis = 1, inplace=True)

# 특수 기호가 포함된 컬럼명을 변경
weather.columns=['date', 'temp', 'wind', 'rain', 'humid']

# 미세먼지데이터와 동일한 타입을 위해
# 컬럼 일부 데이터(시간) 제거한 후,
weather['date'] = pd.to_datetime(weather['date']).dt.date

# 데이터 타입 변경
weather['date'] = weather['date'].astype('datetime64[ns]')

# 결측값 확인
weather.isnull().sum()

# 강수량 데이터 확인
weather['rain'].value_counts()
'''
기상청에서는 0.1 단위로 강수량을 측정,
0.1 이하는 비가 내리면 0으로 표시
따라서 좀 더 세부적인 값을 측정하기 위해
'''
# 강수량이 0인 값을 0.01로 변환
weather['rain'] = weather['rain'].replace([0], 0.01)
weather['rain'].value_counts()

### 데이터 병합 ###
# 미세먼지 데이터와 날씨 데이터를 병합하기 위해
# 두 데이터 프레임의 차원을 파악
dust.shape # (744, 10)
weather.shape #(743, 5)

# 미세먼지 데이터와 날씨 데이터의 
# 공통적인 내용이 아닌 행을 제거
dust.drop(index=743, inplace=True) # (743, 10)

# dust와 weather이 동일하게 가진 date를 기준으로 병합해서 df 프레임 생성
df = pd.merge(dust, weather, on='date')

### 데이터 분석 및 시각화 ###
# 미세먼지 데이터와 날씨 데이터의 모든 요소별 상관관계 확인
df.corr() # => 상관계수
'''
상관계수 

양의 상관관계 : 정비례
0.7 ~ 1.0 : 강한 양의 상관관계
0.3 ~ 0.7 : 뚜렷한 양의 상관관계
0.1 ~ 0.3 : 약한 양의 상관관계

관련 없음 : -0.1 ~ 0.1

음의 상관관계 : 반비례
-0.7 ~ -1.0 : 강한 음의 상관관계
-0.3 ~ -0.7 : 뚜렷한 음의 상관관계
-0.1 ~ -0.3 : 약한 음의 상관관계
'''
corr = df.corr()
corr['PM10'].sort_values(ascending=False)
'''
PM10     1.000000
PM2.5    0.825433
co       0.529720
no2      0.420554
humid    0.216753
temp     0.175430
so2      0.160874
rain     0.026272
date     0.016124
day      0.016124
wind    -0.108474
o3      -0.348229
year          NaN
month         NaN
Name: PM10, dtype: float64
'''

# 히스토그램으로 시각화
df.hist(bins=50, figsize=(20, 15))
plt.show()

# 막대 그래프로 시각화 : 일별 미세먼지 평균현황
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(15, 10))
sns.barplot(x='day', y='PM10', data= df, palette='Set1' )
plt.xticks(rotation=0)
plt.show()

# 히트맵 그래프로 시각화 : 각 변수간의 상관관계
plt.figure(figsize=(15, 12))
sns.heatmap(data= corr, annot=True, fmt='.2f', cmap='hot')
plt.show()

'''
PM10, PM2.5, no2,co : 이들은 모두 대기 오염물질이기에 관련성
o3와 wind : 바람과 오존이 약한 관계성
'''

# 산점도 그래프로 시각화1 : 온도와 미세먼지 상관관계
plt.figure(figsize=(15,10))
x=df['temp']
y=df['PM10']
plt.plot(x, y, marker='o', linestyle='none', alpha=0.5)
plt.title('temp - pm10')
plt.xlabel('temp')
plt.ylabel('pm10')

plt.show()

# 온도와 미세먼지는 상관관계가 없음을 확인

# 산점도 그래프로 시각화2: # 미세먼지와 초미세먼지의 상관관계
plt.figure(figsize=(15,10))
x=df['PM10']
y=df['PM2.5']

plt.plot(x, y, marker='o', linestyle='none', color = 'red', alpha=0.5)
plt.title('pm10- pm2.5')
plt.xlabel('pm10')
plt.ylabel('pm2.5')
plt.show()

# => 미세먼지와 초미세먼지가 선형성을 갖는 것이 확인됨.
# => 따라서 상관관계가 상당히 높다
'''
미세먼지와 초미세먼지는 강한 관계성
미세먼지 중 대기오염과 관련된 변수들은 관련성이 있다.
일산화탄소와 이산화 질소는 강한 관계성
오존과 바람은 약한 관계성
기온과 미세먼지는 무관
'''
































