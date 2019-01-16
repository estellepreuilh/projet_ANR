# -*- coding:utf-8 -*-

import pandas as pd

data = pd.read_csv("fr-esr-aap-anr-projets-retenus-participants-identifies.csv", sep=";",encoding='utf-8')
data = data.loc[:,[u"Année de financement",u"Durée en mois", u"Montant"]]
data = data.dropna()
data = data.reset_index()
data = data.drop(["index"],axis=1) 

for i in range(0,len(data)):
    if data.loc[i,"Montant"]==0:
        data = data.drop(i)
        
data = data.reset_index()
data = data.drop(["index"],axis=1)
data.columns=["Année","Durée en mois","Montant"]

data.to_csv("../ANR/static/parallel.csv", sep=",", index=False)

