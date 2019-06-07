import time
import csv
from random import randint
import urllib.parse

# ------------------------------------------------------------------------------------------------------
# FONTION : choisir un user agent à utiliser pour le navigateur 
# ------------------------------------------------------------------------------------------------------
def my_user_agent():
    # Ouvrir le fichier avec les proxies
    fichier = open("user-agent.csv","r")    
    cr = csv.reader(fichier, delimiter = ',')

    my_list = []

    # Charger les proxies dans un tableau
    for row in cr:
        my_list.append({'user-agent': row[0]})
    
    nb_ua = len(my_list)

    # Choisir un proxy au hasard
    ua_num = randint(0, nb_ua)-1
    my_ua = my_list[ua_num]

    print('# INFO : FONCTION my_user_agent : Affectation d\'un User Agent')
    return my_ua['user-agent']

# FONTION : lancer un navigateur via le proxy TOR - Chrome
def browser_chrome_launch(): 
    # Paramètres du proxy de TOR
    proxyIP = "127.0.0.1"
    proxyPort = 9150

    proxy = proxyIP + ":" + str(proxyPort)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=socks5://%s' % proxy)

    # User Agent sélectionné 
    my_ua = my_user_agent()

    # Ouvrir un navigateur avec le nouveau proxy
    browser = webdriver.Chrome(chrome_options=chrome_options)

    print('# INFO : FONCTION browser_launch : Lancement du navigateur avec TOR comme proxy')

    return browser

# FONTION : lancer un navigateur via le proxy TOR
def browser_launch(): 
    # Paramètres du proxy de TOR
    proxyIP = "127.0.0.1"
    proxyPort = 9150

    proxy_settings = {"network.proxy.type":1,

        "network.proxy.socks": proxyIP,
        "network.proxy.socks_port": proxyPort,
        "network.proxy.socks_remote_dns": True,

    }

    # User Agent sélectionné 
    my_ua = my_user_agent()

    # Ouvrir un navigateur avec le nouveau proxy
    caps = DesiredCapabilities.FIREFOX
    caps["marionette"] = True

    browser = Browser('firefox', profile_preferences=proxy_settings,capabilities=caps, user_agent=my_ua, wait_time=15, timeout=30)
    
    # Supprimer les cookies
    browser.cookies.delete()

    print('# INFO : FONCTION browser_launch : Lancement du navigateur avec TOR comme proxy')

    return browser

def browser_launch_proxy(ip_proxy, port_proxy): 
    # Paramètres du proxy de TOR
    proxyIP = ip_proxy
    proxyPort = port_proxy

    proxy_settings = {"network.proxy.type":1,
        'network.proxy.http': proxyIP,
        'network.proxy.http_port': proxyPort,

    }

    # User Agent sélectionné 
    my_ua = my_user_agent()

    # Ouvrir un navigateur avec le nouveau proxy
    caps = DesiredCapabilities.FIREFOX
    caps["marionette"] = True

    browser = Browser('firefox', profile_preferences=proxy_settings,capabilities=caps, user_agent=my_ua, wait_time=15, timeout=30)
    
    # Supprimer les cookies
    browser.cookies.delete()

    print('# INFO : FONCTION browser_launch : Lancement du navigateur avec TOR comme proxy')

    return browser

def browser_launch_no_safety(): 
    # Ouvrir un navigateur avec le nouveau proxy
    caps = DesiredCapabilities.FIREFOX
    caps["marionette"] = True

    browser = Browser('firefox', capabilities=caps)
    
    # Supprimer les cookies
    browser.cookies.delete()

    print('# INFO : FONCTION browser_launch : Lancement du navigateur non anonyme')

    return browser

# FONTION : Faire changer l'IP à la prochaine ouverture de navigateur
def switch_ip():
    # Ne fonctionne que si le navigateur a été fermé puis réouvert
    with Controller.from_port(port=9151) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
    print('# INFO : FONCTION switch_ip : Changement de l\'IP pour le prochain lancement du navigateur')

# FONTION : Récupérer l'IP utilisé
def get_my_ip(browser):
    browser.visit('http://icanhazip.com')
    ip_address = browser.find_by_xpath('/html/body/pre').first.text
    print('# INFO : FONCTION get_my_ip : Récupérer l\'adresse IP utilisé : ', ip_address)

# FONCTION : Charger toutes les villes dans un tableau et créer toutes les urls
def create_list_ville(type_recherche):
    # Ouvrir le fichier des villes
    if type_recherche < 3:
        fichier = open("liste_commune.csv","r")    
        cr = csv.reader(fichier, delimiter = ',')
    elif type_recherche == 3:
        fichier = open("liste_commune_selection.csv","r")    
        cr = csv.reader(fichier, delimiter = ',')
    else:
        print('# ERREUR : Type de recherche spécifiée inexistant')    

    # Charger les villes du fichier dans un tableau
    my_list = []

    for row in cr:
        my_list.append({'code_postal': row[0],'code_insee': row[1],'nom_commune': row[2],'code_departement': row[3], '100_plus_grandes': row[4], 'url': 'A définir'})
    
    #print("# Liste ville : \n", my_list)

    nb_ville = len(my_list)
    #print("# Nbe Ville : ", nb_ville)

    # Parcourir toutes les villes et formater les urls
    for ville in my_list:
        # Formatage de la ville pour Se Loger
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
        
           
        # Création de l'url complète Meilleurs agents
        code_postal = ville['code_postal']
        ville['url'] = "http://meilleursagents.com/prix-immobilier/" + nom_ville_formate + "-" + code_postal
        #print(ville['url'])

        if "Paris" in ville['nom_commune']:
            nom_ville = "Paris"
        elif "Marseille" in ville['nom_commune']:
            nom_ville = "Marseille"
        elif "Lyon" in ville['nom_commune']:
            nom_ville = "Lyon"
        else:
            nom_ville = ville['nom_commune']


        # Nom commune sans arrondissement
        nom_commune_url = ville['nom_commune']
        if ("Paris" in ville['nom_commune']) or ("Marseille" in ville['nom_commune']) or ("Lyon" in ville['nom_commune']):
            nom_commune_url = nom_commune_url.replace("1er Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("2e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("3e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("4e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("5e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("6e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("7e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("8e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("9e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("10e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("11e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("12e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("13e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("14e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("15e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("16e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("17e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("18e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("19e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace("20e  Arrondissement", "")
            nom_commune_url = nom_commune_url.replace(" ", "")
            nom_commune_url = nom_commune_url.replace("Paris1", "Paris")
            nom_commune_url = nom_commune_url.replace("Marseille1", "Marseille")
            nom_commune_url = nom_commune_url.replace("Lyon1", "Lyon")
        else:
            nom_commune_url = nom_commune_url.replace("' ", "'")
            nom_commune_url = nom_commune_url.replace("É", "E")

        ville['nom_commune_simple'] = nom_commune_url

    # Renvoyer le tableau
    print('# INFO : FONCTION create_list_ville : Chargement des villes dans un tableau avec urls formatées')
    return my_list
