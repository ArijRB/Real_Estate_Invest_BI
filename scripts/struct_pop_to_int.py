import pandas as pd
import numpy as np

struct_pop = pd.read_csv("/Users/lauranguyen/Documents/UPMC/M1/S2/BI/PROJET_BI/data/data_csv/structure-et-densite-de-la-population-2011.csv",delimiter=';')
unchanged_columns = ['Code Département','Code INSEE','Commune',"Densité d'habitants (hab/km2)",'Département',\
                'EPCI','Superficie','geo_point_2d', 'geo_shape', 'Région']
for c in struct_pop.columns:
    if c not in unchanged_columns:
        struct_pop[c] = struct_pop[c].astype(int)

struct_pop.to_csv("../data/data_csv/struct-pop.csv", sep=';')
