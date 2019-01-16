# -*- coding: utf-8 -*

#Ce code permet de récolter les données nécessaires à la création du streamgraph des villes.

import pandas as pd

data = pd.read_csv("fr-esr-aap-anr-projets-retenus-participants-identifies.csv",sep=";",encoding ='utf-8')

year=u'Année de financement'
part=u'Libellé de partenaire'

    
data=data.loc[:,[year,part]]
data.dropna(inplace=True)
data = data.reset_index()
data = data.drop(["index"],axis=1)
#data contient uniquement les colonnes "année de financement" et "libellé de partenaire" de notre base de donnée initiale. Les lignes n'ayant pas de donnée pour ces deux informations sont supprimées.

#nous allons garder uniquement les projets dont les noms de villes suivant apparaissent.
cities=['Paris','Marseille','Lyon','Toulouse','Nice','Nantes','Montpellier','Strasbourg','Bordeaux','Lille'] 

l=[]
for i in range(0,len(data)):
    k=0
    for j in range(0,len(cities)):
        if  cities[j] in data.loc[i,part]:
            k=1
    if k==0 :
        l.append(i)
            

data = data.drop(l)
data = data.reset_index()
data = data.drop(["index"],axis=1)
#nous supprimons les lignes qui ne contienent pas un partenaire ayant un nom de ville,
#biensur il y a de la perte d'information puisque chaque partenaire appartiennent à une ville mais ne l'ont pas forcément explicetement dans leur libellé
#par exemple le labri contient "bordelais" et n'est pas prit en compte ici

df=pd.DataFrame(columns=['year','place',"useless"])  #useless sera nécessaire pour d3
line=0
for i in range(0,len(data)):
    for j in range(0,len(cities)):
        if cities[j] in data.loc[i,part]:
            df.loc[line,'year']=data.loc[i,year]
            df.loc[line,'place']=cities[j]
            df.loc[line,'useless']='a'
            line+=1

df.to_csv("../ANR/static/streamcities.csv",sep=",",index=False)


