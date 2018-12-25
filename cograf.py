# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 10:43:31 2018

@author: BurakBey
"""

import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np


def get_cities():
    programPageUrl = 'https://www.gezenbilir.com/konu/turkiyede-bolgelere-gore-iller.59258/'
    programsPage = urlopen(programPageUrl)
    # HTML Parser for undergraduate Computer Engineering programs page
    programsParser = BeautifulSoup(programsPage, 'html.parser')
    
    # Find all 'div' lines of university and program names
    nameDiv = programsParser.find_all('blockquote', attrs={'class': 'messageText'})
    #print(nameDiv)
    
    st = str(nameDiv)
    #print(st)
    
    all_cities = []
    
    MAR = st.split('<br/>')[1]
    ICA = st.split('<br/>')[7]
    EGE = st.split('<br/>')[12]
    AKD = st.split('<br/>')[18]
    KAR = st.split('<br/>')[24]
    DOG = st.split('<br/>')[31]
    GDO = st.split('<br/>')[37].split('<')[0]
    
    all_cities.append(MAR)
    all_cities.append(ICA)
    all_cities.append(EGE)
    all_cities.append(AKD)
    all_cities.append(KAR)
    all_cities.append(DOG)
    all_cities.append(GDO)
    
    all_cities_split = []
    
    
    for bolge in all_cities:
        bolge = bolge.split(',')
        city_list = []
        for city in bolge:
            city = city.strip(' ')
            city = city.strip('.')
            city = city.strip('\n')
            #print(city + '\n')
            if(len(city) > 2 ):
                
                city_list.append(city.upper())
        all_cities_split.append(city_list)

    
    return all_cities_split    