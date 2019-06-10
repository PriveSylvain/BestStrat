#!/usr/bin/env python

from Tools import objects
from Tools.objects import *
from Tools import methodes as mth
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
import sys

MISE = 0

def main() :
    """ 
    """
    joueurs,croupier,pioche = mth.initialiser_partie()
    
    PLAYER_JSON_F = "data_player_bust.json"
    DEALER_JSON_F = "data_dealer_bust.json"
    data_player = mth.load_json_file(os.path.join("output",PLAYER_JSON_F))
    data_dealer = mth.load_json_file(os.path.join("output",DEALER_JSON_F))

    data = {}
    data["clé"] = []

    for i in range(1000) :
        mth.faitesVosJeux(joueurs,MISE)
        croupier.distribuer(joueurs,pioche)
        score_c = str(croupier.calculer())
        proba_bust_dealer = data_dealer["dealing"][score_c]["bust"] / data_dealer["dealing"][score_c]["distrib"]
        for j in joueurs :
            score_j = str(j.calculer())
            if not score_j in data["clé"] :
                data[score_j] = {}
                data[score_j]["clé"] = []
                data["clé"].append(score_j)
            if not score_c in data[score_j]["clé"] :
                proba_player = 1 - (data_player["dealing"][score_j]["bust"] / data_player["dealing"][score_j]["distrib"])
                s_tot = proba_player + proba_bust_dealer
                data[score_j][score_c] = s_tot
                data[score_j]["clé"].append(score_c)
        mth.reset_all(joueurs,croupier,pioche)
    li_x = []
    for x in sorted(data["clé"]) :
        li_y = []
        for y in sorted(data[x]["clé"]) :
            li_y.append(data[x][y])
        li_x.append(li_y)
    
    HEATMAP_base_strat_PNG = "heatmap_stratégie_de_base.png"

    # print(li_x)
    plt.matshow(li_x)
    plt.title('test')
    plt.show()
    #plt.savefig(os.path.join("output",HEATMAP_base_strat_PNG))

if __name__ == "__main__":
	main()
