
#distance = float(input("Quelle distance en kilomètres sépare mon domicile et mon lieu de travail/étude ? "))
#preference = int(input("Quel est mon moyen de transport préféré pour réaliser mon trajet quotidien ? 1 pour voiture, 2 pour vélo, 3 pour la marche, 4 pour les transports en commun")) 
#biais = int(input("Quel biais module mon choix d'un moyen de transport ? 1 pour le biais de réactance, 2 pour le biais de sous additivité, etc..."))

from re import U
from biases import biases
from user import *



a = user()
for k,v in a.critere.items :
    print(k,v)

