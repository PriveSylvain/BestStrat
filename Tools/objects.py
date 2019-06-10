#!/usr/bin/env python

import argparse
import random
import sys, os, time, itertools

class Carte(object):
	"""une valeur et une couleur"""
	def __init__(self,value,color) :
		"""constructeur"""
		self.value = value
		self.color = color
	def __str__(self) :
		return '%s de %s' %(self.value,self.color)
	def getValue(self) :
		return self.value
	def getColor(self) :
		return self.color
class Pioche(object):
	"""une pioche de n*52 cartes avec n compris entre 1 et 6"""
	colors = ["trèfle","carreau","coeur","pique"]
	values = ["A","2","3","4","5","6","7","8","9","10","V","D","R"]
	def __init__(self, nb_deck = 1) :
		self.cards = []
		self.waste = []
		for n in range(nb_deck) :
			for color in Pioche.colors :
				for value in Pioche.values :
					card = Carte(value,color)
					self.cards.append(card)
	def __str__(self) :
		str_pioche = ""
		return str_pioche
	def shuffle(self,iteration = 1) :
		if iteration < 0 :
			raise ValueError
		if iteration != 0 :
			self.shuffle(iteration - 1)
		random.shuffle(self.cards)
	def burn(self,iteration = 1) :
		"""brule n cartes de la pioche vers la defausse"""
		if iteration > 0 :
			self.waste.append(self.cards.pop())
			self.burn(iteration-1)
	def tirer(self) :
		"""retourne la première carte de la pioche"""
		carte = self.cards.pop()
		self.waste.append(carte)
		return carte
	def reset(self) :
		"""replace toutes les cartes de la defausse vers la pioche puis melange"""
		self.cards += self.waste
		self.waste = []
		self.shuffle(5)	
class Joueur(object):
	"""Un joueur possède un id, un solde, une mise. sa main de départ est vide. deux status : play ou bust"""
	ID = itertools.count()
	def __init__(self,solde=1000) :
		"""constructeur"""
		self.id = next(Joueur.ID)
		self.main = []
		self.solde = solde
		self.mise = 0
		self.play = False
		self.bust = False
		print("Joueur {} créé".format(self.id))
	def __str__(self) :
		str_joueur = "Joueur {} Solde : {}\n".format(self.id,self.solde)
		for carte in self.main :
			str_joueur += "\t%s"%(carte)
		return str_joueur
	def tirer(self,pioche,iteration=1,cards = []) :
		if iteration > 0 :
			card = self._tirer(pioche)
			cards.append(card)			
			iteration -= 1
			self.tirer(pioche,iteration,cards)
		return cards
	def _tirer(self,pioche) :
		"""retourne la carte ajoutée à la main du joueur"""
		if self.play == True :
			carte = pioche.tirer()
			self.main.append(carte)
			return carte
	def sort_hand(self) :
		return self.main.sorted()
	def calculer(self) :
		"""retourne la somme des valeurs de chaque carte"""
		compte = 0
		AS = False
		for card in self.main :
			if card.getValue() == "2" :
				compte += 2
			elif card.getValue() == "3" :
				compte += 3
			elif card.getValue() == "4" :
				compte += 4
			elif card.getValue() == "5" :
				compte += 5
			elif card.getValue() == "6" :
				compte += 6
			elif card.getValue() == "7" :
				compte += 7
			elif card.getValue() == "8" :
				compte += 8
			elif card.getValue() == "9" :
				compte += 9
			elif card.getValue() == "10" :
				compte += 10
			elif card.getValue() == "V" :
				compte += 10
			elif card.getValue() == "D" :
				compte += 10
			elif card.getValue() == "R" :
				compte += 10
			elif card.getValue() == "A" :
				compte += 1
				AS = True
		if AS and compte <= 11 :
			compte += 10
		return compte
	def miser(self,mise = 10) :
		"""si son solde le permet, le joueur mise et entre dans la partie."""
		if self.solde >= mise :
			self.mise = mise
			self.play = True
			self.bust = False
	def appliquer_strategie(self,pioche,func=None) :
		"""Vide pour le moment"""
		if func :
			func(self,pioche)
		else :
			pass
	def crediter(self) :
		self.solde += self.mise
	def debiter(self) :
		self.solde -= self.mise
	def reset(self) :
		self.main = []
		self.mise = 0
		self.play = False
		self.bust = False
class Croupier(object) :
	"""dealer : tire à 16 et s'arrête à 17"""
	def __init__(self) :
		self.main=[]
		self.play = True
		self.bust = False
	def __str__(self) :
		str_croupier="DEALER :\n"
		for carte in self.main :
			str_croupier+="\t%s"%(carte)
		return str_croupier
	def tirer(self,pioche) :
		carte = pioche.tirer()
		self.main.append(carte)
		return carte
	def calculer(self) :
		compte = 0
		AS = False
		for card in self.main :
			if card.getValue() == "2" :
				compte += 2
			elif card.getValue() == "3" :
				compte += 3
			elif card.getValue() == "4" :
				compte += 4
			elif card.getValue() == "5" :
				compte += 5
			elif card.getValue() == "6" :
				compte += 6
			elif card.getValue() == "7" :
				compte += 7
			elif card.getValue() == "8" :
				compte += 8
			elif card.getValue() == "9" :
				compte += 9
			elif card.getValue() == "10" :
				compte += 10
			elif card.getValue() == "V" :
				compte += 10
			elif card.getValue() == "D" :
				compte += 10
			elif card.getValue() == "R" :
				compte += 10
			elif card.getValue() == "A" :
				compte += 1
				AS = True
		if AS and compte <= 11 :
			compte += 10
		return compte
	def distribuer(self,instance,pioche) :
		if isinstance(instance,list) : 
			for joueur in instance :
				joueur.tirer(pioche)
				joueur.tirer(pioche)
		elif isinstance(instance,Joueur) :
			instance.tirer(pioche,2)
		self.tirer(pioche)
	def appliquer_strategie(self,pioche) :
		compte = self.calculer()
		if compte > 21 :
			self.bust = True
			self.play = False
		elif compte >= 17 :
			self.bust = False
			self.play = False
		else :
			self.tirer(pioche)
			self.appliquer_strategie(pioche)
	def reset(self) :
		self.main=[]
		self.play = True
		self.bust = False