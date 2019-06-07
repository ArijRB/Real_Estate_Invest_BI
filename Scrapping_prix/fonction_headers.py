# ---------------------------------------------------
# Import des modules nécessaires
# ---------------------------------------------------
import time
import csv
from random import randint
import urllib.parse

# ------------------------------------------------------------------------------------------------------
# FONTION : choisir un user agent à utiliser pour le navigateur 
# ------------------------------------------------------------------------------------------------------
def my_user_agent():
    # Ouvrir le fichier avec les proxies
    fichier = open("../data/user-agent.csv","r")    
    cr = csv.reader(fichier, delimiter = '%')

    my_list = []

    # Charger les proxies dans un tableau
    for row in cr:
        my_list.append({'user-agent': row[0]})
    
    nb_ua = len(my_list)
    #print("# Nbe UA : ", nb_ua)

    # Choisir un proxy au hasard
    ua_num = randint(0, nb_ua)-1
    my_ua = my_list[ua_num]
    #print(my_ua['user-agent'])

    print('# INFO : FONCTION my_user_agent : Affectation d\'un User Agent')
    return my_ua['user-agent']
