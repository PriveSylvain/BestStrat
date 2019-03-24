#!/usr/bin/env python

from Tools.objects import *
from Tools import methodes as mth
import os
import json
import pprint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections

def merge_data(data_in,data_out) :
	"""once loaded from the json file, data is merge to the new generated data"""
	if type(data_in) == dict :
		for key in data_in :
			data_out[key] = merge_data(data_in[key],data_out[key])
	else :
		data_out += data_in
	return data_out
def load_json_file(json_f_path) :
	"""load data from the existing json file"""
	with open(json_f_path,'r') as json_f :
		return json.load(json_f)
def data_already_exist(json_f_path) :
	"""check if data has already been generated before"""
	return(os.path.exists(json_f_path))
def test_data_structure(data_in,data_out,result = False) :
	"""test if data structure from json file is compatible with the generated one"""
	if type(data_in) == type(data_out) :
		if type(data_in) == dict :
			for key in data_in.keys() :
				if key in data_out.keys() :
					result = True
					return test_data_structure(data_in[key],data_out[key],result)
				else :
					return False
		else :
			return True
	else :
		return False


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
			data["1ere carte"][value]["bust"] = 0
			data["1ere carte"][value]["compte_final"] = {'17':0,'18':0,'19':0,'20':0,'21':0}

		croupier.appliquer_strategie(pioche)
		compte = croupier.calculer()

		if croupier.bust :
			data["1ere carte"][value]["bust"] += 1
		else :
			data["1ere carte"][value]["compte_final"][str(compte)] += 1 
		mth.reset_all(joueurs,croupier,pioche)

	mth.check_and_export_data2json(data,json_f_path)

	prob_bust = {}
	for value in data["1ere carte"] :
		prob_bust[value] = data["1ere carte"][value]["bust"] / data["n"]

	s = pd.Series(prob_bust,Pioche.values)
	s.plot.bar()
	plt.show()
	

if __name__ == "__main__":
	main()
