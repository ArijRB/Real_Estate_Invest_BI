
import pandas as pd
from pymongo import MongoClient
DB_NAME = 'meilleurs_agents'
data = pd.read_csv('cities_france.csv',";")
villes=list(data["Name"])
connection = MongoClient("mongodb://mongoarij:secretarij@51.75.25.98:27017/admin")
db = connection[DB_NAME]
coll=db.commune_prix_immo
ventes=[]
locations=[]
for ville in coll.find():

    if ville["nom_commune"] in villes:
        for e in (list(ville["prix_m2_vente"]["meilleurs_agents"])):
            v=dict()
            if "Maison" in e.keys() and 'Appartement' in e.keys():
                v["date_extraction"]=e["date"]
                v["nom_commune"]=ville["nom_commune"]
                v["prix_maison_moyen_m2_vente"]=e["Maison"]["all"]["prix_m2_moyen"]
                v["prix_maison_bas_m2_vente"]=e["Maison"]["all"]["prix_m2_bas"]
                v["prix_maison_haut_m2_vente"]=e["Maison"]["all"]["prix_m2_haut"]
                v["prix_appartement_moyen_m2_vente"]=e["Appartement"]["all"]["prix_m2_moyen"]
                v["prix_appartement_bas_m2_vente"]=e["Appartement"]["all"]["prix_m2_bas"]
                v["prix_appartement_haut_m2_vente"]=e["Appartement"]["all"]["prix_m2_haut"]
                ventes.append(v)
        for e in (list(ville["prix_m2_location"])):
            l=dict()
            if "Maison" in e.keys() and 'Appartement' in e.keys():
                l["date_extraction"]=e["date"]
                l["nom_commune"]=ville["nom_commune"]
                l["prix_maison_moyen_m2_location"]=e["Maison"]["all"]["prix_m2_moyen"]
                l["prix_maison_bas_m2_location"]=e["Maison"]["all"]["prix_m2_bas"]
                l["prix_maison_haut_m2_location"]=e["Maison"]["all"]["prix_m2_haut"]
                l["prix_appartement_moyen_m2_location"]=e["Appartement"]["all"]["prix_m2_moyen"]
                l["prix_appartement_bas_m2_location"]=e["Appartement"]["all"]["prix_m2_bas"]
                l["prix_appartement_haut_m2_location"]=e["Appartement"]["all"]["prix_m2_haut"]
                locations.append(l)
                print(l)

df = pd.DataFrame.from_records(ventes)
df.to_csv('prix_vente.csv',index=False)
df = pd.DataFrame.from_records(locations)
df.to_csv('prix_locations.csv',index=False)
