import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from user import *
from constant import *

# Fonction permettant de générer les plots des résultats obtenus par la simulation, la liste passer en paramettre contient l'ensembles des agents à prendre en compte dans le plot
def plotDecision(list=list):
    
    # Initialisation du nombre d'agents choisissants chaque moyen de transport en décision rationnelle 
    # rationalDecision[0] = velo, rationalDecision[1] = voiture, rationalDecision[2] = bus, rationalDecision[3] = marche
    rationalDecision=[0,0,0,0]

    # Initialisation du nombre d'agents choisissants chaque moyen de transport en décision biaisée
    biasedDecision=[0,0,0,0]

    # Initialisation du nombre d'agents choisissant chaque moyen de transport en décision habituelle
    habitualDecision=[0,0,0,0]


    # Boucle permettant de compter le nombre d'agents choisissants chaque moyen de transports en décision biaisée
    for agent in list:
        if agent.biasChoise==BIKE:
            biasedDecision[0]+=1
        if agent.biasChoise==CAR:
            biasedDecision[1]+=1
        if agent.biasChoise==BUS:
            biasedDecision[2]+=1
        if agent.biasChoise==WALK:
            biasedDecision[3]+=1

    # Boucle permettant de compter le nombre d'agents choisissants chaque moyen de transports en décision rationnelle
    for agent in list:
        if agent.rationalChoice==BIKE:
            rationalDecision[0]+=1
        if agent.rationalChoice==CAR:
            rationalDecision[1]+=1
        if agent.rationalChoice==BUS:
            rationalDecision[2]+=1
        if agent.rationalChoice==WALK:
            rationalDecision[3]+=1
    
    # Boucle permettant de compter le nombre d'agents choisissants chaque moyen de transports en décision habituelle
    for agent in list:
        if agent.habiChoice==BIKE:
            habitualDecision[0]+=1
        if agent.habiChoice==CAR:
            habitualDecision[1]+=1
        if agent.habiChoice==BUS:
            habitualDecision[2]+=1
        if agent.habiChoice==WALK:
            habitualDecision[3]+=1

    # Récupération des noms des différents moyens de transport (Pour les axes du plot)
    names = LISTMODES
   
    
    # Définition de la dimmension du plot 
    plt.figure(figsize=(9, 3))

    # Définition d'un sous plot de type histogramme correspondant aux décisions rationnelles prises par les agents de la simulation 
    plt.subplot(131)
    plt.title('Rational Decision')
    plt.bar(names, rationalDecision)

    # Définition d'un sous plot de type histogramme correspondant aux décisions biaisées prises par les agents de la simulation 
    plt.subplot(132)
    plt.title('Biased Decision')
    plt.bar(names, biasedDecision)
    
    # Définition d'un sous plot de type histogramme correspondant aux décisions habituelles prises par les agents de la simulation 
    plt.subplot(133)
    plt.title('Habitual Decision')
    plt.bar(names, habitualDecision)
    
    # Définition du titre du plot
    plt.suptitle('Bias effect on decision making')
    
    # Affichage du plot 
    plt.show()
    