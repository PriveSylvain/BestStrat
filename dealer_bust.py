#!/usr/bin/env python

from Tools.objects import *
from Tools import methodes as mth
import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main() :
	joueurs,croupier,pioche = mth.initialiser_partie(nombre_joueurs = 6,nombre_paquets = 6)
	pioche.shuffle(5)
	pioche.burn(5)

	index = Pioche.values
	data = {}
	n = 10000
	for i in range(n) :
		carte = croupier.tirer(pioche)
		value = carte.getValue()

		if value not in data.keys() :
			data[value] = 0
		croupier.appliquer_strategie(pioche)
		compte = croupier.calculer()
		if croupier.bust :
			data[value]+=1
		mth.reset_all(joueurs,croupier,pioche)
	s = pd.Series(data,index)
	s.plot.bar()
	plt.show()
	mth.export_data(data,"output","dealer_bust.txt")

if __name__ == "__main__":
	main()
