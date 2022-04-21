from ast import walk
from environnement import *
from pickletools import markobject
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

## Variables représentants les moyens de transports à disposition de l'agent
HASBIKE = "agent has bike"
HASCAR = "agent has car"
HASBUS = "agent is on bus line"
AGENTBOOLS = [HASBIKE, HASCAR, HASBUS]

FITNESS = "agent's fitness level"


class user:
    
  
    dico = dict      
    ##
    fitness=float
    means=AGENTBOOLS
    critAgent=CRITERIAS
    rationalChoice=str #choix rationnel de l'utilisateur
    mark = [0,0,0,0]
    habits=list
    
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

        ##initialisation de l'environnement de l'agent 
        env = environnement()

        ##Initialisation des notes attribué aux différents critères de choix en fonctions des moyens des transports 
        self.dico = env.getMarks()
        

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
                x= (input(agtbool+" ? : (y)/(n) "))
                while x not in ["y","n"]:
                    x= (input(agtbool+" ? : (y)/(n) "))
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

        # Mise à 0 des notes correspondants à des moyens de transport inaccessibles pour l'agent (changement de méthode pour le traitement des modes inaccessible)
        """if self.means[0]==False or self.fitness < 20:
            self.dico[BIKE][ECOLOGY] = 0
            self.dico[BIKE][COMFORT] = 0
            self.dico[BIKE][CHEAP] = 0
            self.dico[BIKE][SAFETY] = 0
            self.dico[BIKE][PRATICITY] = 0
            self.dico[BIKE][FAST] = 0

        if self.means[1]==False:
            self.dico[CAR][ECOLOGY] = 0
            self.dico[CAR][COMFORT] = 0
            self.dico[CAR][CHEAP] = 0
            self.dico[CAR][SAFETY] = 0
            self.dico[CAR][PRATICITY] = 0
            self.dico[CAR][FAST] = 0

        if self.means[2]==False:
            self.dico[BUS][ECOLOGY] = 0
            self.dico[BUS][COMFORT] = 0
            self.dico[BUS][CHEAP] = 0
            self.dico[BUS][SAFETY] = 0
            self.dico[BUS][PRATICITY] = 0
            self.dico[BUS][FAST] = 0

        if self.fitness < 10:
            self.dico[WALK][ECOLOGY] = 0
            self.dico[WALK][COMFORT] = 0
            self.dico[WALK][CHEAP] = 0
            self.dico[WALK][SAFETY] = 0
            self.dico[WALK][PRATICITY] = 0
            self.dico[WALK][FAST] = 0"""
        
        

        print(self.dico)



    #Fonction de sauvegarde de l'agent dans un fichier      
    def saveAgent(self):
        agent = open("Agent.txt","w")
        for crit in self.critAgent:
            agent.write(str(crit)+"\n")
        agent.write("\n")
        for bool in self.means:
            agent.write(str(bool)+"\n")
        agent.write("\n"+str(self.fitness))

    #Methode retournant le choix rationel d'un agent
    def rationalModeChoice(self,envir=environnement):
        
        
        #notation de chacun des modes de transport en fonction de l'evaluation de chaque mode
        i=0
        for p_id, p_info in envir.marks.items():
            
            j=0
            for key in p_info:
               
                self.mark[i]=self.mark[i]+(p_info[key]*self.critAgent[j])
                
                j+=1
            
            i=+1
        


        
        #TODO Sortir la note la plus haute et c'est elle qui indique le mode choisis rationement
        markmax = 0
        indexMarkMax = 0
        k=0

     
        for k in range(0,len(self.mark)):
            
            if (float(self.mark[k])>markmax) :
                # test print(str(self.mark[k]) + "ma note")
                markmax = float(self.mark[k])
                # test print(str(markmax) + "note max")
                indexMarkMax = k

        choice = LISTMODES[indexMarkMax]
        #on verifie que notre mode favoris nous est accessible et si ce n'est pas le cas on prends le suivant dans la liste 
        n=4
        while n>0:
            if (choice==CAR & self.means[1]==False) or (choice==BUS & self.means[2]==False) or (choice==BIKE & self.means[0]==False) or  (choice==WALK & self.fitness<=10):
                print("I'd like to use  "+choice+" transport mode, but it is currently unaivalable to me.")
                self.mark[indexMarkMax]=0
                markmax = 0
                indexMarkMax = 0
                k=0

     
                for k in range(0,len(self.mark)):
            
                    if (float(self.mark[k])>markmax) :
                        print(str(self.mark[k]) + "ma note")
                        markmax = float(self.mark[k])
                        print(str(markmax) + "note max")
                        indexMarkMax = k
            n=-1

        choice = LISTMODES[indexMarkMax]

        print("If i was a rationnal agent i would have chosen"+choice+" has a mode of transportation.")
        self.rationalChoice=choice
        


     



    #Fonction permettant d'effacer le contenu du fichier habits.txt et donc de d'oublier l'ensemble des abitudes de l'agent
    def refreshHabits(self):
        habits = open("habits.txt","w")
        habits.flush()


    #Fonction permttant de mettre à jour les abitudes de l'agent en ajoutant le choix du dernier trajet réalisé 
    def updateHabits(self,choice=str):
        
        habits = open("habits.txt","a")
        
       

        habits.write(choice+" ")

        for bool in self.weather:
            habits.write(str(bool) + " ")
        
        habits.write('\n')

        habits.close()

    #Fonction de lecture du fichier d'habitude 
    def readHabits(self):
        habits = open("habits.txt","r")
        f=habits.readlines()
        for lines in range(len(f)) :
            f[lines]=f[lines].strip('\n')

    #Fonction permettant d'écrir dans un fichier le choix du moyen de transport avec et sans biais
    def result(self):
        res = open("result.txt","w")
        res.write("Trouvez ci-dessous le moyen de transport choisi avec l'effet des biais\n"+"car(PROVISOIRE) \n")
        res.write("Trouvez ci-dessous le moyen de transport choisi de façon rationnelle\n"+"car(PROVISOIR) \n")
        res.close()


