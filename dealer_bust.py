#!/usr/bin/env python3

from Tools.objects import *
from Tools import methodes as mth
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from includes import CONSTANTES

def main() :
	""" déterminer le compte final le plus probable du croupier en fonction de la première carte tirée
	"""

	joueurs,croupier,pioche = mth.initialiser_partie(nombre_joueurs = 6,nombre_paquets = 6)
	pioche.shuffle(5)
	pioche.burn(5)

	DATA_DEALER_BUST_JSON = "data_dealer_bust.json"

	data = {}
	data["n"] = 1000
	data["dealing"] = {}

	for i in range(data["n"]) :
		croupier.tirer(pioche)
		value = str(croupier.calculer())

		if value not in data["dealing"].keys() :
			data["dealing"][value] = {}
			data["dealing"][value]["distrib"] = 0
			data["dealing"][value]["bust"] = 0
			data["dealing"][value]["final_count"] = {'17':0,'18':0,'19':0,'20':0,'21':0}
		data["dealing"][value]["distrib"] += 1

		croupier.appliquer_strategie(pioche)
		compte = str(croupier.calculer())

		if croupier.bust :
			data["dealing"][value]["bust"] += 1
		else :
			data["dealing"][value]["final_count"][compte] += 1 
		mth.reset_all(joueurs,croupier,pioche)

	mth.check_and_export_data2json(data,directory = "output",filename = DATA_DEALER_BUST_JSON)

	# proba de bust en ayant tiré cette carte = nb_bust / (nb_tirage de cette carte)
	prob_bust = {}
	distrib_func = {}
	for value in data["dealing"] :
		nb_bust = data["dealing"][value]["bust"]
		nb_occurrences = data["dealing"][value]["distrib"]
		prob_bust[value] = nb_bust / nb_occurrences
		for f_count in data["dealing"][value]["final_count"] :
			f_count_occur = data["dealing"][value]["final_count"][f_count]
			value_occur = (data["dealing"][value]["distrib"] - data["dealing"][value]["bust"])
			distrib_func[f_count] = f_count_occur / value_occur
	
	D_PROBA_BUST_JSON = "proba_dealer_bust.json"
	D_DISTRIB_FINAL_COUNT_JSON = "dealer_distrib_final_count.json"
	D_PROBA_BUST_PNG = "proba_dealer_bust.png"
	D_DISTRIB_FINAL_COUNT_PNG = "dealer_distrib_final_count.png"

	INDEX_FIRST_CARD = ["2","3","4","5","6","7","8","9","10","11"]
	INDEX_D_FINAL_COUNT = ["17","18","19","20","21"]

	mth.export_data2json(prob_bust,os.path.join("output",D_PROBA_BUST_JSON))
	mth.export_data2json(distrib_func,os.path.join("output",D_DISTRIB_FINAL_COUNT_JSON))

	sbust = pd.Series(prob_bust,INDEX_FIRST_CARD)
	sbust.plot.bar()
	plt.xlabel("Dealer hand (occurence = %d)"%(data["n"]))
	plt.ylabel("probability of going bust")
	plt.show()
	plt.savefig(os.path.join("output",D_PROBA_BUST_PNG))

	sdistrib = pd.Series(distrib_func,INDEX_D_FINAL_COUNT)
	sdistrib.plot.bar()
	plt.xlabel("Dealer final count (occurence = %d)"%(data["n"]))
	plt.ylabel("distribution function")
	plt.show()
	plt.savefig(os.path.join("output",D_DISTRIB_FINAL_COUNT_PNG))

if __name__ == "__main__":
	main()
