# -*- coding: utf-8 -*-

import my_controller
import requests
from lxml import html
import json

def get_proxy():
    url_api = "https://gimmeproxy.com/api/getProxy?api_key=e2887ba0-df70-4b34-a4d8-7447b1bb7835"
    #url_api = "https://gimmeproxy.com/api/getProxy?api_key=e2887ba0-df70-4b34-a4d8-7447b1bb7835&anonymityLevel=1"
    
    for i in range(0,100): # Tester la connexion et changer d'IP si ça ne marche
        try:
            s = requests.session()
            json_proxy = s.get(url_api)

            tree = html.fromstring(json_proxy.content)
            data = json.loads(tree.text)

            url_proxy = data['curl']

            return url_proxy
            
            break
        except Exception as e:
            print("# INFO | Erreur Gimmeproxy : ", e)
            pass
        
        if i == 100:
            print("# INFO | Erreur Gimmeproxy")

# FONCTION : Ouvrir une nouvelle session de requête avec un nouveau proxy
def get_session():
    
    proxy = get_proxy()
    
    proxy_to_use = {'https':proxy, 'http':proxy}

    s = requests.session()
    s.proxies.update(proxy_to_use)

    print('# INFO | Proxy utilise = ', proxy_to_use)

    return s

def get_proxy_anonyme():
    url_api = "https://gimmeproxy.com/api/getProxy?api_key=e2887ba0-df70-4b34-a4d8-7447b1bb7835&anonymityLevel=1"
    
    for i in range(0,100): # Tester la connexion et changer d'IP si ça ne marche
        try:
            s = requests.session()
            json_proxy = s.get(url_api)

            tree = html.fromstring(json_proxy.content)
            data = json.loads(tree.text)

            url_proxy = data['curl']
            
            print('# INFO | Proxy utilisé = ', url_proxy)

            return url_proxy
            
            break
        except Exception as e:
            print("# INFO | Erreur Gimmeproxy : ", e)
            pass
        
        if i == 100:
            print("# INFO | Erreur Gimmeproxy")

# FONCTION : Ouvrir une nouvelle session de requête avec un nouveau proxy
def get_session_anonyme():
    
    proxy = get_proxy_anonyme()
    
    proxy_to_use = {'https':proxy, 'http':proxy}

    s = requests.session()
    s.proxies.update(proxy_to_use)

    print('# INFO | Proxy anonyme utilisé = ', proxy_to_use)

    return s

# PROGRAMME PRINCIPAL DU FICHIER
if __name__ == '__main__':
    get_session()
