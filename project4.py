#!/usr/local/bin/python3

# Computer Project-I
# Project 4

import sys
import numpy as np
from time import sleep
from urllib.request import urlopen
from bs4 import BeautifulSoup
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
# URL of YOK Computer Engineering undergraduate programs page
programPageUrl = 'https://yokatlas.yok.gov.tr/2017/lisans-bolum.php?b=10024'
# Open Computer Engineering undergraduate programs page
programsPage = urlopen(programPageUrl)
# HTML Parser for undergraduate Computer Engineering programs page
programsParser = BeautifulSoup(programsPage, 'html.parser')

# Find all 'div' lines of university and program names
nameDiv = programsParser.find_all('div', attrs={'style': 'overflow: hidden; text-overflow: ellipsis; white-space: nowrap;width:80%'})

# Extract university and program names from 'div' lines
universityNames = []
for name in nameDiv:
    universityNames.append(name.text.strip())

# Find all 'a' lines of program URLs from 'a' lines
linkA = programsParser.find_all('a', attrs={'data-parent': '#'})

# Extract link extensions of program URLs from 'a' lines
programLinks = []
for extension in linkA:
    programLinks.append(extension['href'][6:])

# Get quotes, lowest student ranks and average YGS math nets of undergraduate programs using found links 
programQuotes = [[],[],[],[],[],[],[]]
lowestStudentRanks = []
averageMathNets = []

import cograf
city_list = cograf.get_cities()

regions = ["Marmara","Ege","Karadeniz","Ic Anadolu","Akdeniz","Dogu Anadolu","Guney Dogu Anadolu"]


def openUrl(url,tries = 4, delay=3,backoff=2,logger=None):
    while tries>1:
        try:
            return urlopen(url)
        except:
            print('Retrying in', delay,'seconds')
            sleep(delay)
            tries -= 1
            delay += backoff
    return urlopen(url)
    

for i in range(len(programLinks)):
    uniLink = 'https://yokatlas.yok.gov.tr/2017/lisans' + programLinks[i]
    uniPage = openUrl(uniLink)
    uniParser = BeautifulSoup(uniPage, 'html.parser')
    
    city = uniParser.find('h3', attrs= {'class':'panel-title'})
    city_str = str(city)
    city_split = city_str.split('(')[1]
    city_split_name = city_split.split(')')[0]
    
    quota = uniParser.find_all('strong')
    quotaLink = 'https://yokatlas.yok.gov.tr/2017/content/lisans-dynamic/1000_2' + programLinks[i]
    quotaPage = openUrl(quotaLink)
    quotaParser = BeautifulSoup(quotaPage, 'html.parser')
    quota = quotaParser.find('td', attrs= {'class':'tdr text-center'})
    
    
    
    city_bolge = 0
    
    for k in range(len(city_list)):
        for j in range(len(city_list[k])):
            if(city_split_name==city_list[k][j]):
                city_bolge = k
    programQuotes[city_bolge].append(int(quota.text.strip()))
    
    
    mathURI = 'https://yokatlas.yok.gov.tr/2017/content/lisans-dynamic/1210a' + programLinks[i]
    mathOpen = openUrl(mathURI)
    
    mathParsed = BeautifulSoup(mathOpen, 'html.parser')
    try:
        mathText = mathParsed.findAll('td', attrs= {'class':'text-center'})
        mathText = mathText[8].text.strip()
        mathText = mathText.replace(',','.')
        
        mathScore = float(mathText)
    except:
        mathScore = 0.0

    lastEntranceURI = 'https://yokatlas.yok.gov.tr/2017/content/lisans-dynamic/1070' + programLinks[i]
    lastEntranceOpen = openUrl(lastEntranceURI)
    

    lastEntranceParsed = BeautifulSoup(lastEntranceOpen, 'html.parser')
    lastEntranceText = lastEntranceParsed.findAll('td')
    lastEntranceText = lastEntranceText[11].text.strip()
    lastEntranceText = lastEntranceText.replace('.','')
    try:
        lastEntranceRank = int(lastEntranceText)
    except:
        lastEntranceRank = 0 
    print(mathScore)
    print(lastEntranceRank)
    if(mathScore > 0 and lastEntranceRank > 0):
        averageMathNets.append(mathScore)
        lowestStudentRanks.append(lastEntranceRank) 
        print(i)
    
plt.scatter(lowestStudentRanks,averageMathNets,color = 'black')

lowRank = np.array(lowestStudentRanks)
lowRank = lowRank.reshape(-1,1)
mathNets= np.array(averageMathNets)
mathNets = mathNets.reshape(-1,1)
reg = LinearRegression().fit(lowRank, mathNets)
rMetric = reg.score(lowRank,mathNets)
mathresults = reg.predict(lowRank)
plt.plot(lowRank,mathresults,color='red', linewidth = 2)
plt.show()
fig7, ax7 = plt.subplots()
plt.ylabel('Quota')
ax7.set_title('Quotes of Universities w.r.t to Regions')
ax7.boxplot(programQuotes)
plt.show()
print('R Square metric' + ' ' + str(rMetric))