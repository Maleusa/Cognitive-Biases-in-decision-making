from fcntl import DN_DELETE
from environnement import *
from pickletools import markobject
from re import A, L
from math import *
from typing import Iterable
import random

# transportation modes
BIKE = "bike"
CAR = "car"
BUS = "publictransport"
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
    
    ident=int
    dico = dict
    biasMarks =dict    
    ##
    biasChoise=str #choix biaisé de l'utilisateur
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
    # Initialisation de l'utilsateur avec trois choix 

    def __init__(self,envir=environnement) -> None:
        #copie du table des notes "objectives" dans le tableau bias Marks
        self.biasMarks=envir.marks
        #initialisation de l'identifiant de l'agent
        self.ident=random.randint(0,100)
        # initialisation de l'environnement de l'agent 
        env = envir

        # Initialisation des notes attribué aux différents critères de choix en fonctions des moyens des transports 
        self.dico = env.marks
        

        # Initialisation des poids associés aux différents critères de choix
        x = input("(r)andom agent priorities or (u)ser input or (f)ile input? : ")
        while x not in ["u","r","f"]:
            x = input("(u)ser agent priorities or (r)andom ? : ")


        # Initialisation d'un agent par input via la console 
        if x == "u": 
            
            cpt=0
            for crit in CRITERIAS :
                
                x = float(input("Priority (0-1) of " + crit + " ? : "))
                
                while x<0 or x>1:
                    x = float(input("Priority (0-1) of "+crit+" ? : "))		
                self.critAgent[cpt] = x
                cpt += 1



            cpt=0
            # Initialisation des poids associés aux différents critères de choix
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

        # Initialisation d'un agent par le hasard   
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

        # Initialisation d'un agent en lisant un fichier
        if x=="f":
            id=int(input("Please input the agent number between 0 and 100"))
            while id<0 or id>100:
                id=int(input("Please input the agent number between 0 and 100"))
            self.ident=id
            agent=open("Agent"+str(id)+".txt","r")
            f=agent.readlines()
            for lines in range(len(f)):
                f[lines]=f[lines].strip('\n')
            # Ceci etait un test print(f)
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
                    habits = open("habits"+str(self.ident)+".txt","a")
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
                    for boole in CONTEXTBOOLS:
                        habits.write(str(boole) + " ")
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



    # Fonction de sauvegarde de l'agent dans un fichier      
    def saveAgent(self):
        agent = open("Agent"+str(self.ident)+".txt","w")
        for crit in self.critAgent:
            agent.write(str(crit)+"\n")
        agent.write("\n")
        for bool in self.means:
            agent.write(str(bool)+"\n")
        agent.write("\n"+str(self.fitness))

    # Methode retournant le choix rationel d'un agent
    def rationalModeChoice(self,envir=environnement):
        
        
        # Notation de chacun des modes de transport en fonction de l'evaluation de chaque mode
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
                # Test print(str(self.mark[k]) + "ma note")
                markmax = float(self.mark[k])
                # Test print(str(markmax) + "note max")
                indexMarkMax = k

        choice = LISTMODES[indexMarkMax]

        # On verifie que notre mode favoris nous est accessible et si ce n'est pas le cas on prends le suivant dans la liste 
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

        print("If i was a rationnal agent i would have chosen "+choice+" has a mode of transportation.")
        self.rationalChoice=choice

    # Fonction de choix habituel 
    def habitualChoice(self):
        self.readHabits()
        weightMod=[0,0,0,0]
        cont=""                    
        for bool in self.env.CONTEXTBOOLS:
            cont=cont+str(bool)+" "        # Initialisation du context actuelle
            
        
        for lines in range(len(self.habits)) : # Initialisation du tableau weightMod qui determine combien de fois on as fait le choix n sit les circonstances étaient similiares
             print(self.habits[lines].split(' ', 1)[1])
             if self.habits[lines].split(' ', 1)[1] == cont :
                 if self.habits[lines].split(' ', 1)[0] == BIKE :
                     weightMod[0]=weightMod[0]+1
                 if self.habits[lines].split(' ', 1)[0] == CAR :
                     weightMod[1]=weightMod[1]+1
                 if self.habits[lines].split(' ', 1)[0] == BUS:
                     weightMod[2]=weightMod[2]+1
                 if self.habits[lines].split(' ', 1)[0] == WALK:
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
        

     



    # Fonction permettant d'effacer le contenu du fichier habits.txt et donc de d'oublier l'ensemble des abitudes de l'agent
    def refreshHabits(self):
        habits = open("habits"+str(self.ident)+".txt","w")
        habits.flush()


    # Fonction permttant de mettre à jour les abitudes de l'agent en ajoutant le choix du dernier trajet réalisé 
    def updateHabits(self,choice=str):
        
        habits = open("habits"+str(self.ident)+".txt","a")
        
       

        habits.write(choice+" ")

        for bool in self.env.CONTEXTBOOLS:
            habits.write(str(bool) + " ")
        
        habits.write('\n')

        habits.close()

    # Fonction de lecture du fichier d'habitude (ca marche)
    def readHabits(self):
        habits = open("habits"+str(self.ident)+".txt","r")
        f=habits.readlines()
        for lines in range(len(f)) :
            f[lines]=f[lines].strip('\n')
            
       
        self.habits=f

    # Fonction permettant d'écrir dans un fichier le choix du moyen de transport avec et sans biais
    def result(self,env=environnement):
        
        res = open("Result"+str(self.ident)+".txt","a")
        res.write("Environemental conditions : \n Rainy : "+str(env.CONTEXTBOOLS[0])+" Good temperature : "+str(env.CONTEXTBOOLS[1])+ " Presence of light : "+str(env.CONTEXTBOOLS[2])+"\n gasPrice= "+str(env.gasPrice)+"Public Transport Price:"+str(env.subPrice)+" ratioCycleWay : "+str(env.ratioCycleWay)+"Bus frequency : "+str(env.busFrequency)+"Bus Speed : "+str(env.busSpeed)+"Bus Capacity : "+str(env.busCapacity)+"Car speed : "+str(env.carSpeed)+"Cycle Speed : "+str(env.bikeSpeed)+"Walk speed : "+str(env.walkSpeed)+"\n")
        res.write("Habitual choice : "+self.habiChoice+"\n")
        res.write("Rationnal choice : "+self.rationalChoice+"\n")
        res.write("Biased choice : "+ self.biasChoise+"\n \n")
        res.close()

    #Ici les biais

    def biasedResults(self,envir=environnement):
        self.rationalModeChoice()
        self.habitualChoice()
        aForbid=False
        aConf=False
        aEst=False
        x=input("Do you wish to use confirmation bias / reactance in decision making (y/n) ? :")
        while x not in ["y","n"] :
            x=input("Do you wish to use confirmation bias / reactance in decision making (y/n) ? :")
        y=input("Do you wish to use under/over estimation in decision making (y/n) ? :")
        while y not in ["y","n"] :
            y=input("Do you wish to use under/over estimation in decision making (y/n) ? :")
        z=input("Do you wish to use the forbidden behavior paradigme in decision making (y)/(n) ? : ")
        while z not in ["y","n"] :
            z=input("Do you wish to use the forbidden behavior paradigme in decision making (y)/(n) ? : ")
        if z=="y":
            aForbid=True
        if x=="y":
            aConf=True
        if y=="y":
            aEst=True
        
        #TODO Maths des deux biais en modifian les valeurs soit de nos preference (forbidden behavior paradigme), soit de nos notes biaisé pour les autres dans le dict self.biasMarks 
        if aConf==True:
            #TODO faire un test pour determiner si on utilise le biais de confirmation ou la reactance

            #Confirmation en dessous
            if self.habiChoice==BIKE :
                self.biasMarks[BIKE][ECOLOGY] = envir.marks[BIKE][ECOLOGY]
                self.biasMarks[BIKE][COMFORT] = envir.marks[BIKE][COMFORT]
                self.biasMarks[BIKE][CHEAP] = envir.marks[BIKE][CHEAP]
                self.biasMarks[BIKE][SAFETY] = envir.marks[BIKE][SAFETY]
                self.biasMarks[BIKE][PRATICITY] = envir.marks[BIKE][PRATICITY]
                self.biasMarks[BIKE][FAST] = envir.marks[BIKE][FAST]
                self.biasMarks[CAR][ECOLOGY] = envir.marks[CAR][ECOLOGY] - random.normalvariate((envir.marks[CAR][ECOLOGY]/2),(envir.marks[CAR][ECOLOGY]/4)) #Ici on genere du bruit avec un float entre 0 et la valeur objective de la note selon une repartition normal avec pour moyenne note/2 et et note/4 (estimation a la louche)
                self.biasMarks[CAR][COMFORT] = envir.marks[CAR][COMFORT] -random.normalvariate((envir.marks[CAR][COMFORT]/2),(envir.marks[CAR][COMFORT] /4))
                self.biasMarks[CAR][CHEAP] = envir.marks[CAR][CHEAP] - random.normalvariate((envir.marks[CAR][CHEAP]/2),(envir.marks[CAR][CHEAP]/4))
                self.biasMarks[CAR][SAFETY] = envir.marks[CAR][SAFETY]- random.normalvariate((envir.marks[CAR][SAFETY]/2),(envir.marks[CAR][SAFETY]/4))
                self.biasMarks[CAR][PRATICITY] = envir.marks[CAR][PRATICITY] - random.normalvariate((envir.marks[CAR][PRATICITY]/2),(envir.marks[CAR][PRATICITY]/4))
                self.biasMarks[CAR][FAST] = envir.marks[CAR][FAST] - random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4))
                self.biasMarks[BUS][ECOLOGY] = envir.marks[BUS][ECOLOGY] - random.normalvariate((envir.marks[BUS][ECOLOGY]/2),(envir.marks[BUS][ECOLOGY]/4))
                self.biasMarks[BUS][COMFORT] = envir.marks[BUS][COMFORT] - random.normalvariate((envir.marks[BUS][COMFORT]/2),(envir.marks[BUS][COMFORT]/4))
                self.biasMarks[BUS][CHEAP] = envir.marks[BUS][CHEAP]
                self.biasMarks[BUS][SAFETY] = envir.marks[BUS][SAFETY]
                self.biasMarks[BUS][PRATICITY] = envir.marks[BUS][PRATICITY] - random.normalvariate((envir.marks[BUS][PRATICITY]/2 ),(envir.marks[BUS][PRATICITY]/4 ))
                self.biasMarks[BUS][FAST] = envir.marks[BUS][FAST] - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4))
                self.biasMarks[WALK][ECOLOGY] = envir.marks[WALK][ECOLOGY] 
                self.biasMarks[WALK][COMFORT] = envir.marks[WALK][COMFORT] -random.normalvariate((envir.marks[WALK][COMFORT]/2),(envir.marks[WALK][COMFORT]/4))
                self.biasMarks[WALK][CHEAP] = envir.marks[WALK][CHEAP]
                self.biasMarks[WALK][SAFETY] = envir.marks[WALK][SAFETY]
                self.biasMarks[WALK][PRATICITY] = envir.marks[WALK][PRATICITY] - random.normalvariate((envir.marks[WALK][PRATICITY]/2),(envir.marks[WALK][PRATICITY]/4))
                self.biasMarks[WALK][FAST] = envir.marks[WALK][FAST] - random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/4))
            #TODO
            if self.habiChoice==CAR :
                self.biasMarks[BIKE][ECOLOGY] = envir.marks[BIKE][ECOLOGY]
                self.biasMarks[BIKE][COMFORT] = envir.marks[BIKE][COMFORT]
                self.biasMarks[BIKE][CHEAP] = envir.marks[BIKE][CHEAP]
                self.biasMarks[BIKE][SAFETY] = envir.marks[BIKE][SAFETY]
                self.biasMarks[BIKE][PRATICITY] = envir.marks[BIKE][PRATICITY]
                self.biasMarks[BIKE][FAST] = envir.marks[BIKE][FAST]
                self.biasMarks[CAR][ECOLOGY] = envir.marks[CAR][ECOLOGY] - random.normalvariate((envir.marks[CAR][ECOLOGY]/2),(envir.marks[CAR][ECOLOGY]/4)) #Ici on genere du bruit avec un float entre 0 et la valeur objective de la note selon une repartition normal avec pour moyenne note/2 et et note/4 (estimation a la louche)
                self.biasMarks[CAR][COMFORT] = envir.marks[CAR][COMFORT] -random.normalvariate((envir.marks[CAR][COMFORT]/2),(envir.marks[CAR][COMFORT] /4))
                self.biasMarks[CAR][CHEAP] = envir.marks[CAR][CHEAP] - random.normalvariate((envir.marks[CAR][CHEAP]/2),(envir.marks[CAR][CHEAP]/4))
                self.biasMarks[CAR][SAFETY] = envir.marks[CAR][SAFETY]- random.normalvariate((envir.marks[CAR][SAFETY]/2),(envir.marks[CAR][SAFETY]/4))
                self.biasMarks[CAR][PRATICITY] = envir.marks[CAR][PRATICITY] - random.normalvariate((envir.marks[CAR][PRATICITY]/2),(envir.marks[CAR][PRATICITY]/4))
                self.biasMarks[CAR][FAST] = envir.marks[CAR][FAST] - random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4))
                self.biasMarks[BUS][ECOLOGY] = envir.marks[BUS][ECOLOGY] - random.normalvariate((envir.marks[BUS][ECOLOGY]/2),(envir.marks[BUS][ECOLOGY]/4))
                self.biasMarks[BUS][COMFORT] = envir.marks[BUS][COMFORT] - random.normalvariate((envir.marks[BUS][COMFORT]/2),(envir.marks[BUS][COMFORT]/4))
                self.biasMarks[BUS][CHEAP] = envir.marks[BUS][CHEAP]
                self.biasMarks[BUS][SAFETY] = envir.marks[BUS][SAFETY]
                self.biasMarks[BUS][PRATICITY] = envir.marks[BUS][PRATICITY] - random.normalvariate((envir.marks[BUS][PRATICITY]/2 ),(envir.marks[BUS][PRATICITY]/4 ))
                self.biasMarks[BUS][FAST] = envir.marks[BUS][FAST] - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4))
                self.biasMarks[WALK][ECOLOGY] = envir.marks[WALK][ECOLOGY] 
                self.biasMarks[WALK][COMFORT] = envir.marks[WALK][COMFORT] -random.normalvariate((envir.marks[WALK][COMFORT]/2),(envir.marks[WALK][COMFORT]/4))
                self.biasMarks[WALK][CHEAP] = envir.marks[WALK][CHEAP]
                self.biasMarks[WALK][SAFETY] = envir.marks[WALK][SAFETY]
                self.biasMarks[WALK][PRATICITY] = envir.marks[WALK][PRATICITY] - random.normalvariate((envir.marks[WALK][PRATICITY]/2),(envir.marks[WALK][PRATICITY]/4))
                self.biasMarks[WALK][FAST] = envir.marks[WALK][FAST] - random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/4))
            #TODO
            if self.habiChoice==BUS :
                self.biasMarks[BIKE][ECOLOGY] = envir.marks[BIKE][ECOLOGY]
                self.biasMarks[BIKE][COMFORT] = envir.marks[BIKE][COMFORT]
                self.biasMarks[BIKE][CHEAP] = envir.marks[BIKE][CHEAP]
                self.biasMarks[BIKE][SAFETY] = envir.marks[BIKE][SAFETY]
                self.biasMarks[BIKE][PRATICITY] = envir.marks[BIKE][PRATICITY]
                self.biasMarks[BIKE][FAST] = envir.marks[BIKE][FAST]
                self.biasMarks[CAR][ECOLOGY] = envir.marks[CAR][ECOLOGY] - random.normalvariate((envir.marks[CAR][ECOLOGY]/2),(envir.marks[CAR][ECOLOGY]/4)) #Ici on genere du bruit avec un float entre 0 et la valeur objective de la note selon une repartition normal avec pour moyenne note/2 et et note/4 (estimation a la louche)
                self.biasMarks[CAR][COMFORT] = envir.marks[CAR][COMFORT] -random.normalvariate((envir.marks[CAR][COMFORT]/2),(envir.marks[CAR][COMFORT] /4))
                self.biasMarks[CAR][CHEAP] = envir.marks[CAR][CHEAP] - random.normalvariate((envir.marks[CAR][CHEAP]/2),(envir.marks[CAR][CHEAP]/4))
                self.biasMarks[CAR][SAFETY] = envir.marks[CAR][SAFETY]- random.normalvariate((envir.marks[CAR][SAFETY]/2),(envir.marks[CAR][SAFETY]/4))
                self.biasMarks[CAR][PRATICITY] = envir.marks[CAR][PRATICITY] - random.normalvariate((envir.marks[CAR][PRATICITY]/2),(envir.marks[CAR][PRATICITY]/4))
                self.biasMarks[CAR][FAST] = envir.marks[CAR][FAST] - random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4))
                self.biasMarks[BUS][ECOLOGY] = envir.marks[BUS][ECOLOGY] - random.normalvariate((envir.marks[BUS][ECOLOGY]/2),(envir.marks[BUS][ECOLOGY]/4))
                self.biasMarks[BUS][COMFORT] = envir.marks[BUS][COMFORT] - random.normalvariate((envir.marks[BUS][COMFORT]/2),(envir.marks[BUS][COMFORT]/4))
                self.biasMarks[BUS][CHEAP] = envir.marks[BUS][CHEAP]
                self.biasMarks[BUS][SAFETY] = envir.marks[BUS][SAFETY]
                self.biasMarks[BUS][PRATICITY] = envir.marks[BUS][PRATICITY] - random.normalvariate((envir.marks[BUS][PRATICITY]/2 ),(envir.marks[BUS][PRATICITY]/4 ))
                self.biasMarks[BUS][FAST] = envir.marks[BUS][FAST] - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4))
                self.biasMarks[WALK][ECOLOGY] = envir.marks[WALK][ECOLOGY] 
                self.biasMarks[WALK][COMFORT] = envir.marks[WALK][COMFORT] -random.normalvariate((envir.marks[WALK][COMFORT]/2),(envir.marks[WALK][COMFORT]/4))
                self.biasMarks[WALK][CHEAP] = envir.marks[WALK][CHEAP]
                self.biasMarks[WALK][SAFETY] = envir.marks[WALK][SAFETY]
                self.biasMarks[WALK][PRATICITY] = envir.marks[WALK][PRATICITY] - random.normalvariate((envir.marks[WALK][PRATICITY]/2),(envir.marks[WALK][PRATICITY]/4))
                self.biasMarks[WALK][FAST] = envir.marks[WALK][FAST] - random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/4))
            #TODO
            if self.habiChoice==WALK :
                self.biasMarks[BIKE][ECOLOGY] = envir.marks[BIKE][ECOLOGY]
                self.biasMarks[BIKE][COMFORT] = envir.marks[BIKE][COMFORT]
                self.biasMarks[BIKE][CHEAP] = envir.marks[BIKE][CHEAP]
                self.biasMarks[BIKE][SAFETY] = envir.marks[BIKE][SAFETY]
                self.biasMarks[BIKE][PRATICITY] = envir.marks[BIKE][PRATICITY]
                self.biasMarks[BIKE][FAST] = envir.marks[BIKE][FAST]
                self.biasMarks[CAR][ECOLOGY] = envir.marks[CAR][ECOLOGY] - random.normalvariate((envir.marks[CAR][ECOLOGY]/2),(envir.marks[CAR][ECOLOGY]/4)) #Ici on genere du bruit avec un float entre 0 et la valeur objective de la note selon une repartition normal avec pour moyenne note/2 et et note/4 (estimation a la louche)
                self.biasMarks[CAR][COMFORT] = envir.marks[CAR][COMFORT] -random.normalvariate((envir.marks[CAR][COMFORT]/2),(envir.marks[CAR][COMFORT] /4))
                self.biasMarks[CAR][CHEAP] = envir.marks[CAR][CHEAP] - random.normalvariate((envir.marks[CAR][CHEAP]/2),(envir.marks[CAR][CHEAP]/4))
                self.biasMarks[CAR][SAFETY] = envir.marks[CAR][SAFETY]- random.normalvariate((envir.marks[CAR][SAFETY]/2),(envir.marks[CAR][SAFETY]/4))
                self.biasMarks[CAR][PRATICITY] = envir.marks[CAR][PRATICITY] - random.normalvariate((envir.marks[CAR][PRATICITY]/2),(envir.marks[CAR][PRATICITY]/4))
                self.biasMarks[CAR][FAST] = envir.marks[CAR][FAST] - random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4))
                self.biasMarks[BUS][ECOLOGY] = envir.marks[BUS][ECOLOGY] - random.normalvariate((envir.marks[BUS][ECOLOGY]/2),(envir.marks[BUS][ECOLOGY]/4))
                self.biasMarks[BUS][COMFORT] = envir.marks[BUS][COMFORT] - random.normalvariate((envir.marks[BUS][COMFORT]/2),(envir.marks[BUS][COMFORT]/4))
                self.biasMarks[BUS][CHEAP] = envir.marks[BUS][CHEAP]
                self.biasMarks[BUS][SAFETY] = envir.marks[BUS][SAFETY]
                self.biasMarks[BUS][PRATICITY] = envir.marks[BUS][PRATICITY] - random.normalvariate((envir.marks[BUS][PRATICITY]/2 ),(envir.marks[BUS][PRATICITY]/4 ))
                self.biasMarks[BUS][FAST] = envir.marks[BUS][FAST] - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4))
                self.biasMarks[WALK][ECOLOGY] = envir.marks[WALK][ECOLOGY] 
                self.biasMarks[WALK][COMFORT] = envir.marks[WALK][COMFORT] -random.normalvariate((envir.marks[WALK][COMFORT]/2),(envir.marks[WALK][COMFORT]/4))
                self.biasMarks[WALK][CHEAP] = envir.marks[WALK][CHEAP]
                self.biasMarks[WALK][SAFETY] = envir.marks[WALK][SAFETY]
                self.biasMarks[WALK][PRATICITY] = envir.marks[WALK][PRATICITY] - random.normalvariate((envir.marks[WALK][PRATICITY]/2),(envir.marks[WALK][PRATICITY]/4))
                self.biasMarks[WALK][FAST] = envir.marks[WALK][FAST] - random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/4))
        
        #Biais de sous/sur estimation seul (atm juste la distance peut etre ajouter le prix)
        if aEst==True and aConf==False:
            self.biasMarks[BIKE][ECOLOGY] = envir.marks[BIKE][ECOLOGY]
            self.biasMarks[BIKE][COMFORT] = envir.marks[BIKE][COMFORT]
            self.biasMarks[BIKE][CHEAP] = envir.marks[BIKE][CHEAP]
            self.biasMarks[BIKE][SAFETY] = envir.marks[BIKE][SAFETY]
            self.biasMarks[BIKE][PRATICITY] = envir.marks[BIKE][PRATICITY]
            self.biasMarks[BIKE][FAST] = envir.marks[BIKE][FAST]
            self.biasMarks[CAR][ECOLOGY] = envir.marks[CAR][ECOLOGY] 
            self.biasMarks[CAR][COMFORT] = envir.marks[CAR][COMFORT] 
            self.biasMarks[CAR][CHEAP] = envir.marks[CAR][CHEAP] 
            self.biasMarks[CAR][SAFETY] = envir.marks[CAR][SAFETY]
            self.biasMarks[CAR][PRATICITY] = envir.marks[CAR][PRATICITY] 
            self.biasMarks[CAR][FAST] = envir.marks[CAR][FAST] + random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4)) #sous estimation du temps en voiture
            self.biasMarks[BUS][ECOLOGY] = envir.marks[BUS][ECOLOGY] 
            self.biasMarks[BUS][COMFORT] = envir.marks[BUS][COMFORT] 
            self.biasMarks[BUS][CHEAP] = envir.marks[BUS][CHEAP]
            self.biasMarks[BUS][SAFETY] = envir.marks[BUS][SAFETY]
            self.biasMarks[BUS][PRATICITY] = envir.marks[BUS][PRATICITY] 
            self.biasMarks[BUS][FAST] = envir.marks[BUS][FAST] - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4)) #sur estimation du temps en transport en commun
            self.biasMarks[WALK][ECOLOGY] = envir.marks[WALK][ECOLOGY] 
            self.biasMarks[WALK][COMFORT] = envir.marks[WALK][COMFORT]
            self.biasMarks[WALK][CHEAP] = envir.marks[WALK][CHEAP]
            self.biasMarks[WALK][SAFETY] = envir.marks[WALK][SAFETY]
            self.biasMarks[WALK][PRATICITY] = envir.marks[WALK][PRATICITY] 
            self.biasMarks[WALK][FAST] = envir.marks[WALK][FAST] - random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/3)) #sur estimation du temps a pieds
        #Pareil qu'au dessus mais cette fois ci avec le biais de confirmation deja appliqué
        if aEst==True and aConf==True:
            self.biasMarks[BIKE][ECOLOGY] = self.biasMarks[BIKE][ECOLOGY]
            self.biasMarks[BIKE][COMFORT] = self.biasMarks[BIKE][COMFORT]
            self.biasMarks[BIKE][CHEAP] = self.biasMarks[BIKE][CHEAP]
            self.biasMarks[BIKE][SAFETY] = self.biasMarks[BIKE][SAFETY]
            self.biasMarks[BIKE][PRATICITY] = self.biasMarks[BIKE][PRATICITY]
            self.biasMarks[BIKE][FAST] = self.biasMarks[BIKE][FAST]
            self.biasMarks[CAR][ECOLOGY] = self.biasMarks[CAR][ECOLOGY] 
            self.biasMarks[CAR][COMFORT] = self.biasMarks[CAR][COMFORT] 
            self.biasMarks[CAR][CHEAP] = self.biasMarks[CAR][CHEAP] 
            self.biasMarks[CAR][SAFETY] = self.biasMarks[CAR][SAFETY]
            self.biasMarks[CAR][PRATICITY] = self.biasMarks[CAR][PRATICITY] 
            self.biasMarks[CAR][FAST] = self.biasMarks[CAR][FAST] + random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4)) #sous estimation du temps en voiture
            self.biasMarks[BUS][ECOLOGY] = self.biasMarks[BUS][ECOLOGY] 
            self.biasMarks[BUS][COMFORT] = self.biasMarks[BUS][COMFORT] 
            self.biasMarks[BUS][CHEAP] =self.biasMarks[BUS][CHEAP]
            self.biasMarks[BUS][SAFETY] = self.biasMarks[BUS][SAFETY]
            self.biasMarks[BUS][PRATICITY] = self.biasMarks[BUS][PRATICITY] 
            self.biasMarks[BUS][FAST] = self.biasMarks[BUS][FAST] - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4)) #sur estimation du temps en transport en commun
            self.biasMarks[WALK][ECOLOGY] = self.biasMarks[WALK][ECOLOGY] 
            self.biasMarks[WALK][COMFORT] = self.biasMarks[WALK][COMFORT]
            self.biasMarks[WALK][CHEAP] = self.biasMarks[WALK][CHEAP]
            self.biasMarks[WALK][SAFETY] = self.biasMarks[WALK][SAFETY]
            self.biasMarks[WALK][PRATICITY] = self.biasMarks[WALK][PRATICITY] 
            self.biasMarks[WALK][FAST] = self.biasMarks[WALK][FAST] - random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/3)) #sur estimation du temps a pieds
        #Application du biais forbidden choice TODO
        if aForbid==True:
            if self.habiChoice==BIKE:
                print()
            if self.habiChoice==CAR:
                print()
            if self.habiChoice==BUS:
                print()
            if self.habiChoice==WALK:
                print()

        # Notation de chacun des modes de transport en fonction de l'evaluation de chaque mode
        i=0
        for p_id, p_info in self.biasMarks.items():
            
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
                # Test print(str(self.mark[k]) + "ma note")
                markmax = float(self.mark[k])
                # Test print(str(markmax) + "note max")
                indexMarkMax = k

        choice = LISTMODES[indexMarkMax]

        # On verifie que notre mode favoris nous est accessible et si ce n'est pas le cas on prends le suivant dans la liste 
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
                        # test print(str(self.mark[k]) + "ma note")
                        markmax = float(self.mark[k])
                        # test print(str(markmax) + "note max")
                        indexMarkMax = k
            n=-1

        choice = LISTMODES[indexMarkMax]

        print("As a biased agent i chose "+choice+" has a mode of transportation.")
        self.biasChoise=choice
