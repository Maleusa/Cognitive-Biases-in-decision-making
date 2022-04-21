from ast import walk
from tkinter.filedialog import Open
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
    habits = []
    habiChoice= str #choix habituel de l'user
    gasPrice=float
    subPrice=float
    ratioCycleWay=float
    busFrequency=int
    busCapacity=int
    carSpeed=int
    bikeSpeed=int
    walkSpeed=int
    busSpeed=int
    env=environnement
    ##Initialisation de l'utilsateur avec trois choix 

    def __init__(self,) -> None:

        ##initialisation de l'environnement de l'agent 
        self.env = environnement()

        ##Initialisation des notes attribué aux différents critères de choix en fonctions des moyens des transports 
        self.dico = self.env.marks
        

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
            self.fitness=float(f[11])
        ##Initialisation des habitudes
        y= input("Do you want to use the (h)abits file as is,(e)rase it or erase it and create a (s)et of habits ? :")
        while y not in ["h","e","s"] :
            y= input("Do you want to use the (h)abits file as is,(e)rase it or erase it and create a (s)et of habits ? :")
        #On efface le fichier habits.txt
        if y=="e":
            self.refreshHabits()
        
        if y=="s":
            self.refreshHabits()
            z=input("Do you want to (r)andomize a certain number of habits or (e)nter them by hand ? : ")
            while z not in ["r","e"]:
                z=input("Do you want to (r)andomize a certain number of habits or (e)nter them by hand ? : ")
            h=int(input ("How many habits would you like to create ? :"))
            
            if z=="r":
                
                for i in range(h):
                    habits = open("habits.txt","a")
                    n=random.randint(0,3)
                    habits.write(LISTMODES[n]+" ")
                    for j in range(3) :
                        random_bit = random.getrandbits(1)
                        habits.write(str(bool(random_bit))+" ")
                    habits.write("\n")
            if z=="e":
                for i in range(h):
                    m=input("Did i use a (0)bike, (1)car, (2)bus or did i (3)walk ? : ")
                    while m not in ["0","1","2","3"]:
                        m=input("Did i use a (0)bike, (1)car, (2)bus or did i (3)walk ? : ")
                    habits = open("habits.txt","a")
                    habits.write(LISTMODES[int(m)]+" ")
                    cpt = 0 
                    RAINY = "rainy"
                    TEMPOK = "temperature ok"
                    LIGHT = "light"
                    CONTEXTBOOLS = [RAINY,TEMPOK,LIGHT]
                    for elem in CONTEXTBOOLS:
                        answer = input(elem + " ? (y/n) : ")
                        while answer not in ["y","n"]:
                            answer = input(elem + " ? (y/n) : ")
                        CONTEXTBOOLS[cpt] = (answer == "y")
                        cpt += 1
                    for bool in CONTEXTBOOLS:
                        habits.write(str(bool) + " ")
                    habits.write('\n')



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
            if (choice==CAR and self.means[1]==False) or (choice==BUS and self.means[2]==False) or (choice==BIKE and self.means[0]==False) or  (choice==WALK and self.fitness<=10):
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

    #fonction de choix habituel 
    def habitualChoice(self):
        self.readHabits()
        weightMod=[0,0,0,0]
        cont=""                    
        for bool in self.env.CONTEXTBOOLS:
            cont=cont+str(bool)+" "        #Initialisation du context actuelle
            
        
        for lines in range(len(self.habits)) : #Initialisation du tableau weightMod qui determine combien de fois on as fait le choix n sit les circonstances étaient similiares
             print(self.habits[lines].split(' ', 1)[1])
             if self.habits[lines].split(' ', 1)[1] == cont :
                 if self.habits[lines].split(' ', 1)[0] == "bike" :
                     weightMod[0]=weightMod[0]+1
                 if self.habits[lines].split(' ', 1)[0] == "car" :
                     weightMod[1]=weightMod[1]+1
                 if self.habits[lines].split(' ', 1)[0] == "bus" :
                     weightMod[2]=weightMod[2]+1
                 if self.habits[lines].split(' ', 1)[0] == "walk" :
                     weightMod[3]=weightMod[3]+1
        totweight=weightMod[0]+weightMod[1]+weightMod[2]+weightMod[3]
        print(weightMod)
        if totweight==0:
            print("I have no usual behavior for this specific environement")
            return
        for i in range(len(weightMod)):
            weightMod[i]=weightMod[i]/totweight

        for i in {1,2,3}: 
            weightMod[i]=weightMod[i]+weightMod[i-1]

        rand=float(random.randint(0,100)/100)

        #Ca marche
        print(len(weightMod))

        for i in range(len(weightMod)):
            print(rand)
            if rand<weightMod[i]:
                choice=LISTMODES[i]
                print(choice)
                self.habiChoice=choice
                break
            
        #test print(self.habiChoice)
        print("In the contexte that i am in if i follow my usual behavior i will choose "+self.habiChoice+" as a mode of transportation")
        # si jamais on veut ajouter le choix habituel self.updateHabits(self.habiChoice)
        

     



    #Fonction permettant d'effacer le contenu du fichier habits.txt et donc de d'oublier l'ensemble des abitudes de l'agent
    def refreshHabits(self):
        habits = open("habits.txt","w")
        habits.flush()


    #Fonction permttant de mettre à jour les abitudes de l'agent en ajoutant le choix du dernier trajet réalisé 
    def updateHabits(self,choice=str):
        
        habits = open("habits.txt","a")
        
       

        habits.write(choice+" ")

        for bool in self.env.CONTEXTBOOLS:
            habits.write(str(bool) + " ")
        
        habits.write('\n')

        habits.close()

    #Fonction de lecture du fichier d'habitude (ca marche)
    def readHabits(self):
        habits = open("habits.txt","r")
        f=habits.readlines()
        for lines in range(len(f)) :
            f[lines]=f[lines].strip('\n')
            
       
        self.habits=f

    #Fonction permettant d'écrir dans un fichier le choix du moyen de transport avec et sans biais
    def result(self):
        
        res = open("result.txt","w")
        res.write("Trouvez ci-dessous le moyen de transport choisi avec l'effet des biais\n"+"car(PROVISOIRE) \n")
        res.write("Trouvez ci-dessous le moyen de transport choisi de façon rationnelle\n"+"car(PROVISOIR) \n")
        res.close()


