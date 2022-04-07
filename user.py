from re import L
from tkinter import DoubleVar
from math import *

from switch import *



class user:

    def __init__(self,) -> None:
        preferenceCar = int(input("Quel est mon degré de préférence pour la voiture ? saisir un flotant de 1 à 4 où 1 est transport préféré et 4 est le transport le moins apprécié"))
        preferenceBike = int(input("Quel est mon degré de préférence pour le vélo ? saisir un flotant de 1 à 4 où 1 est transport préféré et 4 est le transport le moins apprécié"))
        preferenceBus = int(input("Quel est mon degré de préférence pour le bus ? saisir un flotant de 1 à 4 où 1 est transport préféré et 4 est le transport le moins apprécié"))
        preferenceWalk = int(input("Quel est mon degré de préférence pour le bus ? saisir un flotant de 1 à 4 où 1 est transport préféré et 4 est le transport le moins apprécié"))
        self.preference = list(("c",preferenceCar),("bu",preferenceBus),("bi",preferenceBike),("w",preferenceWalk))


        self.agent = generateAgent()

        ## Préférence (ex ecologie confort cf switch python)
        ## Météo 
        ## Fitness level
        ## contraintes cf switch (sauf agenda)



        self.gasPrice=float
        self.subPrice=float
        self.ratioCycleWay=float
        self.busFrequency=int
        self.busCapacity=int
        self.carSpeed=int
        self.bikeSpeed=int
        self.walkSpeed=int
        self.busSpeed=int
