#!/usr/bin/env python

from Tools.objects import *
from Tools import methodes as mth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main() :
	""" déterminer le compte final le plus probable du croupier en fonction de la première carte tirée
	"""

	joueurs,croupier,pioche = mth.initialiser_partie(nombre_joueurs = 6,nombre_paquets = 6)
	pioche.shuffle(5)
	pioche.burn(5)

	OUTPUT_FILE = "data_dealer_bust.json"
	json_f_path = os.path.join("output",OUTPUT_FILE)

	data = {}
	data["n"] = 1000
	data["1ere carte"] = {}

	for i in range(data["n"]) :
		carte = croupier.tirer(pioche)
		value = carte.getValue()

		if value not in data["1ere carte"].keys() :
			data["1ere carte"][value] = {}
			data["1ere carte"][value]["distrib"] = 0
			data["1ere carte"][value]["bust"] = 0
			data["1ere carte"][value]["compte_final"] = {'17':0,'18':0,'19':0,'20':0,'21':0}
		data["1ere carte"][value]["distrib"] += 1

		croupier.appliquer_strategie(pioche)
		compte = croupier.calculer()

		if croupier.bust :
			data["1ere carte"][value]["bust"] += 1
		else :
			data["1ere carte"][value]["compte_final"][str(compte)] += 1 
		mth.reset_all(joueurs,croupier,pioche)

	mth.check_and_export_data2json(data,json_f_path)

	# proba de bust en ayant tiré cette carte = nb_bust / (nb_tirage de cette carte)
	prob_bust = {}
	for value in data["1ere carte"] :
		prob_bust[value] = data["1ere carte"][value]["bust"] / data["1ere carte"][value]["distrib"]

	s = pd.Series(prob_bust,Pioche.values)
	s.plot.bar()
	plt.show()
	

if __name__ == "__main__":
	main()
