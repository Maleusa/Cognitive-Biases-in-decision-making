from ast import walk
from re import L
from math import *
from typing import Iterable
import random

# transportation modes
BIKE = "bike"
CAR = "individual car"
BUS = "public transport"
WALK = "walk"
LISTMODES = [BIKE,CAR,BUS,WALK]

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
    mark = LISTMODES

    
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


        ###Initialisation d'un agent par input via la console 
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
        #Initialisation d'un agent par le hasard   
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
        #initialisation d'un agent en lisant un fichier
        if x=="f":
            agent=open("Agent.txt","r")
            f=agent.readlines()
            for lines in range(len(f)):
                f[lines]=f[lines].strip('\n')
            # ceci etait un test print(f)
            cpt=0
            for crit in CRITERIAS:
                self.critAgent[cpt]=float(f[cpt])
                cpt+=1
            cpt=0
            for agtbool in AGENTBOOLS:
                if(f[cpt+7]=="True") : self.means[cpt]=True
                else: self.means[cpt]=False
                cpt+=1
            self.fitness=int(f[11])

            
        
        


         
    def saveAgent(self):
        agent = open("Agent.txt","w")
        for crit in self.critAgent:
            agent.write(str(crit)+"\n")
        agent.write("\n")
        for bool in self.means:
            agent.write(str(bool)+"\n")
        agent.write("\n"+str(self.fitness))

    #Methode retournant le choix rationel d'un agent
    def rationalModeChoice(self):
        
        dico={}
        for mode in LISTMODES:
            dico[mode] = {}
            for crit in CRITERIAS:
                dico[mode][crit]=0
        #Remplissage du dictionnaire des valeurs associé à chaque critere pour chaque mode de transport
        dico[BIKE][ECOLOGY] = 1
        dico[BIKE][COMFORT] = 0
        dico[BIKE][CHEAP] = 0
        dico[BIKE][SAFETY] = 0
        dico[BIKE][PRATICITY] = 0
        dico[BIKE][FAST] = 0
        dico[CAR][ECOLOGY] = 1
        dico[CAR][COMFORT] = 0
        dico[CAR][CHEAP] = 0
        dico[CAR][SAFETY] = 0
        dico[CAR][PRATICITY] = 0
        dico[CAR][FAST] = 0
        dico[BUS][ECOLOGY] = 1
        dico[BUS][COMFORT] = 0
        dico[BUS][CHEAP] = 0
        dico[BUS][SAFETY] = 0
        dico[BUS][PRATICITY] = 0
        dico[BUS][FAST] = 0
        dico[WALK][ECOLOGY] = 1
        dico[WALK][COMFORT] = 0
        dico[WALK][CHEAP] = 0
        dico[WALK][SAFETY] = 0
        dico[WALK][PRATICITY] = 0
        dico[WALK][FAST] = 0
        #notation de chacun des modes de transport en fonction de l'evaluation de chaque mode
        i=0
        for mode in LISTMODES:
            self.mark[i]=0
            for crit in CRITERIAS:
                self.mark[i]=self.mark[i]+(dico[mode][crit]*self.critAgent[i])
            i=+1
        #TODO Sortir la note la plus haute et c'est elle qui indique le mode choisis rationement
        modefavoris = BIKE
        sortedmark=self.mark.copy()
        sortedmark.sort()
        indice=self.mark.index(sortedmark[23])
        if (indice>=0 & indice<=5):
            return BIKE
        else :
            if (indice >5 & indice <=11):
                return CAR
            if (indice >11 & indice <=17):
                return WALK
            if (indice >17 ):
                return BUS



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


