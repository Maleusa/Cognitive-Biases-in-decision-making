from re import L
from math import *
from switch import *

from switch import *

ECOLOGY = "ecology"
COMFORT = "comfort"
CHEAP = "cheap"
SAFETY = "safety"
PRATICITY = "praticity"
FAST = "fast"
CRITERIAS = [ECOLOGY, COMFORT, CHEAP, SAFETY, PRATICITY, FAST]

HASBIKE = "agent has bike"
HASCAR = "agent has car"
HASBUS = "agent is on bus line"
AGENTBOOLS = [HASBIKE, HASCAR, HASBUS]
FITNESS = "agent's fitness level"


class user:

    def __init__(self,) -> None:
        preferenceCar = int(input("Quel est mon degré de préférence pour la voiture ? saisir un flotant de 1 à 4 où 1 est transport préféré et 4 est le transport le moins apprécié"))
        preferenceBike = int(input("Quel est mon degré de préférence pour le vélo ? saisir un flotant de 1 à 4 où 1 est transport préféré et 4 est le transport le moins apprécié"))
        preferenceBus = int(input("Quel est mon degré de préférence pour le bus ? saisir un flotant de 1 à 4 où 1 est transport préféré et 4 est le transport le moins apprécié"))
        preferenceWalk = int(input("Quel est mon degré de préférence pour le bus ? saisir un flotant de 1 à 4 où 1 est transport préféré et 4 est le transport le moins apprécié"))
        self.preference = list(("c",preferenceCar),("bu",preferenceBus),("bi",preferenceBike),("w",preferenceWalk))

        x = input("(r)andom agent priorities or (u)ser input or (f)ile input? : ")
	    while x not in ["u","r","f"]:
	        	x = input("(u)ser agent priorities or (r)andom ? : ")
	    if x == "u": self = inputAgent()
	    else if : self = generateAgent()
        

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
