# -*- coding: utf-8 -*-

# ---------------------------------------------------
# Import des modules nécessaires
# ---------------------------------------------------
import sys

import requests
from lxml import html
from datetime import datetime
from datetime import date
import datetime
import time
from fonction import fonction_liste_ville
import fonction_get_session_proxy
import math
import random
from fonction import fonction_headers
from multiprocessing.pool import ThreadPool as Pool
from lxml.html.clean import clean_html
import fonction_get_my_ip
import json
import re
import urllib.parse
from datetime import timedelta
# ------------------------------------------------------------------------------------------------------
# Variables globales
# ------------------------------------------------------------------------------------------------------

# Définir le header
header = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Host':'www.meilleursagents.com',
    'Pragma':'no-cache',
    'Referer':'https://www.meilleursagents.com/',
    'X-Requested-With':'XMLHttpRequest',
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

# Nombre utilisation d'IP
nb_utilisation_ip = 0
nb_utilisation_ip_max = 10

# Identification d'une session proxy
s = fonction_get_session_proxy.get_session()

# Nombre d'annonces insérées par ville
nb_annonce_ville_insere = 0

# informations des prix
resultat=dict()
# ------------------------------------------------------------------------------------------------------
# Collecter les données sur les prix immo d'une ville
# ------------------------------------------------------------------------------------------------------
def collecter_donnee_prix_immo(type_recherche, departement_to_extract, ville_to_extract):
    
    # Créer la liste des url des villes concernées
    liste_url_ville = creer_liste_url_ville(type_recherche, departement_to_extract, ville_to_extract)   

    # Pour chaque ville, collecter les données
    pool_size = 5
    pool = Pool(pool_size)

    for ville in liste_url_ville:
        pool.apply_async(collecter_donnee, (ville,))
    
    pool.close()
    pool.join()


# ------------------------------------------------------------------------------------------------------
# Créer la liste des url pour ville 
# ------------------------------------------------------------------------------------------------------
def creer_liste_url_ville(type_recherche, departement_to_extract, ville_to_extract):
    # Créer la liste des villes à crawler
    liste_ville = fonction_liste_ville.create_list_ville(type_recherche, departement_to_extract, ville_to_extract)

    # Créer la liste des urls de chaque ville
    liste_url_ville = []

    for ville in liste_ville:
        url_ville = creer_url_ville(ville)
        liste_url_ville.append({'url':url_ville, 'code_departement':ville['code_departement'], 'code_insee':ville['code_insee'], 'code_postal':ville['code_postal'], 'nom_commune':ville['nom_commune']})
    
    print("# INFO | =========================================================")
    print("# INFO | Département traité : ", departement_to_extract)
    print("# INFO | Nombre de ville(s) : ", len(liste_url_ville))
    print("# INFO | =========================================================")

    #print("# DEV | ", liste_url_ville)
    return liste_url_ville

# ------------------------------------------------------------------------------------------------------
# Créer le format de l'url pour une ville 
# ------------------------------------------------------------------------------------------------------
def creer_url_ville(ville):
    
    # Formatage de la ville
    nom_ville_formate = ville['nom_commune'].lower() # transformé en minuscule
    nom_ville_formate = nom_ville_formate.replace("' ",'-') # suppression des "apostrophe + espace"
    nom_ville_formate = nom_ville_formate.replace('e  ','eme-') # suppression des espaces
    nom_ville_formate = nom_ville_formate.replace(' ','-') # suppression des espaces
    nom_ville_formate = nom_ville_formate.replace("'",'-') # suppression des apostrophes seuls
    nom_ville_formate = nom_ville_formate.replace('é','e') # remplacement des é
    nom_ville_formate = nom_ville_formate.replace('è','e') # remplacement des è
    nom_ville_formate = nom_ville_formate.replace('ê','e') # remplacement des ê
    nom_ville_formate = nom_ville_formate.replace('à','a') # remplacement des à
    nom_ville_formate = nom_ville_formate.replace('â','a') # remplacement des â
    nom_ville_formate = nom_ville_formate.replace('î','i') # remplacement des î
    nom_ville_formate = nom_ville_formate.replace('ï','i') # remplacement des ï
    nom_ville_formate = nom_ville_formate.replace('ô','o') # remplacement des ô
    nom_ville_formate = nom_ville_formate.replace('û','u') # remplacement des û
    nom_ville_formate = nom_ville_formate.replace('ü','u') # remplacement des ü
    nom_ville_formate = nom_ville_formate.replace('ç','c') # remplacement des ç
    nom_ville_formate = nom_ville_formate.replace('ÿ','y') # remplacement des ÿ

    # Formatage pour Paris, Marseille, Lyon
    if nom_ville_formate in ('paris', 'lyon', 'marseille'):
        if ville['code_postal'][3:5] == '01':
            texte_arrondissement_nbe = '1er'
        elif ville['code_postal'][3:5] in ('02', '03', '04', '05', '06', '07', '08', '09'):
            texte_arrondissement_nbe = ville['code_postal'][4:5] + 'eme'
        else:
            texte_arrondissement_nbe = ville['code_postal'][3:5] + 'eme'

        nom_ville_formate = nom_ville_formate + '-' + texte_arrondissement_nbe + '-arrondissement'
        
    # Création de l'url complète Meilleurs agents
    code_postal = ville['code_postal']
    url_ville = "http://meilleursagents.com/prix-immobilier/" + nom_ville_formate + "-" + code_postal
  
    return url_ville

# ------------------------------------------------------------------------------------------------------
# Collecter les données Prix Moyen à l'achat et à la location
# ------------------------------------------------------------------------------------------------------
def collecter_donnee(ville):
    # Préciser les variables globales
    global nb_utilisation_ip
    global nb_utilisation_ip_max
    global s

    # Attendre 2 secondes avant de lancer le traitement
    time.sleep(0.5)

    # Tester la connexion et changer d'IP si ça ne marche
    test_boucle = ''
    while test_boucle == '': 
        try:
            if  nb_utilisation_ip > 10:
                s = fonction_get_session_proxy.get_session()
                nb_utilisation_ip = 0
            else:
                pass

            ip = s.get(ville['url'], headers = header, timeout=20)

            nb_utilisation_ip = nb_utilisation_ip + 1

            tree = html.fromstring(ip.content)

            test_boucle = 'OK'
            break
        except Exception as e:
            print("# ERREUR collecter_donnee | Ville traitée : ", ville['code_postal'], " - ", ville['nom_commune'], " | Url de la ville à traiter ", ville['url'], " | Erreur : ", e)
            s = fonction_get_session_proxy.get_session()
            nb_utilisation_ip = 0
            test_boucle = ''

    # Identifier les données à récupérer
    code_postal = ville['code_postal']
    code_departement = ville['code_departement']
    nom_commune = ville['nom_commune']
    code_insee = ville['code_insee']

    # Datas appartement V2
    xpath_flat_base = '//*[@class="prices-summary__apartment-prices"]'
    xpath_flat_presence = xpath_flat_base + '/div/p/text()'
    xpath_flat_price_moyen = xpath_flat_base + '/ul/li[2]/text()'
    xpath_flat_price_bas_haut = xpath_flat_base + '/ul/li[3]/text()'

    try:
        data_flat_v2 = tree.xpath(xpath_flat_presence)[0]
        if data_flat_v2 == "Appartement":
            prix_flat_moyen = tree.xpath(xpath_flat_price_moyen)[0]                
            prix_flat_moyen = formater_prix_moyen_v2(prix_flat_moyen)

            prix_flat_bas_haut = tree.xpath(xpath_flat_price_bas_haut)[0]
            prix_flat_bas_haut = formater_prix_bas_haut_v2(prix_flat_bas_haut)

            prix_flat_bas = prix_flat_bas_haut['prix_bas']
            prix_flat_haut = prix_flat_bas_haut['prix_haut']
    except Exception as e:
        print(e)
        data_flat_v2 = 0
        prix_flat_bas = "Non disponible"
        prix_flat_moyen = "Non disponible"
        prix_flat_haut = "Non disponible"
        print("# WARNING : Pas de données Appartement modèle V2")

    # Datas Maison V2
    xpath_house_base = '//*[@class="prices-summary__house-prices"]'
    xpath_house_presence = xpath_house_base + '/div/p/text()'
    xpath_house_price_moyen = xpath_house_base + '/ul/li[2]/text()'
    xpath_house_price_bas_haut = xpath_house_base + '/ul/li[3]/text()'
    try:
        data_house_v2 = tree.xpath(xpath_house_presence)[0]
        if data_house_v2 == "Maison":
            prix_house_moyen = tree.xpath(xpath_house_price_moyen)[0]                
            prix_house_moyen = formater_prix_moyen_v2(prix_house_moyen)

            prix_house_bas_haut = tree.xpath(xpath_house_price_bas_haut)[0]
            prix_house_bas_haut = formater_prix_bas_haut_v2(prix_house_bas_haut)

            prix_house_bas = prix_house_bas_haut['prix_bas']
            prix_house_haut = prix_house_bas_haut['prix_haut']
    except Exception as e:
        print(e)
        data_house_v2 = 0
        prix_house_bas = "Non disponible"
        prix_house_moyen = "Non disponible"
        prix_house_haut = "Non disponible"
        print("# WARNING : Pas de données Maison modèle V2")

    # Date d'extraction
    date_extraction = str(time.strftime('%Y-%m-%d %H:%M:%S'))
    
    # Insérer les données des prix immo de la ville
    data = {
            'code_departement': code_departement,
            'code_insee': code_insee, 
            'code_postal': code_postal, 
            'nom_commune': nom_commune,
            'prix_m2_vente':{
                'source_meilleursagents':[{
                    'date_extraction': date_extraction, 
                    'appartement':{
                        'prix_m2_bas': prix_flat_bas,
                        'prix_m2_moyen': prix_flat_moyen,
                        'prix_m2_haut':prix_flat_haut
                    },
                    'maison':{       
                        'prix_m2_bas': prix_house_bas,
                        'prix_m2_moyen': prix_house_moyen,
                        'prix_m2_haut':prix_house_haut
                    }
                }]
            }
        }

    source = 'meilleursagents'
    
    resultat.add(data)
    
    print("# INFO collecter_donnee | ", code_postal, " - ", nom_commune, " | ", data, " | ", reponse)

# ------------------------------------------------------------------------------------------------------
# Formater les prix moyen affiché 
# ------------------------------------------------------------------------------------------------------
def formater_prix_moyen_v2(prix):
    try: 
        prix = prix.replace('\n','')
        prix = prix.replace('\n','')
        prix = prix.replace('\t','')
        prix = prix.replace('\r','')
        prix = prix.replace('\xa0','')
        prix = prix.replace(' ','')
        prix = prix.replace('€Indicedeconfiance','') 
        prix = prix.replace('€','')
        prix = prix.replace(',','.')
    except Exception as e:
        print(e)
        prix = "Non disponible"               

    #print('# FONCTION formater_prix_V2 : formatage des prix : ', prix )
    return prix

# ------------------------------------------------------------------------------------------------------
# Formater les prix bas et haut affichés dans le modèle V2
# ------------------------------------------------------------------------------------------------------
def formater_prix_bas_haut_v2(prix):
    try: 
        prix = prix.replace('\n','')
        prix = prix.replace('\n','')
        prix = prix.replace('\t','')
        prix = prix.replace('\r','')
        prix = prix.replace('\xa0','')
        prix = prix.replace(' ','')
        prix = prix.replace('€Indicedeconfiance','') 
        prix = prix.replace('€','')
        prix = prix.replace(',','.')

        #print("# BRUT PRIX FONCTION : ", prix)
        
        prix.index("de")
        prix.index("à")

        prix_bas = prix[ prix.index("de")+2 : prix.index("à") ]
        prix_haut = prix[ prix.index("à")+1 : ]
    except:
        prix_haut = "Non disponible" 
        prix_bas = "Non disponible"               

    prix_bas_haut = {'prix_bas':prix_bas, 'prix_haut': prix_haut}   

    #print('# FONCTION formater_prix_V2 : formatage des prix : ', prix_bas_haut )
    return prix_bas_haut

# ------------------------------------------------------------------------------------------------------
# PROGRAMME PRINCIPAL DU MODULE
# ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    collecter_donnee_prix_immo(2, "", "")



# ---------------------------------------------------
# FIN - PROGRAMME PRINCIPAL DU MODULE
# ---------------------------------------------------
