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

## Variables représentants le context
RAINY = "rainy"
TEMPOK = "temperature ok"
LIGHT = "light"
CONTEXTBOOLS = [RAINY,TEMPOK,LIGHT]


## Variables représentants les moyens de transports à disposition de l'agent
HASBIKE = "agent has bike"
HASCAR = "agent has car"
HASBUS = "agent is on bus line"
AGENTBOOLS = [HASBIKE, HASCAR, HASBUS]

FITNESS = "agent's fitness level"


class user:

    ##
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

        ##initialisation de la météo
        cpt = 0 
        for elem in CONTEXTBOOLS:
            answer = input(elem + " ? (y/n) : ")
            while answer not in ["y","n"]:
                answer = input(elem + " ? (y/n) : ")
            self.weather[cpt] = (answer == "y")
            cpt += 1
        

        ##Initialisation des poids associés aux différents critères de choix
        x = input("(r)andom agent priorities or (u)ser input or (f)ile input? : ")
        while x not in ["u","r","f"]:
            x = input("(u)ser agent priorities or (r)andom ? : ")
        if x == "u": 
            cpt=0
            for crit in CRITERIAS :
                
                x = float(input("Priority (0-1) of " + crit + " ? : "))
                
                while x<0 or x>1:
                    x = float(input("Priority (0-1) of "+crit+" ? : "))		
                self.critAgent[cpt] = x
                cpt += 1

                
                



            cpt=0
        ##Initialisation des poids associés aux différents critères de choix
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


    ##Fonction permettant d'effacer le contenu du fichier habits.txt et donc de d'oublier l'ensemble des abitudes de l'agent
    def refreshHabits(self):
        habits = open("habits.txt","w")
        habits.flush()


    ##Fonction permttant de mettre à jour les abitudes de l'agent en ajoutant le choix du dernier trajet réalisé 
    def updateHabits(self):
        
        habits = open("habits.txt","a")
        
        with open("result.txt","r") as result:
            
            print(result)
            res = result.readlines()
            print(res)

        habits.write(res[1]+" ")

        for bool in self.weather:
            habits.write(str(bool) + " ")
        
        habits.write('\n')

        habits.close()


    #Fonction permettant d'écrir dans un fichier le choix du moyen de transport avec et sans biais
    def result(self):
        res = open("result.txt","w")
        res.write("Trouvez ci-dessous le moyen de transport choisi avec l'effet des biais\n"+"car(PROVISOIRE) \n")
        res.write("Trouvez ci-dessous le moyen de transport choisi de façon rationnelle\n"+"car(PROVISOIR) \n")
        res.close()


