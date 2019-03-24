#!/usr/bin/env python

from Tools.objects import *
from Tools import methodes as mth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main() :

	joueurs,croupier,pioche = mth.initialiser_partie(nombre_joueurs = 10,nombre_paquets = 6,solde_depart = 10000)
	pioche.shuffle(5)
	pioche.burn(5)

	OUTPUT_FILE = "data_player_bust.json"
	path_output_file = os.path.join("output",OUTPUT_FILE)

	data = {}
	data["n"] = 1000
	data["dealing"] = {}

	for i in range(data["n"]) :

		mth.faitesVosJeux(joueurs,0)
		croupier.distribuer(joueurs,pioche)
		score_c = croupier.calculer()

		# les joueurs possèdent 2 cartes : calcul de distribution
		for j in joueurs : 
			score_j = str(j.calculer())
			if not score_j in data["dealing"].keys() :
				data["dealing"][score_j] = {}
				data["dealing"][score_j]["distrib"] = 0
				data["dealing"][score_j]["bust"] = 0
				data["dealing"][score_j]["compte"] = {}
			data["dealing"][score_j]["distrib"] += 1
		
		# les joueurs reçoivent une 3eme carte :
		#	comptabilise le nombre de bust en fonction du dealing de départ
		#	si le joueur n'a pas bust, quel compte à-t-il et combien de fois l'a-t-il eut

		for j in joueurs :
			score_j = str(j.calculer())
			j.tirer(pioche)
			score_j_3 = str(j.calculer())
			if int(score_j_3) > 21 :
				data["dealing"][score_j]["bust"] += 1
			else : 
				if not score_j_3 in data["dealing"][score_j]["compte"].keys() :
					data["dealing"][score_j]["compte"][score_j_3] = 0
				data["dealing"][score_j]["compte"][score_j_3] += 1
		mth.reset_all(joueurs,croupier,pioche)
	mth.check_and_export_data2json(data,path_output_file)

if __name__ == "__main__":
	main()
