#!/usr/bin/env python
from .objects import *
import json
import os
import pandas as pd
import logging


def initialiser_partie(nombre_joueurs = 6,nombre_paquets = 6,solde_depart = 1000) :
	croupier = Croupier()
	pioche = Pioche(nb_deck = nombre_paquets)
	joueurs = []
	for i in range(nombre_joueurs) :
		joueur = Joueur(solde = solde_depart)
		joueurs.append(joueur)
	return(joueurs,croupier,pioche)
def jouer_partie(joueurs,croupier,pioche) :
	for j in joueurs :
		j.miser(10)
	for j in joueurs :
		j.tirer(pioche)
		j.tirer(pioche)
	croupier.tirer(pioche)
	for j in joueurs :
		j.appliquer_strategie(pioche)
	croupier.appliquer_strategie(pioche)
def _who_won(joueur,croupier) :
	C_compte = croupier.calculer() 
	if joueur.play and not joueur.bust :
		if croupier.bust or joueur.calculer() > C_compte :
			joueur.crediter()
		elif joueur.calculer() < C_compte :
			joueur.debiter()
	else :
		joueur.debiter()
def who_won(instance,croupier) :
	if isinstance(instance,list) :
		for joueur in instance:
			_who_won(joueur,croupier)
	elif isinstance(instance,Joueur) :
		_who_won(instance,croupier)
def reset_all(joueurs,croupier,pioche) :
	if isinstance(joueurs,list) :
		for j in joueurs :
			j.reset()
	elif isinstance(joueurs,Joueur) :
		joueurs.reset()
	croupier.reset()
	pioche.reset()
def faitesVosJeux(joueurs,mise=1) :
	for j in joueurs :
		j.miser(mise)
def start_stat(l=range(4,22),L=range(2,12),p=0.0) :
	data = [p]*10
	narray = {}
	for i in l:
		s = pd.Series(data,index = L)
		narray[i]=s
	df = pd.DataFrame(narray)
	return df

def check_and_export_data2json(data,directory,filename) :
	json_f_path = os.path.join(directory,filename)
	if data_already_exist(json_f_path) :
		data_from_json = load_json_file(json_f_path)
		if test_data_structure(data_from_json,data) :
			data = merge_data(data_from_json,data)
		else : 
			logging.warning("json file cannot be merged to data : its structure doesn't match with the current structure.")
	else : 
		logging.warning("%s file does not exist. new one will be generated in few seconds"%(filename))

	export_data2json(data,json_f_path)
def data_already_exist(json_f_path) :
	"""check if data has already been generated before"""
	return(os.path.exists(json_f_path))
def load_json_file(json_f_path) :
	"""load data from the existing json file"""
	if os.path.exists(json_f_path) :
		with open(json_f_path,'r') as json_f :
			return json.load(json_f)
	else :
		logging.warning("json file not found")
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
def merge_data(data_in,data_out) :
	"""once loaded from the json file, data is merge to the new generated data"""
	if type(data_in) == dict :
		for key in data_in.keys() :
			data_out[key] = merge_data(data_in[key],data_out[key])
	else :
		data_out += data_in
	return data_out
def export_data2json(data,json_f_path) :
	with open(json_f_path,'w',encoding="utf-8") as output_file :
		json.dump(data,output_file,sort_keys=True,indent=4)

def export_df2csv(df,directory,filename) :
	directory = "output"
	if not os.path.exists(directory) :
		os.mkdir(directory)
	output_file = os.path.join(directory,filename.replace(".py",".csv"))
	df.to_csv(output_file, sep = '\t')

def main() :
	pass

if __name__ == "__main__":
	main()