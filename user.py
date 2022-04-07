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

RAINY = "rainy"
TEMPOK = "temperature ok"
LIGHT = "light"
CONTEXTBOOLS = [RAINY,TEMPOK,,LIGHT]


HASBIKE = "agent has bike"
HASCAR = "agent has car"
HASBUS = "agent is on bus line"
AGENTBOOLS = [HASBIKE, HASCAR, HASBUS]
FITNESS = "agent's fitness level"


class user:

    def __init__(self,) -> None:
        x = input("(r)andom agent priorities or (u)ser input or (f)ile input? : ")
        while x not in ["u","r","f"]:
            x = input("(u)ser agent priorities or (r)andom ? : ")
        if x == "u": self = inputAgent()
        else : 
            if x=="r" : self = generateAgent()
        

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
