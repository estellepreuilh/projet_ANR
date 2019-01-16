#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template
import jinja2

from model import model
from view import view

data_model = model.Model()
view = view.View()

app = Flask(__name__)
app.jinja_loader=jinja2.FileSystemLoader('./view/templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/villes')
def villes():
    return render_template('streamcities.html')

@app.route('/villes/<nom>')
def city(nom):
    view.ville2json(nom)
    return render_template('city.html',mot=nom)
    
@app.route('/universite', methods = ['GET'])
def universite():
	'''
	on charge un graphe
	'''
	graph = data_model.load_graph()

	'''
	on confie le graphe calcule a la vue qui sait traduire la donnee
	"brute" en un objet qui se prete au calcul de la vue cote client
	'''
	view.graph2json(graph)

	'''
	on envoie le resultat cote client
	'''
	return render_template('universities.html')


@app.route('/universite/<univ>')
def univ(univ):
    univ=int(univ)
    graph = data_model.load_graph()
    univ=view.graph2json2(graph,univ).decode('utf-8')
    return render_template('university.html',univ=univ)

@app.route('/labri')
def Labri():
	view.generate_graph()
	return render_template('labri.html')
    
@app.route('/labri/<sigle>')
def labri3(sigle):
	view.projet(sigle)
	return render_template('projects_part_labri.html',mot=sigle)

@app.route('/mad') #mad=montant/année/durée
def mad():
    return render_template('mad.html')
    

if __name__ == '__main__':
	app.run(debug=True)
