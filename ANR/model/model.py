# -*- coding:utf-8 -*-

from flask import Flask, request
from tulip import *
import ConfigParser

class Model(object):
	"""docstring for Model"""
	def __init__(self):
		super(Model, self).__init__()
		self.config = ConfigParser.ConfigParser()
		self.config.read('app/webapp.ini')
		self.model_path = self.config.get('data', 'path')

	def load_graph(self):
		'''
		on va chercher un sous-graphe
		(ici, on fait simple, on ne fait que charger le graphe depuis un fichier)
		'''
		graph = tlp.loadGraph(self.model_path)

		return graph

		
		
