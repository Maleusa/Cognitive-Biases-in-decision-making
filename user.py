from re import L
from math import *


ECOLOGY = "ecology"
COMFORT = "comfort"
CHEAP = "cheap"
SAFETY = "safety"
PRATICITY = "praticity"
FAST = "fast"
CRITERIAS = [ECOLOGY, COMFORT, CHEAP, SAFETY, PRATICITY, FAST]



HASBIKE = "agent bike"
HASCAR = "agent has car"
HASBUS = "agent is on bus line"
AGENTBOOLS = [HASBIKE, HASCAR, HASBUS]
FITNESS = "agent's fitness level"


class user:
    ##Initialisation de l'utilsateur avec trois choix 
    def __init__(self,) -> None:
        x = input("(r)andom agent priorities or (u)ser input or (f)ile input? : ")
        while x not in ["u","r","f"]:
            x = input("(u)ser agent priorities or (r)andom ? : ")
        if x == "u": self.inputAgent(self)
        else : 
            if x=="r" : self.generateAgent(self)
            else : self.readAgent(self)
        

        ## Préférence (ex ecologie confort cf switch python)

        ## Météo 
        ## Fitness level
        ## contraintes cf switch (sauf agenda)

        self.fitness=float
        self.means=AGENTBOOLS
        self.critere=CRITERIAS
        self.gasPrice=float
        self.subPrice=float
        self.ratioCycleWay=float
        self.busFrequency=int
        self.busCapacity=int
        self.carSpeed=int
        self.bikeSpeed=int
        self.walkSpeed=int
        self.busSpeed=int

    def inputAgent(self) :
        
        for crit in CRITERIAS :
            x = float(input("Priority (0-1) of "+crit+" ? : "))
            while x<0 or x>1:
                x = float(input("Priority (0-1) of "+crit+" ? : "))
		# priority within 0-1
            self.critere[crit]=x
        for agtbool in [AGENTBOOLS]:
            x= bool(input("Do i own a "+AGENTBOOLS+"? : (y)/(n)"))
            while x not in ["y","n"]:
                x= bool(input("Do i own a "+AGENTBOOLS+"? : (y)/(n)"))
            if x == True: self.means[agtbool]=True
            else :
                self.mens[agtbool]=False
        x=float(input("Am i fit on a scale from 0 to 100 ? :"))
        while x<0 or x>100:
            x=float(input("Am i fit on a scale from 0 to 100 ? :"))
        self.fitness=x




        return 1

    def generateAgent() :
        return 1
    
    def readAgent():
        return 1
