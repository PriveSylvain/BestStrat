#!/usr/bin/env python

from Tools.objects import *
from Tools import methodes as mth
import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def faitesVosJeux(joueurs,mise=5) :
	for j in joueurs :
		j.miser(mise)
def init_data_i(indice) :
	data={}
	data["players"]={}
	data["dealer"]={}
	data["stat_bust"] = {}
	return data
def start_stat() :
	"""attribuer O.5 chance de tirer une carte à tout couple compte dealer compte joueur"""
	data = [0]*10
	narray = {}
	for i in range(4,22):
		s = pd.Series(data,index = range(2,12))
		narray[i]=s
	df = pd.DataFrame(narray)
	df2 = pd.DataFrame(narray)
	return df
	
def strat(joueur,pioche) :
	joueur.tirer(pioche)
	if joueur.calculer() > 21 :
		joueur.bust = True
		joueur.play = True
	else :
		joueur.bust = False
		joueur.play = False


def main() :

	joueurs,croupier,pioche = mth.initialiser_partie()
	pioche.shuffle(5)
	pioche.burn(5)

	df_main = start_stat()
	df_bust = start_stat()

	for i in range(200) :
		faitesVosJeux(joueurs)
		croupier.distribuer(joueurs,pioche)
		print(i)
		score_c = croupier.calculer()
		for j in joueurs :
			score_j = j.calculer()
			df_main[score_j][score_c]+=1
		for j in joueurs :
			j.appliquer_strategie(pioche,strat)
			if j.bust :
				df_bust[score_j][score_c]+=1
		
		croupier.appliquer_strategie(pioche)

		mth.who_won(joueurs,croupier)
		for j in joueurs :
			j.reset()
		croupier.reset()
		pioche.reset()
		i+=1
	print(df_main)
	print(df_bust)

if __name__ == "__main__":
	main()
