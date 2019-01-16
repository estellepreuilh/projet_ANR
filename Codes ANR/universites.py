# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import tlp
import random
import time

# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# The main(graph) function must be defined 
# to run the script on the current graph

def main(graph): 
  Acronyme = graph.getStringProperty("Acronyme")
  Annee_de_financement = graph.getIntegerProperty("AnnÃ©e de financement")
  Code_du_programme = graph.getStringProperty("Code du programme")
  Code_du_projet = graph.getStringProperty("Code du projet")
  Code_du_type_de_partenaire = graph.getStringVectorProperty("Code du type de partenaire")
  Coordinateur_du_projet = graph.getStringProperty("Coordinateur du projet")
  Date_de_debut = graph.getIntegerProperty("Date de dÃ©but")
  Duree_en_mois = graph.getIntegerProperty("DurÃ©e en mois")
  Identifiant_de_partenaire = graph.getStringVectorProperty("Identifiant de partenaire")
  Libelle_de_partenaire = graph.getStringVectorProperty("LibellÃ© de partenaire")
  Lien_Programme = graph.getStringProperty("Lien Programme")
  Lien_Projet = graph.getStringProperty("Lien Projet")
  Montant = graph.getDoubleProperty("Montant")
  Perspectives = graph.getStringProperty("Perspectives")
  Programme = graph.getStringProperty("Programme")
  Publications_et_brevets = graph.getStringProperty("Publications et brevets")
  Resultats = graph.getStringProperty("RÃ©sultats")
  Resume = graph.getStringProperty("RÃ©sumÃ©")
  Resume_de_la_soumission = graph.getStringProperty("RÃ©sumÃ© de la soumission")
  Sigle_de_partenaire = graph.getStringVectorProperty("Sigle de partenaire")
  Titre = graph.getStringProperty("Titre")
  Type_didentifiant = graph.getStringVectorProperty("Type d'identifiant")
  Type_de_partenaire = graph.getStringVectorProperty("Type de partenaire")
  viewBorderColor = graph.getColorProperty("viewBorderColor")
  viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
  viewColor = graph.getColorProperty("viewColor")
  viewFont = graph.getStringProperty("viewFont")
  viewFontSize = graph.getIntegerProperty("viewFontSize")
  viewIcon = graph.getStringProperty("viewIcon")
  viewLabel = graph.getStringProperty("viewLabel")
  viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
  viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
  viewLabelColor = graph.getColorProperty("viewLabelColor")
  viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
  viewLayout = graph.getLayoutProperty("viewLayout")
  viewMetric = graph.getDoubleProperty("viewMetric")
  viewRotation = graph.getDoubleProperty("viewRotation")
  viewSelection = graph.getBooleanProperty("viewSelection")
  viewShape = graph.getIntegerProperty("viewShape")
  viewSize = graph.getSizeProperty("viewSize")
  viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
  viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
  viewTexture = graph.getStringProperty("viewTexture")
  viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
  viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")

  start_time = time.time()

  partenaire=tlp.newGraph()
  list=[]
  print ('Création des noeuds:')
  
  for n in graph.getNodes():    
    libPart=Libelle_de_partenaire[n]     
    for i in range (0,len(libPart)):     
      if "Université" in libPart[i]:          
        if libPart[i] not in list :        #si on rencontre ce partenaire pour la premiÃ¨re fois       
          list.append(libPart[i])
          node=partenaire.addNode()
          x=random.randrange(1,1025,1)
          y=random.randrange(1, 1025, 1)
          projet=[Acronyme[n]]
          communs=[]
          for j in range (0,len(libPart)):      
            if libPart[j]!=libPart[i] and libPart[j] not in communs and "Université" in libPart[j]:
              communs.append(libPart[j])    
          dict={"Libellé de partenaire": libPart[i], "Projet" : projet ,"Partenaires communs": communs ,"viewColor":(200,150,80,230) ,"viewLayout":tlp.Coord(x,y,0)}
          partenaire.setNodePropertiesValues(node,dict)
          
        else :  #ce partenaire a dÃ©jÃ  un noeud, on le cherche alors parmi tous les noeuds du nouveau graphe, et on ajoute dans ses paramÃ¨tres le projet n et les partenaires communs 
          for o in partenaire.getNodes():            
            if libPart[i] == partenaire.getStringProperty("Libellé de partenaire")[o] and Acronyme[n] not in partenaire.getStringVectorProperty("Projet")[o] : 
              communs=[]              
              for j in range (0,len(libPart)):      
                if libPart[j]!=libPart[i] and libPart[j] not in communs and libPart[j] not in partenaire.getStringVectorProperty("Partenaires communs")[o] and "Université" in libPart[j]:
                  communs.append(libPart[j])
              dict={"Libellé de partenaire": partenaire.getStringProperty("Libellé de partenaire")[o] ,  "Projet" : partenaire.getStringVectorProperty("Projet")[o]+[Acronyme[n]] , "Partenaires communs": partenaire.getStringVectorProperty("Partenaires communs")[o]+communs, "viewColor":(200,150,80,230)}
              partenaire.setNodePropertiesValues(o,dict) 
  
  print ("Création des arêtes")
  
  node1=0
  for p in partenaire.getNodes():    
    node2=0
    for q in partenaire.getNodes():      
      for i in partenaire.getStringVectorProperty("Projet")[p] :
        if i in partenaire.getStringVectorProperty("Projet")[q] and partenaire.getStringProperty("Libellé de partenaire")[q] in partenaire.getStringVectorProperty("Partenaires communs")[p] and p!=q and node2>=node1 :     #node1 et node2 pour Ã©viter que les arÃªtes soient en double     
          e=partenaire.addEdge(p,q)
          dict={"Projet":[i],"Partenaires" :[partenaire.getStringProperty("Libellé de partenaire")[p],partenaire.getStringProperty("Libellé de partenaire")[q]]}
          partenaire.setEdgePropertiesValues(e,dict) 
      node2+=1
    node1+=1
    
    
  print ("Louvain")
  params = tlp.getDefaultPluginParameters('Louvain', partenaire)
  partenaire.applyDoubleAlgorithm('Louvain', params)
  
  tlp.saveGraph(partenaire,"univlouv.tlp")
  interval = time.time() - start_time 
  print ('Total time in seconds:', interval) 
    
    
    
    
    
