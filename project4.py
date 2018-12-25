#!/usr/local/bin/python3

# Computer Project-I
# Project 4

import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# URL of YOK Computer Engineering undergraduate programs page
programPageUrl = 'https://yokatlas.yok.gov.tr/lisans-bolum.php?b=10024'
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


for i in range(len(programLinks)):
    uniLink = 'https://yokatlas.yok.gov.tr/lisans' + programLinks[i]
    uniPage = urlopen(uniLink)
    uniParser = BeautifulSoup(uniPage, 'html.parser')
    
    city = uniParser.find('h3', attrs= {'class':'panel-title'})
    city_str = str(city)
    city_split = city_str.split('(')[1]
    city_split_name = city_split.split(')')[0]
    
    quota = uniParser.find_all('strong')
    quotaLink = 'https://yokatlas.yok.gov.tr/content/lisans-dynamic/1000_2' + programLinks[i]
    quotaPage = urlopen(quotaLink)
    quotaParser = BeautifulSoup(quotaPage, 'html.parser')
    quota = quotaParser.find('td', attrs= {'class':'tdr text-center'})
    
    
    
    city_bolge = 0
    
    for k in range(len(city_list)):
        for j in range(len(city_list[k])):
            if(city_split_name==city_list[k][j]):
                city_bolge = k
    programQuotes[city_bolge].append(int(quota.text.strip()))
    
    quotaLink = 'https://yokatlas.yok.gov.tr/content/lisans-dynamic/1000_2' + programLinks[i]
    quotaPage = urlopen(quotaLink)
    quotaParser = BeautifulSoup(quotaPage, 'html.parser')
    quota = quotaParser.find('td', attrs= {'class':'tdr text-center'})
    

    averageMathNetLink = 'https://yokatlas.yok.gov.tr/content/lisans-dynamic/1210a' + programLinks[i]
    averageMathNetPage = urlopen(averageMathNetLink)
    averageMathNetParser = BeautifulSoup(averageMathNetPage, 'html.parser')
    averageMathNetString = averageMathNetParser.findAll('td', attrs= {'class':'text-center'})
    if not averageMathNetString:
        averageMathNet = 0.0
    else:
        averageMathNetString = averageMathNetString[8].text.strip()
        averageMathNetString = averageMathNetString.replace(',','.')
        averageMathNet = float(averageMathNetString)
    
    
    
    
    lowestStudentLink = 'https://yokatlas.yok.gov.tr/content/lisans-dynamic/1070' + programLinks[i]
    lowestStudentPage = urlopen(lowestStudentLink)
    lowestStudentParser = BeautifulSoup(lowestStudentPage, 'html.parser')
    lowestStudentRankString = lowestStudentParser.findAll('td', attrs= {'align':'center'})[5].text.strip()

    if lowestStudentRankString == '':
        lowestStudentRank = 0
    else:
        lowestStudentRankString = lowestStudentRankString.replace('.', '')
        lowestStudentRank = int(lowestStudentRankString)
    if(averageMathNet > 0 and lowestStudentRank > 0):
        averageMathNets.append(averageMathNet)
        lowestStudentRanks.append(lowestStudentRank) 
    print(i)
plt.scatter(lowestStudentRanks,averageMathNets)
fig7, ax7 = plt.subplots()
plt.ylabel('Quota')
ax7.set_title('Quotes of Universities w.r.t to Regions')
ax7.boxplot(programQuotes)