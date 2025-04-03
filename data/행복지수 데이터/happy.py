# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 16:30:30 2025

@author: Admin
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import font_manager, rc
import platform

if platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname= path).get_name()
    rc('font', family = font_name)
elif platform.sytem() == 'Darwin':
    rc('font', family = 'AppleGothic')
else:
    print('Check your OS system')


health = pd.read_excel('./data/행복지수 데이터/대한민국행복지도_교육건강.xlsx')
economy = pd.read_excel('./data/행복지수 데이터/대한민국행복지도_경제.xlsx')
relationship = pd.read_excel('./data/행복지수 데이터/대한민국행복지도_관계및사회참여.xlsx')
education = pd.read_excel('./data/행복지수 데이터/대한민국행복지도_교육.xlsx')
life_satisfaction = pd.read_excel('./data/행복지수 데이터/대한민국행복지도_삶의만족도.xlsx')
safety = pd.read_excel('./data/행복지수 데이터/대한민국행복지도_안전.xlsx')
leisure = pd.read_excel('./data/행복지수 데이터/대한민국행복지도_여가.xlsx')
environment = pd.read_excel('./data/행복지수 데이터/대한민국행복지도_환경.xlsx')

health.drop('시도', axis = 1, inplace = True)
health.rename(columns = {'평균' : '행복_평균'}, inplace = True)

economy.drop('시도', axis = 1, inplace = True)
economy.rename(columns = {'관계_평균' : '경제_평균'}, inplace = True)

relationship.drop('시도', axis = 1, inplace = True)
relationship.rename(columns = {'평균' : '관계_평균'}, inplace = True)

education.drop('시도', axis = 1, inplace = True)
education.rename(columns = {'관계_평균' : '교육_평균'}, inplace = True)

life_satisfaction.drop('시도', axis = 1, inplace = True)
life_satisfaction.rename(columns = {'삶의 만족도' : '삶의 만족도_평균'}, inplace = True)


safety.drop('시도', axis = 1, inplace = True)
safety.rename(columns = {'평균' : '안전_평균'}, inplace = True)

leisure.drop('시도', axis = 1, inplace = True)
leisure.rename(columns = {'평균' : '여가_평균'}, inplace = True)

environment.drop('도시지역 중 '녹지지역 비율'', axis = 1, inplace = True)
environment.rename(columns = {'평균' : '환경_평균'}, inplace = True)


columns = ['행복_평균', '경제_평균', '관계_평균', '교육_평균', '삶의 만족도_평균', '안전_평균','여가_평균', '환경_평균' ]

































