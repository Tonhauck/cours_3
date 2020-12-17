import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np
import pandas as pd

#Lecture des points OSM
#A MODIFIER
points = gpd.read_file('../data/points_FR_amenity_bar_pub.geojson')

xmin,ymin,xmax,ymax =  points.total_bounds
#TAILLE DES CELLULES (en degrés décimaux)
#MODIFIABLE
width = 0.1
height = 0.1

rows = int(np.ceil((ymax-ymin) /  height))
cols = int(np.ceil((xmax-xmin) / width))
XleftOrigin = xmin
XrightOrigin = xmin + width
YtopOrigin = ymax
YbottomOrigin = ymax- height
polygons = []
id=[]

for i in range(cols):
    Ytop = YtopOrigin
    Ybottom =YbottomOrigin
    for j in range(rows):
        polygons.append(Polygon([(XleftOrigin, Ytop), (XrightOrigin, Ytop), (XrightOrigin, Ybottom), (XleftOrigin, Ybottom)])) 
        Ytop = Ytop - height
        Ybottom = Ybottom - height
    XleftOrigin = XleftOrigin + width
    XrightOrigin = XrightOrigin + width

#Nous créons un géodataframe de type polygone
grid = gpd.GeoDataFrame({'geometry':polygons})
#Déclaration d'un système de projection (4326 = système WGS 84)
grid.set_crs(epsg=4326, inplace=True)

#Ce coefficient servira pour créer des barres visibles à grande échelle sur la carte
#MODIFIABLE
coef_exageration = 500
#Jointure spatiale entre les points et les cellules de la grille que nous avons créé
#Autrement dit : on associe les points avec la cellule dans laquelle ces points se trouvent. Ainsi, pour chaque point, 
#nous créons une cellule supplémentaire
dfsjoin = gpd.sjoin(grid,points) #Spatial join Points to polygons

#On donne un id à chaque cellule associée
dfsjoin["id"] = dfsjoin.index + 1
# On fusionne les cellules par id et nous comptons le nombre de cellules fusionnées, ce qui nous donne le nombre de points dans la cellule. 
dataFinal = dfsjoin.dissolve(by='id',aggfunc='count')
#on ajoute une variable hauteur, basé sur le champ count (ce qui servira pour l'extrusion des polygones sur la carte)
dataFinal['height'] = dataFinal['name']*coef_exageration
#Renommage du champ name en value. Le champ name contient le compte des points par cellule. Nous le renommons.
dataFinal = dataFinal.rename(columns={'name': 'value'})
#A MODIFIER
dataFinal.to_file("output_bar_pub.geojson", driver="GeoJSON")
