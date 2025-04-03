# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 09:11:10 2025

@author: Admin
수집 데이터 전처리
danawa_crawling_result.xlsx
2. preprocessing
"""
import pandas as pd
data = pd.read_excel('./data/danawa_crawling_result.xlsx')
data.info()

# 1. 상품명 데이터를 회사명과 상품명으로 분리
company_list = []
product_list = []

data['상품명'][:10]
title = 'LG전자 코드제로 A9 A978'
info = title.split(' ')
# = >['LG전자', '코드제로', 'A9', 'A978']

info = title.split(' ', 1)
# => ['LG전자', '코드제로 AG A978']
#-----------------------------------------
company_list = []
product_list = []

for title in data['상품명']:
    title_info = title.split(' ',1)
    company_name = title_info[0]
    product_name = title_info[1]
    
    company_list.append(company_name)
    company_list.append(product_name)

# 2. 스펙 목록 데이터를 분석에 필요한 요소만 추출
## 카테고리, 사용기간, 흡입력
# 테스트 코드
data['스펙 목록'][0]
'''
'핸디/스틱청소기 / 핸디+스틱형 / 무선형 / 전압: 25.2V / 헤파필터 / H12급 / 5단계여과 / 흡입력: 140AW / 
흡입력: 22000Pa / 먼지통용량: 0.5L / 충전시간: 3시간30분 / 사용시간: 1시간 / 용량: 2500mAh /
 브러쉬: 바닥, 솔형, 틈새, 침구, 연장관 / 거치대 / 무게: 1.5kg / 색상:화이트 / 소비전력: 450W'
'''
data['스펙 목록'][0].split(' / ')
'''
['핸디/스틱청소기',  <== 카테고리 명
 '흡입력: 140AW',    
 '흡입력: 22000Pa',
 '사용시간: 1시간',
]
'''
## '스펙 목록'에 대한 패턴 분석
'''
카테고리 : 첫 번째 항목에 위치
사용시간 : 00분 /00 시간   <== 사용시간
흡입력: 000pa / 000AW     <== 흡입력
'''
# 카테고리
spec_list = data['스펙 목록'][0].split(' / ')

category = spec_list[0]  # '핸디/스틱청소기'

# 흡입력 / 사용시간
use_time_spec = ''   # '사용시간: 1시간
suction_spec = ''    #  '흡입력: 22000Pa'

for spec in spec_list: 
    if '사용시간' in spec:
        use_time_spec = spec
    elif '흡입력' in spec:
        suction_spec = spec

use_time_value = use_time_spec.split(' ')[1].strip() # '1시간'
suction_value = suction_spec.split(' ')[1].strip()   # '22000Pa'
# -------------------------------------------------------
category_list = []
use_time_list = []
suction_list = []

for sepc_data in data['스펙 목록']:
    # ' / ' 기준으로 스펙 분리하기
    spec_list = sepc_data.split(' / ')
    
    # 카테고리 추출하기
    category = spec_list[0]
    category_list.append(category)
    
    # 사용시간, 흡입력 추출
    # => 사용시간, 흡입력 정보가 없는 제품을 위해 변수를 생성
    use_time_value = None   # use_time_value = ''
    suction_value = None
    
    # spect_list의 각 원소에서 사용시간, 흡입력 수치 추출
    for sepc in spec_list:
        if '사용시간' in spec:
            use_time_value = spec.split(' ')[1].strip()
        if '흡입력'  in spec:
            suction_value = spec.split(' ')[1].strip()
            
    use_time_list.append(use_time_value)
    suction_list.append(suction_value)

### 3. 무선 청소기 사용시간 단위 통일 ###
'''
'시간' 단어가 있으면 
1시간 60분
1. '시간'앞의 숫자를 추출한 뒤, 60곱하기 => 분
2. '시간'뒤에 '분' 글자 앞의 숫자를 추출하여 시간에 더하기

'시간' 단어가 없으면
'분' 글자 앞의 숫자를 추출하여 시간에 더하기

예외 처리
'''
# 데스트 코드
times= ["40분", "4분", "1시간", "3시간30분", "4시간"]

def convert_time_minute(time): # "40분"
    try:
        if '시간' in time:
            hour = time.split('시간')[0]
            if '분' in time:
                minute = time.split('시간')[-1].split('분')[0]
            else:
                minute = 0
        else:
            hour = 0
            minute = time.split('분')[0]
        return int(hour)*60 + int(minute)
    except:
        return None
'''
                minute = time.split('시간')[-1].split('분')[0]
#                       "3시간30분"
#                            ["3", "30분"]                       
#                                      "30분" 
#                                        ["30"]
#                                             30
'''
for time in times:
    time_value = convert_time_minute(time)
    print(time, "=", time_value)
'''
40분 = 40
4분 = 4
1시간 = 60
3시간30분 = 210
4시간 = 240
'''
#------------------------------
# 모델별 사용시간을 분 단위로 통일
new_use_time_list = []

for time in use_time_list:
    value = convert_time_minute(time)
    new_use_time_list.append(value)
    


#### 무선 청소기 흡입력 단위 통일 ####
'''
AW : 진공청소기의 전력량(AirWatt)
W : 모터의 소비전력단위(Watt)
PA : 흡입력 단위(Pascal)

(IW == 1AW == 100PA)
'''
# 흡입력 단위를 통일시키는 함수
def get_suction(value):
    try:
        value = value.upper()
        if "AW" in value or "w" in value:
            result = value.replace("A", "").replace("w","")
            result = int(result.replace(",",""))
        elif "PA" in value:
            result = value.replace("PA", "")
            result = int(result.replace(",",""))/100
        else:
            result = None
        return result
    except:
        return None
'''
대소문자를 통일하기 위해보든 알파벳 문자를 대문자로 통일
만약 흡입력에 "AW", "W" 가 있으면
   1. 흡입력에서 "A" 와 "W"를 삭제
   2. "," 글자를 삭제한 후,
      숫자형 데이터로 변환
만약 흡입력에 "PA" 가 있으면
   1. 흡입력에서 "PA"를 삭제
   2. ","를 삭제한 후,
   숫자형으로 바꾸고 watt 단위로 통일하기 위해 100으로 나눔
   흡입력 값이 비어 있거나 단위변환 시, 문제가 있으면 예외로 처리
'''
# 흡입력 단위 통일
new_suction_list = []

for power in suction_list:
    value = get_suction(power)
    new_suction_list.append(value)

#---------------------------- 여기까지 분석에 필요한 전처리-----------------
### 다나와 전처리 결과를 엑셀로 저장 ###

pd_data = pd.DataFrame()

pd_data['카테고리'] = category_list
pd.data['회사명'] = company_list
pd.data['제품'] = product_list
pd_data['가격'] = data['가격']
pd_data['사용시간'] = new_use_time_list
pd.data['흡입력'] = new_suction_list

# 카테고리 분류 기준 및 데이터 개수 점검
pd.data.value_count()

# 핸디/스틱청소기만 선택
pd_data_final = pd_data[pd_data['카테고리'].isin(['핸디/스틱청소기'])]

# 가성비
pd_data_final['가격'].unique()

# 엑셀로 저장
pd_data_final.to_excel('./data/danawa_data_final.xlsx', index=False)



















