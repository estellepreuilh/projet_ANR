# -*- coding:utf-8 -*-

import ConfigParser
from tulip import *
import math
import json
import pandas as pd
import numpy as np


class View(object):
        """docstring for View"""
        def __init__(self):
                super(View, self).__init__()		
                self.config = ConfigParser.ConfigParser()
                self.config.read('app/webapp.ini')
                self.store_path = self.config.get('view', 'store_path')

        def graph2json(self, graph):
                json_object = {}
                label = graph['Libellé de partenaire']

                nodes = []                        
                for n in graph.getNodes():
                        node={ 'id': n.id ,'label': label[n],'group':graph['viewMetric'][n]}
                        nodes.append(node)
                        
                json_object['nodes'] = nodes
                links = []
                for e in graph.getEdges():
                        links.append({'from': graph.source(e).id, 'to': graph.target(e).id})
                json_object['links'] = links
                
                with open('static/universities.json', 'w') as fp:
                        json.dump(json_object, fp)

        def graph2json2(self,graph,univ):
                json_object = {}
                label = graph['Libellé de partenaire']

                nodes = []                        
                for n in graph.getNodes():              #on cherche le libelle correspondant à l'id univ.
                        if n.id==univ:
                                univlab=label[n]
                                break

                for n in graph.getNodes():                      
                        if label[n]==univlab or univlab in graph['Partenaires communs'][n] :
                                node={ 'id': n.id ,'label': label[n]}
                                nodes.append(node)
                        
                json_object['nodes'] = nodes
                links = []
                for e in graph.getEdges():
                        if univlab in graph['Partenaires'][e] :
                                a_ajouter=True
                                for a in links:
                                        if (a['from']==graph.source(e).id and a['to']==graph.target(e).id):  #on regarde si une arête entre cette source et cette cible existe déjà, et dans ce cas on ajoute dans ces paramètre le projet et on incrémente de 1 le nombre de projet.
                                                a['title']=a['title']+', '+graph['Projet'][e][0]
                                                a['value']=a['value']+1
                                                a['label']=str(a['value'])+' projets'
                                                a_ajouter=False                                                #dans ce cas pas besoin d'ajouter une nouvelle arête
                                                break
                                if (a_ajouter==True):                                        #si il n'existe pas encore une arête entre cette source et cette cible, on en créé une
                                        links.append({'from': graph.source(e).id, 'to': graph.target(e).id,'label' : '1 projet' ,'font': {'align': 'middle'},'value':1,'title': graph['Projet'][e][0] })       
                json_object['links'] = links             
                with open('static/university.json', 'w') as fp:
                       json.dump(json_object, fp)                        
                return univlab


        def ville2json(self,ville):
                data = pd.read_csv("static/fr-esr-aap-anr-projets-retenus-participants-identifies.csv",sep=";",encoding ='utf-8')  
                year=u'Année de financement'
                part=u'Libellé de partenaire'
                projet=u'Acronyme'
                montant=u'Montant'
                data=data.loc[:,[projet,year,montant,part]] 
                data.dropna(inplace=True)
                data = data.reset_index()
                data = data.drop(["index"],axis=1)
                l=[]
                for i in range(0,len(data)):
                    if ville not in data.loc[i,part]:
                        l.append(i)                    
                data=data.drop(l)   #on enlève tous les projets auxquels la ville n'a pas participé
                data=data.reset_index()
                data = data.drop(["index"],axis=1)
                df=pd.DataFrame(columns=['Partenaire','Projet','Annee','Montant','id']) 
                line=0
                for i in range(0,len(data)):
                        part_proj=data.loc[i,part].split(';')   #liste de tous les partenaires d'un projet
                        a=0
                        for x in part_proj:
                                if ville in x and x not in part_proj[0:a]:  #x not in part_proj[0:a] car certains partenaires apparaissent plusieurs fois pour un même projet.
                                        df.loc[line,'Partenaire']=x.replace(',', '')
                                        df.loc[line,'Annee']=data.loc[i,year]
                                        df.loc[line,'Projet']=data.loc[i,projet]
                                        df.loc[line,'Montant']=data.loc[i,montant]
                                        df.loc[line,'id']=line
                                        line+=1
                                a+=1
                df.to_json('static/city.json',orient='records')

        def generate_graph(self):
                json_object = {}
                data = pd.read_csv("static/fr-esr-aap-anr-projets-retenus-participants-identifies.csv", sep=";")
                data = data.loc[:,["Acronyme","Sigle de partenaire"]]
                data = data.dropna()
                data = data.reset_index()
                data = data.drop(["index"],axis=1)
                #data contient tous les projets caractérisés par les colonnes "acronyme", et "sigle de partenaire"
                #les projets ayant des valeurs manquantes pour l'acronyme ou le sigle de partenaire sont supprimés
                liste = []
                #liste va contenir les partenaires qui partagent des projets avec le labri
                for i in range(0,len(data)):
                        if 'LaBRI' in data.loc[i,"Sigle de partenaire"]:
                                for x in data.loc[i,"Sigle de partenaire"].split(";"):
                                        if x !='':
                                                liste.append(x)

                liste_ = list(set(liste)) #on ne garde qu'une occurence de chaque partenaire
                node=[]
                #node contient l'ensemble des partenaires qui seront des noeuds sur notre graphe
                for j in range(0,len(liste_)):
                        if liste_[j]=="LaBRI":
                                node.append({'id':liste_[j], 'label':liste_[j], 'group':0}) #la couleur des noeuds sera différente selon le groupe
                        else :
                                node.append({'id':liste_[j], 'label':liste_[j], 'group':liste.count(liste_[j])}) #le groupe représente le nombre de projet partagé(s) avec le labri

                json_object['nodes'] = node
                link=[]
                #link represente les arrêtes de notre graphe, value représente la largeur de l'arête qui sera plus epaisse selon le nombre de projets partagés avec le labri
                for j in range(0,len(liste_)):
                        if liste_[j]!="LaBRI": 
                                link.append({'from':"LaBRI",'to':liste_[j] , 'value':node[j]["group"]*6})

                json_object['links'] = link   
                with open('static/labri.json', 'w') as fp:
                        json.dump(json_object, fp)

        def projet(self,sigle):
                data = pd.read_csv("static/fr-esr-aap-anr-projets-retenus-participants-identifies.csv", sep=";",encoding='utf-8')
                data = data.loc[:,["Acronyme",u'Année de financement',"Montant","Sigle de partenaire"]]
                data = data.dropna(subset=['Acronyme','Sigle de partenaire'])
                data = data.reset_index()
                data = data.drop(["index"],axis=1)
                data=data.fillna(0)
                #Data contient tous les projets caractérisés par les colonnes "acronyme", "année de financement","montant" et "sigle de partenaire"
                #Les projets ayant des valeurs manquantes pour l'acronyme ou le sigle de partenaire sont supprimés (car dans la selection pour faire le graphe précédent (generate.graph()) nous ne prenons que
                #ces deux colonnes, si nous supprimons aussi les lignes ayant des valeurs manquantes pour année de financement et montant alors des projets comptés précédemment seront supprimés
                #et il y aura moins de projets affichés que de projets prévus (par la couleur par exemple sur le graphe du labri)
                #Donc les valeurs manquantes pour l'année de financement ou le montant sont remplacées par des 0
                
                liste = []
                #liste va contenir tous les projets ayant le labri et "sigle" (le partenaire sur lequel on a cliqué) dans ses sigles de partenaire.
                for i in range(0,len(data)):
                        if sigle in data.loc[i,"Sigle de partenaire"] and 'LaBRI' in data.loc[i,"Sigle de partenaire"] :
                                liste.append(i)
                

                proj = pd.DataFrame(index = range(0,len(liste)), columns = ["Acronyme","Annee","Montant","Partenaire" ])
                #proj contient les projets commun entre le labri et le partenaire voulu caractérisés par l'acronyme, l'année de financement, le montant et les autres partenaires
                for j in range(0,len(liste)):
                        proj.loc[j, "Acronyme"] = data.loc[liste[j],u"Acronyme"]
                        proj.loc[j,"Partenaire"] = data.loc[liste[j],"Sigle de partenaire"]
                        proj.loc[j, "Annee"] = data.loc[liste[j],u"Année de financement"]
                        proj.loc[j,"Montant"] = data.loc[liste[j],"Montant"]
                        

                proj.to_csv('static/projects_part_labri.csv', sep=",", encoding='utf-8', index=False)

        

      
