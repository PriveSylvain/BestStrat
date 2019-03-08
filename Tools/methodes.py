#!/usr/bin/env python
from .objects import *
import json
import pandas as pd


def initialiser_partie(nombre_joueurs = 6,nombre_paquets = 6,solde_depart = 1000) :
	print("début de partie")
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
def who_won(joueurs,croupier) :
	C_compte = croupier.calculer()
	for j in joueurs : 
		if j.play and not j.bust :
			if croupier.bust or j.calculer() > C_compte :
				j.crediter()
			elif j.calculer() < C_compte :
				j.debiter()
		else :
			j.debiter()
def reset_all(joueurs,croupier,pioche) :
	for j in joueurs :
		j.reset()
	croupier.reset()
	pioche.reset()
def faitesVosJeux(joueurs,mise=1) :
	for j in joueurs :
		j.miser(mise)
def start_stat(p=0.0) :
	data = [p]*10
	narray = {}
	for i in range(4,22):
		s = pd.Series(data,index = range(2,12))
		narray[i]=s
	df = pd.DataFrame(narray)
	return df
def export_data2json(data,directory,filename) :
	full_path = os.path.join(directory,filename)
	with open(full_path,'w',encoding="utf-8") as output_file :
		json.dump(data,output_file,sort_keys=True,indent=4)
def export_df2csv(df,directory,filename) :
	directory = "output"
	if not os.path.exists(directory) :
		os.mkdir(directory)
	output_file = os.path.join(directory,filename.replace(".py",".csv"))
	print(output_file)
	df.to_csv(output_file, sep = '\t')

def main() :
	pass

if __name__ == "__main__":
	main()