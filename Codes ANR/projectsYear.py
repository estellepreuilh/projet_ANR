# -*- coding:utf-8 -*-

import pandas as pd

data = pd.read_csv("fr-esr-aap-anr-projets-retenus-participants-identifies.csv", sep=";", encoding='utf-8')
data = data.loc[:,[u"Année de financement",u"Libellé de partenaire"]] 
data = data.dropna()
data = data.reset_index()
data = data.drop(["index"],axis=1)

cities = ["Paris","Marseille","Lyon","Toulouse","Nice","Nantes","Montpellier","Strasbourg","Bordeaux","Lille"]
years = [2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016]


j=0
year = pd.DataFrame(index = range(0,len(years)), columns = ["Year","Count" ])
ligne = 0
for i in range(0,len(years)):
    for k in range(0,len(data)):
            if data.loc[k,u"Année de financement"] == years[i]:
               j += 1
    year.loc[ligne, "Year"] = years[i]
    year.loc[ligne, "Count"] = j
    ligne += 1
    j=0

year.to_csv("../ANR/static/projectsYear.csv", sep=",", index=False)

