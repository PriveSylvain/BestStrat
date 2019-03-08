#!/usr/bin/env python

from Tools.objects import *
from Tools import methodes as mth
import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def fill_df_proba(df_proba,df_main,df_bust) :
	for cj in df_main :
		for cc in df_main[cj].keys() :
			if df_main[cj][cc] != 0 :
				df_proba[cj][cc] = "%.4f"%(df_bust[cj][cc]/df_main[cj][cc])
			else :
				df_proba[cj][cc] = 0
	return df_proba	
def strat(joueur,pioche) :
	joueur.tirer(pioche)
	if joueur.calculer() > 21 :
		joueur.bust = True
		joueur.play = True
	else :
		joueur.bust = False
		joueur.play = False

def main() :

	joueurs,croupier,pioche = mth.initialiser_partie(nombre_joueurs = 10,nombre_paquets = 6,solde_depart = 10000)
	pioche.shuffle(5)
	pioche.burn(5)

	df_main = mth.start_stat()
	df_bust = mth.start_stat()

	for i in range(5000) :
		mth.faitesVosJeux(joueurs)
		croupier.distribuer(joueurs,pioche)
		score_c = croupier.calculer()
		for j in joueurs :
			score_j = j.calculer()
			df_main[score_j][score_c]+=1
		for j in joueurs :
			j.appliquer_strategie(pioche,strat)
			if j.bust :
				df_bust[score_j][score_c]+=1
		
		croupier.appliquer_strategie(pioche)
		#mth.who_won(joueurs,croupier)

		for j in joueurs :
			j.reset()
		croupier.reset()
		pioche.reset()
		i+=1
	#note : la fonction de distribution de df_main peu etre interessant par la suite...
	df_proba = mth.start_stat()
	df_proba = fill_df_proba(df_proba,df_main,df_bust)
	mth.export_df2csv(df_proba,"output",__file__)

if __name__ == "__main__":
	main()
