#!/usr/bin/env python
from .objects import *
import json

tools_path = os.path.dirname(os.path.abspath(__file__))
cts_filename = 'Constantes.json'
Constantes_path = os.path.join(tools_path,cts_filename)

with open(Constantes_path, 'r') as Cfile:
    Cts = json.load(Cfile)

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
def export_data(data,directory,filename) :
	full_path = os.path.join(Cts[directory],filename)
	print(full_path)
	with open(full_path,'w',encoding="utf-8") as output_file :
		json.dump(data,output_file,sort_keys=True,indent=4)

def main() :
	pass

if __name__ == "__main__":
	main()