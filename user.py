from re import L
from math import *

##Critères permettant le choix du moyen de transport
ECOLOGY = "ecology"
COMFORT = "comfort"
CHEAP = "cheap"
SAFETY = "safety"
PRATICITY = "praticity"
FAST = "fast"
CRITERIAS = [ECOLOGY, COMFORT, CHEAP, SAFETY, PRATICITY, FAST]

## Varaibles représentant le context
RAINY = "rainy"
TEMPOK = "temperature ok"
LIGHT = "light"
CONTEXTBOOLS = [RAINY,TEMPOK,LIGHT]

##initialisation provisoire de contextebools ###############################################
for bool in CONTEXTBOOLS:
    bool = True
############################################################################################

HASBIKE = "agent has bike"
HASCAR = "agent has car"
HASBUS = "agent is on bus line"
AGENTBOOLS = [HASBIKE, HASCAR, HASBUS]
FITNESS = "agent's fitness level"


class user:
    fitness=float
    means=AGENTBOOLS
    critere=CRITERIAS
    gasPrice=float
    subPrice=float
    ratioCycleWay=float
    busFrequency=int
    busCapacity=int
    carSpeed=int
    bikeSpeed=int
    walkSpeed=int
    busSpeed=int
    ##Initialisation de l'utilsateur avec trois choix 
    def __init__(self,) -> None:
        x = input("(r)andom agent priorities or (u)ser input or (f)ile input? : ")
        while x not in ["u","r","f"]:
            x = input("(u)ser agent priorities or (r)andom ? : ")
        if x == "u": 
            for crit in CRITERIAS :
                x = float(input("Priority (0-1) of "+crit+" ? : "))
            while x<0 or x>1:
                x = float(input("Priority (0-1) of "+crit+" ? : "))
		# priority within 0-1
            self.critere[crit]=x
            for agtbool in [AGENTBOOLS]:
                x= (input("Do i own a "+AGENTBOOLS+"? : (y)/(n)"))
            while x not in ["y","n"]:
                x= (input("Do i own a "+AGENTBOOLS+"? : (y)/(n)"))
            if x == "y": self.means[agtbool]=True
            else :
                self.mens[agtbool]=False
            x=float(input("Am i fit on a scale from 0 to 100 ? :"))
            while x<0 or x>100:
                x=float(input("Am i fit on a scale from 0 to 100 ? :"))
        self.fitness=x
        if x=="r" : self.generateAgent(self)
        
        

        

      

         

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

    


