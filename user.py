from re import L
from math import *


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
CONTEXTBOOLS = [RAINY,TEMPOK,LIGHT]


HASBIKE = "agent has bike"
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
        if x == "u": self = inputAgent()
        else : 
            if x=="r" : self = generateAgent()
            else : self = readAgent()
        

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

    def inputAgent() :
        return 1

    def generateAgent() :
        return 1
    
    def readAgent():
        return 1

    def updateHabits():
        habits = open("habits.txt","a")
        with open("result.txt","r") as result:
            res = result.readlines()

        habits.write(res[1]+" ")

        for bool in CONTEXTBOOLS:
            habits.write(bool + " ")

        habits.close()

    


