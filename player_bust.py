#!/usr/bin/env python

from Tools.objects import *
from Tools import methodes as mth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from includes import CONSTANTES

def main() :
	joueurs,croupier,pioche = mth.initialiser_partie(nombre_joueurs = 10,nombre_paquets = 6,solde_depart = 10000)
	pioche.shuffle(5)
	pioche.burn(5)

	DATA_PLAYER_BUST_JSON = "data_player_bust.json"

	data = {}
	data["n"] = 1000
	data["dealing"] = {}

	for i in range(data["n"]) :

		mth.faitesVosJeux(joueurs,0)
		croupier.distribuer(joueurs,pioche)
		score_c = croupier.calculer()

		for j in joueurs : 
			score_j = str(j.calculer())
			if not score_j in data["dealing"].keys() :
				data["dealing"][score_j] = {}
				data["dealing"][score_j]["distrib"] = 0
				data["dealing"][score_j]["bust"] = 0
				data["dealing"][score_j]["count"] = {}
			data["dealing"][score_j]["distrib"] += 1
			

		for j in joueurs :
			score_j = str(j.calculer())
			j.tirer(pioche)
			score_j_3 = str(j.calculer())
			if int(score_j_3) > 21 :
				data["dealing"][score_j]["bust"] += 1
			else : 
				if not score_j_3 in data["dealing"][score_j]["count"].keys() :
					data["dealing"][score_j]["count"][score_j_3] = 0
				data["dealing"][score_j]["count"][score_j_3] += 1
		mth.reset_all(joueurs,croupier,pioche)
	
	mth.check_and_export_data2json(data,directory = "output",filename = DATA_PLAYER_BUST_JSON)

	prob_bust = {}
	distrib_function = {}
	for value in data["dealing"] :
		prob_bust[int(value)] = data["dealing"][value]["bust"] / data["dealing"][value]["distrib"]
		distrib_function[int(value)] = data["dealing"][value]["distrib"]
	
	P_PROBA_BUST_JSON = "proba_player_bust.json"
	P_DISTRIB_FUNC_JSON = "player_distrib_function.json"
	P_PROBA_BUST_PNG = "proba_player_bust.png"
	P_DISTRIB_FUNC_PNG = "player_distrib_function.png"

	mth.export_data2json(prob_bust,os.path.join("output",P_PROBA_BUST_JSON))
	mth.export_data2json(distrib_function,os.path.join("output",P_DISTRIB_FUNC_JSON))

	f = pd.Series(distrib_function,sorted(distrib_function.keys()))
	f.plot.bar()
	plt.xlabel("Player hand (occurence = %d)"%(data["n"]))
	plt.ylabel("distribution function")
	plt.show()
	plt.savefig(os.path.join("output",P_DISTRIB_FUNC_PNG))

	s = pd.Series(prob_bust,sorted(prob_bust.keys()))
	s.plot.bar()
	plt.xlabel("Player hand (occurence = %d)"%(data["n"]))
	plt.ylabel("probability of going bust")
	plt.show()
	plt.savefig(os.path.join("output",P_PROBA_BUST_PNG))

if __name__ == "__main__":
	main()
