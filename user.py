from re import L
from math import *
from typing import Iterable
import random

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



HASBIKE = "agent has bike"
HASCAR = "agent has car"
HASBUS = "agent is on bus line"
AGENTBOOLS = [HASBIKE, HASCAR, HASBUS]
FITNESS = "agent's fitness level"


class user:
    fitness=float
    means=AGENTBOOLS
    critAgent=CRITERIAS
    weather = CONTEXTBOOLS

    
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
        ##initialisation provisoire de contextebools ###############################################
        for bool in self.weather:
            bool = True
        ############################################################################################


        x = input("(r)andom agent priorities or (u)ser input or (f)ile input? : ")
        while x not in ["u","r","f"]:
            x = input("(u)ser agent priorities or (r)andom ? : ")
        if x == "u": 
            cpt=0
            for crit in CRITERIAS :
                
                x = float(input("Priority (0-1) of " + crit + " ? : "))
                
                while x<0 or x>1:
                    x = float(input("Priority (0-1) of "+crit+" ? : "))
		# priority within 0-1
                self.critAgent[cpt] = x
                cpt += 1

                
                



            cpt=0
            for agtbool in AGENTBOOLS:
                x= (input("Do i own a "+agtbool+"? : (y)/(n)"))
                while x not in ["y","n"]:
                    x= (input("Do i own a "+agtbool+"? : (y)/(n)"))
                if x == "y": 
                    self.means[cpt]=True
                    cpt+=1
                else :
                    self.means[cpt]=False
                    cpt+=1

            x=float(input("Am i fit on a scale from 0 to 100 ? :"))
            while x<0 or x>100:
                x=float(input("Am i fit on a scale from 0 to 100 ? :"))
        
            self.fitness=x
            self.saveAgent()
        if x=="r" : 
            cpt=0
            for crit in CRITERIAS:
                self.critAgent[cpt]=random.random()
                cpt+=1
            cpt=0
            for agtbool in AGENTBOOLS:
                self.means[cpt]=random.choice([True,False])
                cpt+=1
            self.fitness=random.randint(0,100)
            self.saveAgent()
        if x=="f":
            agent=open("Agent.txt","r")
            cpt=0
            for crit in CRITERIAS:
                self.critAgent[cpt]=float(agent.readline(cpt+1))
                cpt+=1
            cpt=0
            for agtbool in AGENTBOOLS:
                if(agent.readline(cpt+8)=="True") : self.means[cpt]=True
                else: self.means[cpt]=False
                cpt+=1
            self.fitness=int(agent.readline(12))

            
        
        

        

      

         
    def saveAgent(self):
        agent = open("Agent.txt","w")
        for crit in self.critAgent:
            agent.write(str(crit)+"\n")
        agent.write("\n")
        for bool in self.means:
            agent.write(str(bool)+"\n")
        agent.write("\n"+str(self.fitness))

    def generateAgent() :
        return 1
    
    def readAgent():
        return 1


    def updateHabits(self):
        
        habits = open("habits.txt","a")
        
        with open("result.txt","r") as result:
            
            print(result)
            res = result.readlines()
            print(res)

        habits.write(res[1]+" ")

        for bool in self.weather:
            habits.write(bool + " ")
        
        habits.write('\n')

        habits.close()

    


