import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np
import pandas as pd


#FOCNTION DE CALCUL DU RATIO
def ratio(x):
	result = 0
	#SI LA VALEUR DU CARROYAGE 1 = 0 alors on la remplace par 1 dans le calcul du ratio pour éviter une erreur
	if (x[6] == 0):
		result = (x[1] / 1)
	else:
	#SINON ON DIVISE CARROYAGE 1 PAR CARROYAGE 2
		result = (x[1] / x[6])
	return result


#CARROYAGE 1
#A MODIFIER
grid_bar = gpd.read_file('../data/output_bakery.geojson')
grid_bar = grid_bar.drop(['index_right'], axis=1)
#CARROYAGE 2
#A MODIFIER
grid_bakery = gpd.read_file('../data/output_bar_pub.geojson')
grid_bakery = grid_bakery.drop(['index_right'], axis=1)

dfsjoin = gpd.sjoin(grid_bakery,grid_bar) #Spatial join Points to polygons
#On donne un id à chaque cellule associée
dfsjoin["id"] = dfsjoin.index + 1
#calcul du ratio pour chaque ligne du fichier joint
dfsjoin["ratio"] = dfsjoin.apply(ratio, axis=1)
#On regroupe la grille finale selon les id de chaque cellule
dataFinal = dfsjoin.dissolve(by='id')
#A MODIFIER
dataFinal.to_file("bar_bakery.geojson", driver="GeoJSON")


