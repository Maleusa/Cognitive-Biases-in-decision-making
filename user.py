
from xmlrpc.client import Boolean
from environnement import *
from pickletools import markobject
from re import A, L
from math import *
from typing import Iterable
import random
from constant import *



class user:
    
    ident=int
    dico = dict
    biasMarks =dict    
    ##
    biasChoise=str # Choix biaisé de l'utilisateur
    fitness=float # Représente le niveau sportif de l'agent 
    means=[None]*AGENTBOOLS.__len__() # Représente les moyens de transport accessible à l'agent. Le premier booléan de la liste représente d'avoir une voiture ou non, le deuxième d'avoir un vélo ou non et le troisième d'être sur une ligne de bus ou non
    critAgent=[None]*CRITERIAS.__len__() # Représente le niveau entre 0 et 1 de priorité de chaque critère pour l'agent (1 : crière trèsimportant pour l'agent, 0 : critère négligeable pour l'agent)
    rationalChoice=str # Choix rationnel de l'utilisateur
    mark = [0,0,0,0] 
    habits = [] 
    habiChoice= "aucun" #Choix habituel de l'user
    env=environnement # Représente l'environnement de l'agent 
    
    # Initialisation de l'utilsateur avec trois choix 

    def __init__(self,envir=environnement,randomBool = bool,idAg=int):
        #copie du table des notes "objectives" dans le tableau bias Marks
        self.biasMarks=envir.marks
        #initialisation de l'identifiant de l'agent si jamais il n'est pas fait
        if idAg==0:

            self.ident=random.randint(0,100)
        else :
            self.ident=idAg
        # initialisation de l'environnement de l'agent 
        env = envir

        # Initialisation des notes attribué aux différents critères de choix en fonctions des moyens des transports 
        self.dico = env.marks.copy()
        self.biasMarks = env.marks.copy()
        
        if randomBool == True :
            x = "r"
        if randomBool == False :
        # Initialisation des poids associés aux différents critères de choix
            x = input("Agent priorities by (u)ser input, (r)andom or (f)ile input? : ")
            while x not in ["u","f","r"]:
                x = input("(u)ser agent priorities,(f)ile or (r)andom ? : ")


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
            #self.saveAgent()

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
            #self.saveAgent()

        # Initialisation d'un agent en lisant un fichier
        if x=="f":
            id=int(input("Please input the agent number between 0 and 100 ? : "))
            while id<0 or id>100:
                id=int(input("Please input the agent number between 0 and 100 ? : "))
            self.ident=id
            agent=open("agent/Agent"+str(id)+".txt","r")
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
        if randomBool == True :
            y = "s"
            z = "r"
            h = int(random.normalvariate(1000,10))
            #print(h)

        else :
            y= input("Do you want to use the (h)abits file as is,(e)rase it or erase it and create a (s)et of habits ? :")
            while y not in ["h","e","s"] :
                y= input("Do you want to use the (h)abits file as is,(e)rase it or erase it and create a (s)et of habits ? :")
            #On efface le fichier habits.txt
        if y=="e":
            self.refreshHabits()
        
        if y=="s":

            # Remet à zéro les habitudes 
            self.refreshHabits()

            # Si l'agent n'est pas créé en random, on demande si l'utilisateur veut utiliser un set de données randomisé ou les rentrer à la main 
            if randomBool == False :
                z=input("Do you want to (r)andomize a certain number of habits or (e)nter them by hand ? : ")
                while z not in ["r","e"]:
                    z=input("Do you want to (r)andomize a certain number of habits or (e)nter them by hand ? : ")
                
                # Permet de définir le nombre d'habtude de l'agent 
                h=int(input ("How many habits would you like to create ? :"))

            # Création  de h habitudes randomisées    
            if z=="r":
                
                for i in range(h):
                    habits = open("habits/habits"+str(self.ident)+".txt","a")
                    n=random.randint(0,3)
                    habits.write(LISTMODES[n]+" ")
                    for j in range(len(CONTEXTBOOLS)) :
                        random_bit = random.getrandbits(1)
                        habits.write(str(bool(random_bit))+" ")
                    habits.write("\n")
            

            # Création de h habitudes à la main par l'utilisateur 
            if z=="e":
                for i in range(h):
                    m=input("Did i use a (0)bike, (1)car, (2)bus or did i (3)walk ? : ")
                    while m not in ["0","1","2","3"]:
                        m=input("Did i use a (0)bike, (1)car, (2)bus or did i (3)walk ? : ")
                    habits = open("habits/habits.txt","a")
                    habits.write(LISTMODES[int(m)]+" ")
                    cpt = 0 
                    for elem in CONTEXTBOOLS:
                        answer = input(elem + " ? (y/n) : ")
                        while answer not in ["y","n"]:
                            answer = input(elem + " ? (y/n) : ")
                        envir.context[cpt] = (answer == "y")
                        cpt += 1
                    for boole in envir.context:
                        habits.write(str(boole) + " ")
                    habits.write('\n')



    # Fonction de sauvegarde de l'agent dans un fichier      
    def saveAgent(self):
        agent = open("agent/Agent"+str(self.ident)+".txt","w")
        for crit in self.critAgent:
            agent.write(str(crit)+"\n")
        agent.write("\n")
        for bool in self.means:
            agent.write(str(bool)+"\n")
        agent.write("\n"+str(self.fitness))

    # Methode retournant le choix rationel d'un agent
    def rationalModeChoice(self,envir=environnement):
        #CRITERIAS = [ECOLOGY, COMFORT, CHEAP, SAFETY, PRATICITY, FAST]  
        #LISTMODES = [BIKE,CAR,BUS,WALK]

        # Notation de chacun des modes de transport en fonction de l'evaluation de chaque mode
        i=0
        for mode in LISTMODES:
           
            j=0
            for key in CRITERIAS:
               
                # print(envir.marks[mode][key])
                self.mark[i]=self.mark[i]+(envir.marks[mode][key]*self.critAgent[j])
                
                j+=1
            
            i+=1
      
        
        # Augmentaion de la note associé au vélo et à la marche pour les agents sportifs 

        if self.fitness >= 70 :
            self.mark[0] = self.mark[0]*2
            self.mark[3] = self.mark[3]*2
        


        
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
                #print("I'd like to use  "+choice+" transport mode, but it is currently unaivalable to me.")
                self.mark[indexMarkMax]=0
                markmax = 0
                indexMarkMax = 0
                k=0

     
                for k in range(0,len(self.mark)):
            
                    if (float(self.mark[k])>markmax) :
                        markmax = float(self.mark[k])
                        indexMarkMax = k
            n=-1

        choice = LISTMODES[indexMarkMax]

        print("If i was a rationnal agent i would have chosen "+choice+" has a mode of transportation.")
      
        return choice

    # Fonction de choix habituel 
    def habitualChoice(self):
        self.readHabits()
        weightMod=[0,0,0,0]
        cont=""                    
        for bool in self.env.context:
            cont=cont+str(bool)+" "        # Initialisation du context actuelle
            
        
        for lines in range(len(self.habits)) : # Initialisation du tableau weightMod qui determine combien de fois on as fait le choix n sit les circonstances étaient similiares
             #test print(self.habits[lines].split(' ', 1)[1])
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
        #test print(weightMod)
        if totweight==0:
            #print("I have no usual behavior for this specific environement")
            return
        for i in range(len(weightMod)):
            weightMod[i]=weightMod[i]/totweight

        for i in {1,2,3}: 
            weightMod[i]=weightMod[i]+weightMod[i-1]

        rand=float(random.randint(0,100)/100)

        

        for i in range(len(weightMod)):
            #test print(rand)
            if rand<weightMod[i]:
                choice=LISTMODES[i]
                #test print(choice)
                self.habiChoice=choice
                break
            
        #test print(self.habiChoice)
        #print("In the contexte that i am in if i follow my usual behavior i will choose "+self.habiChoice+" as a mode of transportation")
        # si jamais on veut ajouter le choix habituel self.updateHabits(self.habiChoice)
        

     



    # Fonction permettant d'effacer le contenu du fichier habits.txt et donc de d'oublier l'ensemble des abitudes de l'agent
    def refreshHabits(self):
        habits = open("habits/habits"+str(self.ident)+".txt","w")
        habits.flush()


    # Fonction permttant de mettre à jour les abitudes de l'agent en ajoutant le choix du dernier trajet réalisé 
    def updateHabits(self,choice=str):
        
        habits = open("habits/habits"+str(self.ident)+".txt","a")
        
       

        habits.write(choice+" ")

        for bool in self.env.context:
            habits.write(str(bool) + " ")
        
        habits.write('\n')

        habits.close()

    # Fonction de lecture du fichier d'habitude (ca marche)
    def readHabits(self):
        habits = open("habits/habits"+str(self.ident)+".txt","r")
        f=habits.readlines()
        for lines in range(len(f)) :
            f[lines]=f[lines].strip('\n')
            
       
        self.habits=f
    #Methode prenant en parametre deux strings  mods appartenant à LISTMOD et crit apparentant a CRITERIAS retourne la valeur de biasmMarks[mods][crit]
    def getDicoAg(self,mods=str,crit=str):
        return self.biasMarks[mods][crit]
    
    
    # Fonction permettant d'écrir dans un fichier le choix du moyen de transport avec et sans biais
    def result(self,env=environnement):
        
        res = open("result/Result"+str(self.ident)+".txt","a")
        res.write("Environemental conditions : \n Rainy : "+str(self.env.context[0])+" Good temperature : "+str(self.env.context[1])+ " Presence of light : "+str(self.env.context[2])+ " Do I live in a city ? : "+str(self.env.context[3])+ " Is it the rush hour ? : "+str(self.env.context[4])+"\n Gas Price :"+str(env.gasPrice)+"| Public Transport Price:"+str(env.subPrice)+"| Ratio Cycle Way : "+str(env.ratioCycleWay)+"| Bus frequency : "+str(env.busFrequency)+"| Bus Speed : "+str(env.busSpeed)+"| Bus Capacity : "+str(env.busCapacity)+"| Car speed : "+str(env.carSpeed)+"| Cycle Speed : "+str(env.bikeSpeed)+"| Walk speed : "+str(env.walkSpeed)+"\n")
        res.write("Habitual choice : "+self.habiChoice+"\n")
        res.write("Rationnal choice : "+self.rationalChoice+"\n")
        res.write("Biased choice : "+ self.biasChoise+"\n \n")
        res.close()
    

    # Ici les biais

    def biasedResults(self,envir=environnement,randomBool = bool, confirmation = False, forbidden = False, estimation = False):
        self.rationalChoice=self.rationalModeChoice()
        self.habitualChoice()
       

        if randomBool == False :
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
                forbidden=True
            if x=="y":
                confirmation=True
            if y=="y":
                estimation=True
  #Application du biais forbidden choice 
        if forbidden==True:
            cpt=0
            #CRITERIAS = [ECOLOGY, COMFORT, CHEAP, SAFETY, PRATICITY, FAST]
            if self.habiChoice==BIKE:
               
                for crit in CRITERIAS:
                    print(crit)
                    if (envir.marks[BIKE][crit]>=0.5):
                        self.critAgent[cpt]=self.critAgent[cpt]+((1-self.critAgent[cpt])/2)
                    else :
                        if (envir.marks[BIKE][crit]<0.5):
                            self.critAgent[cpt]=self.critAgent[cpt]-((self.critAgent[cpt])/2)
                            cpt+=1
            if self.habiChoice==CAR:
                for crit in CRITERIAS:
                    print(crit)
                    if (envir.marks[CAR][crit]>=0.5):
                        self.critAgent[cpt]=self.critAgent[cpt]+((1-self.critAgent[cpt])/2)
                    else :
                        if (envir.marks[CAR][crit]<0.5):
                            self.critAgent[cpt]=self.critAgent[cpt]-((self.critAgent[cpt])/2)
                    cpt+=1
            if self.habiChoice==BUS:
                for crit in CRITERIAS:
                    print(crit)
                    if (envir.marks[BUS][crit]>=0.5):
                        self.critAgent[cpt]=self.critAgent[cpt]+((1-self.critAgent[cpt])/2)
                    else :
                        if float(envir.marks[BUS][crit])<0.5:
                            self.critAgent[cpt]=self.critAgent[cpt]-((self.critAgent[cpt])/2)
                    cpt+=1
            if self.habiChoice==WALK:
                for crit in CRITERIAS:
                    print(crit)
                    if (envir.marks[WALK][crit]>=0.5):
                       self.critAgent[cpt]=self.critAgent[cpt]+((1-self.critAgent[cpt])/2)
                    else :
                        if float(envir.marks[WALK][crit])<0.5:
                            self.critAgent[cpt]=self.critAgent[cpt]-((self.critAgent[cpt])/2)
                    cpt+=1
            self.saveAgent()
            self.biasChoise=self.rationalModeChoice()

        #TODO Maths des deux biais en modifian les valeurs soit de nos preference (forbidden behavior paradigme), soit de nos notes biaisé pour les autres dans le dict self.biasMarks 
        if confirmation==True:
            #TODO faire un test pour determiner si on utilise le biais de confirmation ou la reactance

            #Confirmation en dessous
            if self.habiChoice  in [BIKE,CAR,BUS,WALK] :
                for mod in LISTMODES:
                    for crite in CRITERIAS:
                        if mod==self.habiChoice :
                            self.biasMarks[mod][crite]=envir.marks[mod][crite] + random.normalvariate((envir.marks[mod][crite]/2),(envir.marks[mod][crite]/4))
                        else :
                            self.biasMarks[mod][crite]=envir.marks[mod][crite] - random.normalvariate((envir.marks[mod][crite]/2),(envir.marks[mod][crite]/4))
                #En dessous version sale du calcul d'au dessus        
                """self.biasMarks[BIKE][ECOLOGY] = envir.marks[BIKE][ECOLOGY] +random.normalvariate((envir.marks[BIKE][ECOLOGY]/2),(envir.marks[BIKE][ECOLOGY]/4))
                self.biasMarks[BIKE][COMFORT] = envir.marks[BIKE][COMFORT] +random.normalvariate((envir.marks[BIKE][COMFORT]/2),(envir.marks[BIKE][COMFORT]/4))
                self.biasMarks[BIKE][CHEAP] = envir.marks[BIKE][CHEAP] +random.normalvariate((envir.marks[BIKE][CHEAP]/2),(envir.marks[BIKE][CHEAP]/4))
                self.biasMarks[BIKE][SAFETY] = envir.marks[BIKE][SAFETY]+random.normalvariate((envir.marks[BIKE][SAFETY]/2),(envir.marks[BIKE][SAFETY]/4))
                self.biasMarks[BIKE][PRATICITY] = envir.marks[BIKE][PRATICITY] +random.normalvariate((envir.marks[BIKE][PRATICITY]/2),(envir.marks[BIKE][PRATICITY]/4))
                self.biasMarks[BIKE][FAST] = envir.marks[BIKE][FAST]+random.normalvariate((envir.marks[BIKE][FAST]/2),(envir.marks[BIKE][FAST]/4))
                self.biasMarks[CAR][ECOLOGY] = envir.marks[CAR][ECOLOGY] - random.normalvariate((envir.marks[CAR][ECOLOGY]/2),(envir.marks[CAR][ECOLOGY]/4)) #Ici on genere du bruit avec un float entre 0 et la valeur objective de la note selon une repartition normal avec pour moyenne note/2 et et note/4 (estimation a la louche)
                self.biasMarks[CAR][COMFORT] = envir.marks[CAR][COMFORT] -random.normalvariate((envir.marks[CAR][COMFORT]/2),(envir.marks[CAR][COMFORT] /4))
                self.biasMarks[CAR][CHEAP] = envir.marks[CAR][CHEAP] - random.normalvariate((envir.marks[CAR][CHEAP]/2),(envir.marks[CAR][CHEAP]/4))
                self.biasMarks[CAR][SAFETY] = envir.marks[CAR][SAFETY]- random.normalvariate((envir.marks[CAR][SAFETY]/2),(envir.marks[CAR][SAFETY]/4))
                self.biasMarks[CAR][PRATICITY] = envir.marks[CAR][PRATICITY] - random.normalvariate((envir.marks[CAR][PRATICITY]/2),(envir.marks[CAR][PRATICITY]/4))
                self.biasMarks[CAR][FAST] = envir.marks[CAR][FAST] - random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4))
                self.biasMarks[BUS][ECOLOGY] = envir.marks[BUS][ECOLOGY] - random.normalvariate((envir.marks[BUS][ECOLOGY]/2),(envir.marks[BUS][ECOLOGY]/4))
                self.biasMarks[BUS][COMFORT] = envir.marks[BUS][COMFORT] - random.normalvariate((envir.marks[BUS][COMFORT]/2),(envir.marks[BUS][COMFORT]/4))
                self.biasMarks[BUS][CHEAP] = envir.marks[BUS][CHEAP] - random.normalvariate((envir.marks[BUS][CHEAP]/2),(envir.marks[BUS][CHEAP]/4))
                self.biasMarks[BUS][SAFETY] = envir.marks[BUS][SAFETY] - random.normalvariate((envir.marks[BUS][SAFETY]/2),(envir.marks[BUS][SAFETY]/4))
                self.biasMarks[BUS][PRATICITY] = envir.marks[BUS][PRATICITY] - random.normalvariate((envir.marks[BUS][PRATICITY]/2 ),(envir.marks[BUS][PRATICITY]/4 ))
                self.biasMarks[BUS][FAST] = envir.marks[BUS][FAST] - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4))
                self.biasMarks[WALK][ECOLOGY] = envir.marks[WALK][ECOLOGY] -random.normalvariate((envir.marks[WALK][ECOLOGY]/2),(envir.marks[WALK][ECOLOGY]/4))
                self.biasMarks[WALK][COMFORT] = envir.marks[WALK][COMFORT] -random.normalvariate((envir.marks[WALK][COMFORT]/2),(envir.marks[WALK][COMFORT]/4))
                self.biasMarks[WALK][CHEAP] = envir.marks[WALK][CHEAP]-random.normalvariate((envir.marks[WALK][CHEAP]/2),(envir.marks[WALK][CHEAP]/4))
                self.biasMarks[WALK][SAFETY] = envir.marks[WALK][SAFETY]-random.normalvariate((envir.marks[WALK][SAFETY]/2),(envir.marks[WALK][SAFETY]/4))
                self.biasMarks[WALK][PRATICITY] = envir.marks[WALK][PRATICITY] - random.normalvariate((envir.marks[WALK][PRATICITY]/2),(envir.marks[WALK][PRATICITY]/4))
                self.biasMarks[WALK][FAST] = envir.marks[WALK][FAST] - random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/4))
            #DONE
            if self.habiChoice==CAR :
                self.biasMarks[BIKE][ECOLOGY] = envir.marks[BIKE][ECOLOGY] -random.normalvariate((envir.marks[BIKE][ECOLOGY]/2),(envir.marks[BIKE][ECOLOGY]/4))
                self.biasMarks[BIKE][COMFORT] = envir.marks[BIKE][COMFORT] -random.normalvariate((envir.marks[BIKE][COMFORT]/2),(envir.marks[BIKE][COMFORT]/4))
                self.biasMarks[BIKE][CHEAP] = envir.marks[BIKE][CHEAP] -random.normalvariate((envir.marks[BIKE][CHEAP]/2),(envir.marks[BIKE][CHEAP]/4))
                self.biasMarks[BIKE][SAFETY] = envir.marks[BIKE][SAFETY]-random.normalvariate((envir.marks[BIKE][SAFETY]/2),(envir.marks[BIKE][SAFETY]/4))
                self.biasMarks[BIKE][PRATICITY] = envir.marks[BIKE][PRATICITY] -random.normalvariate((envir.marks[BIKE][PRATICITY]/2),(envir.marks[BIKE][PRATICITY]/4))
                self.biasMarks[BIKE][FAST] = envir.marks[BIKE][FAST]-random.normalvariate((envir.marks[BIKE][FAST]/2),(envir.marks[BIKE][FAST]/4))
                self.biasMarks[CAR][ECOLOGY] = envir.marks[CAR][ECOLOGY] + random.normalvariate((envir.marks[CAR][ECOLOGY]/2),(envir.marks[CAR][ECOLOGY]/4)) #Ici on genere du bruit avec un float entre 0 et la valeur objective de la note selon une repartition normal avec pour moyenne note/2 et et note/4 (estimation a la louche)
                self.biasMarks[CAR][COMFORT] = envir.marks[CAR][COMFORT] +random.normalvariate((envir.marks[CAR][COMFORT]/2),(envir.marks[CAR][COMFORT] /4))
                self.biasMarks[CAR][CHEAP] = envir.marks[CAR][CHEAP] + random.normalvariate((envir.marks[CAR][CHEAP]/2),(envir.marks[CAR][CHEAP]/4))
                self.biasMarks[CAR][SAFETY] = envir.marks[CAR][SAFETY]+ random.normalvariate((envir.marks[CAR][SAFETY]/2),(envir.marks[CAR][SAFETY]/4))
                self.biasMarks[CAR][PRATICITY] = envir.marks[CAR][PRATICITY] + random.normalvariate((envir.marks[CAR][PRATICITY]/2),(envir.marks[CAR][PRATICITY]/4))
                self.biasMarks[CAR][FAST] = envir.marks[CAR][FAST] + random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4))
                self.biasMarks[BUS][ECOLOGY] = envir.marks[BUS][ECOLOGY] - random.normalvariate((envir.marks[BUS][ECOLOGY]/2),(envir.marks[BUS][ECOLOGY]/4))
                self.biasMarks[BUS][COMFORT] = envir.marks[BUS][COMFORT] - random.normalvariate((envir.marks[BUS][COMFORT]/2),(envir.marks[BUS][COMFORT]/4))
                self.biasMarks[BUS][CHEAP] = envir.marks[BUS][CHEAP] - random.normalvariate((envir.marks[BUS][CHEAP]/2),(envir.marks[BUS][CHEAP]/4))
                self.biasMarks[BUS][SAFETY] = envir.marks[BUS][SAFETY] - random.normalvariate((envir.marks[BUS][SAFETY]/2),(envir.marks[BUS][SAFETY]/4))
                self.biasMarks[BUS][PRATICITY] = envir.marks[BUS][PRATICITY] - random.normalvariate((envir.marks[BUS][PRATICITY]/2 ),(envir.marks[BUS][PRATICITY]/4 ))
                self.biasMarks[BUS][FAST] = envir.marks[BUS][FAST] - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4))
                self.biasMarks[WALK][ECOLOGY] = envir.marks[WALK][ECOLOGY] -random.normalvariate((envir.marks[WALK][ECOLOGY]/2),(envir.marks[WALK][ECOLOGY]/4))
                self.biasMarks[WALK][COMFORT] = envir.marks[WALK][COMFORT] -random.normalvariate((envir.marks[WALK][COMFORT]/2),(envir.marks[WALK][COMFORT]/4))
                self.biasMarks[WALK][CHEAP] = envir.marks[WALK][CHEAP]-random.normalvariate((envir.marks[WALK][CHEAP]/2),(envir.marks[WALK][CHEAP]/4))
                self.biasMarks[WALK][SAFETY] = envir.marks[WALK][SAFETY]-random.normalvariate((envir.marks[WALK][SAFETY]/2),(envir.marks[WALK][SAFETY]/4))
                self.biasMarks[WALK][PRATICITY] = envir.marks[WALK][PRATICITY] - random.normalvariate((envir.marks[WALK][PRATICITY]/2),(envir.marks[WALK][PRATICITY]/4))
                self.biasMarks[WALK][FAST] = envir.marks[WALK][FAST] - random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/4))
            #DONE
            if self.habiChoice==BUS :
                self.biasMarks[BIKE][ECOLOGY] = envir.marks[BIKE][ECOLOGY] -random.normalvariate((envir.marks[BIKE][ECOLOGY]/2),(envir.marks[BIKE][ECOLOGY]/4))
                self.biasMarks[BIKE][COMFORT] = envir.marks[BIKE][COMFORT] -random.normalvariate((envir.marks[BIKE][COMFORT]/2),(envir.marks[BIKE][COMFORT]/4))
                self.biasMarks[BIKE][CHEAP] = envir.marks[BIKE][CHEAP] -random.normalvariate((envir.marks[BIKE][CHEAP]/2),(envir.marks[BIKE][CHEAP]/4))
                self.biasMarks[BIKE][SAFETY] = envir.marks[BIKE][SAFETY]-random.normalvariate((envir.marks[BIKE][SAFETY]/2),(envir.marks[BIKE][SAFETY]/4))
                self.biasMarks[BIKE][PRATICITY] = envir.marks[BIKE][PRATICITY] -random.normalvariate((envir.marks[BIKE][PRATICITY]/2),(envir.marks[BIKE][PRATICITY]/4))
                self.biasMarks[BIKE][FAST] = envir.marks[BIKE][FAST]-random.normalvariate((envir.marks[BIKE][FAST]/2),(envir.marks[BIKE][FAST]/4))
                self.biasMarks[CAR][ECOLOGY] = envir.marks[CAR][ECOLOGY] - random.normalvariate((envir.marks[CAR][ECOLOGY]/2),(envir.marks[CAR][ECOLOGY]/4)) #Ici on genere du bruit avec un float entre 0 et la valeur objective de la note selon une repartition normal avec pour moyenne note/2 et et note/4 (estimation a la louche)
                self.biasMarks[CAR][COMFORT] = envir.marks[CAR][COMFORT] -random.normalvariate((envir.marks[CAR][COMFORT]/2),(envir.marks[CAR][COMFORT] /4))
                self.biasMarks[CAR][CHEAP] = envir.marks[CAR][CHEAP] - random.normalvariate((envir.marks[CAR][CHEAP]/2),(envir.marks[CAR][CHEAP]/4))
                self.biasMarks[CAR][SAFETY] = envir.marks[CAR][SAFETY]- random.normalvariate((envir.marks[CAR][SAFETY]/2),(envir.marks[CAR][SAFETY]/4))
                self.biasMarks[CAR][PRATICITY] = envir.marks[CAR][PRATICITY] - random.normalvariate((envir.marks[CAR][PRATICITY]/2),(envir.marks[CAR][PRATICITY]/4))
                self.biasMarks[CAR][FAST] = envir.marks[CAR][FAST] - random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4))
                self.biasMarks[BUS][ECOLOGY] = envir.marks[BUS][ECOLOGY] + random.normalvariate((envir.marks[BUS][ECOLOGY]/2),(envir.marks[BUS][ECOLOGY]/4))
                self.biasMarks[BUS][COMFORT] = envir.marks[BUS][COMFORT] + random.normalvariate((envir.marks[BUS][COMFORT]/2),(envir.marks[BUS][COMFORT]/4))
                self.biasMarks[BUS][CHEAP] = envir.marks[BUS][CHEAP] + random.normalvariate((envir.marks[BUS][CHEAP]/2),(envir.marks[BUS][CHEAP]/4))
                self.biasMarks[BUS][SAFETY] = envir.marks[BUS][SAFETY] + random.normalvariate((envir.marks[BUS][SAFETY]/2),(envir.marks[BUS][SAFETY]/4))
                self.biasMarks[BUS][PRATICITY] = envir.marks[BUS][PRATICITY] + random.normalvariate((envir.marks[BUS][PRATICITY]/2 ),(envir.marks[BUS][PRATICITY]/4 ))
                self.biasMarks[BUS][FAST] = envir.marks[BUS][FAST] + random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4))
                self.biasMarks[WALK][ECOLOGY] = envir.marks[WALK][ECOLOGY] -random.normalvariate((envir.marks[WALK][ECOLOGY]/2),(envir.marks[WALK][ECOLOGY]/4))
                self.biasMarks[WALK][COMFORT] = envir.marks[WALK][COMFORT] -random.normalvariate((envir.marks[WALK][COMFORT]/2),(envir.marks[WALK][COMFORT]/4))
                self.biasMarks[WALK][CHEAP] = envir.marks[WALK][CHEAP]-random.normalvariate((envir.marks[WALK][CHEAP]/2),(envir.marks[WALK][CHEAP]/4))
                self.biasMarks[WALK][SAFETY] = envir.marks[WALK][SAFETY]-random.normalvariate((envir.marks[WALK][SAFETY]/2),(envir.marks[WALK][SAFETY]/4))
                self.biasMarks[WALK][PRATICITY] = envir.marks[WALK][PRATICITY] - random.normalvariate((envir.marks[WALK][PRATICITY]/2),(envir.marks[WALK][PRATICITY]/4))
                self.biasMarks[WALK][FAST] = envir.marks[WALK][FAST] - random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/4))
            #DONE
            if self.habiChoice==WALK :
                self.biasMarks[BIKE][ECOLOGY] = envir.marks[BIKE][ECOLOGY] -random.normalvariate((envir.marks[BIKE][ECOLOGY]/2),(envir.marks[BIKE][ECOLOGY]/4))
                self.biasMarks[BIKE][COMFORT] = envir.marks[BIKE][COMFORT] -random.normalvariate((envir.marks[BIKE][COMFORT]/2),(envir.marks[BIKE][COMFORT]/4))
                self.biasMarks[BIKE][CHEAP] = envir.marks[BIKE][CHEAP] -random.normalvariate((envir.marks[BIKE][CHEAP]/2),(envir.marks[BIKE][CHEAP]/4))
                self.biasMarks[BIKE][SAFETY] = envir.marks[BIKE][SAFETY]-random.normalvariate((envir.marks[BIKE][SAFETY]/2),(envir.marks[BIKE][SAFETY]/4))
                self.biasMarks[BIKE][PRATICITY] = envir.marks[BIKE][PRATICITY] -random.normalvariate((envir.marks[BIKE][PRATICITY]/2),(envir.marks[BIKE][PRATICITY]/4))
                self.biasMarks[BIKE][FAST] = envir.marks[BIKE][FAST]-random.normalvariate((envir.marks[BIKE][FAST]/2),(envir.marks[BIKE][FAST]/4))
                self.biasMarks[CAR][ECOLOGY] = envir.marks[CAR][ECOLOGY] - random.normalvariate((envir.marks[CAR][ECOLOGY]/2),(envir.marks[CAR][ECOLOGY]/4)) #Ici on genere du bruit avec un float entre 0 et la valeur objective de la note selon une repartition normal avec pour moyenne note/2 et et note/4 (estimation a la louche)
                self.biasMarks[CAR][COMFORT] = envir.marks[CAR][COMFORT] -random.normalvariate((envir.marks[CAR][COMFORT]/2),(envir.marks[CAR][COMFORT] /4))
                self.biasMarks[CAR][CHEAP] = envir.marks[CAR][CHEAP] - random.normalvariate((envir.marks[CAR][CHEAP]/2),(envir.marks[CAR][CHEAP]/4))
                self.biasMarks[CAR][SAFETY] = envir.marks[CAR][SAFETY]- random.normalvariate((envir.marks[CAR][SAFETY]/2),(envir.marks[CAR][SAFETY]/4))
                self.biasMarks[CAR][PRATICITY] = envir.marks[CAR][PRATICITY] - random.normalvariate((envir.marks[CAR][PRATICITY]/2),(envir.marks[CAR][PRATICITY]/4))
                self.biasMarks[CAR][FAST] = envir.marks[CAR][FAST] - random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4))
                self.biasMarks[BUS][ECOLOGY] = envir.marks[BUS][ECOLOGY] - random.normalvariate((envir.marks[BUS][ECOLOGY]/2),(envir.marks[BUS][ECOLOGY]/4))
                self.biasMarks[BUS][COMFORT] = envir.marks[BUS][COMFORT] - random.normalvariate((envir.marks[BUS][COMFORT]/2),(envir.marks[BUS][COMFORT]/4))
                self.biasMarks[BUS][CHEAP] = envir.marks[BUS][CHEAP] - random.normalvariate((envir.marks[BUS][CHEAP]/2),(envir.marks[BUS][CHEAP]/4))
                self.biasMarks[BUS][SAFETY] = envir.marks[BUS][SAFETY] - random.normalvariate((envir.marks[BUS][SAFETY]/2),(envir.marks[BUS][SAFETY]/4))
                self.biasMarks[BUS][PRATICITY] = envir.marks[BUS][PRATICITY] - random.normalvariate((envir.marks[BUS][PRATICITY]/2 ),(envir.marks[BUS][PRATICITY]/4 ))
                self.biasMarks[BUS][FAST] = envir.marks[BUS][FAST] - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4))
                self.biasMarks[WALK][ECOLOGY] = envir.marks[WALK][ECOLOGY] +random.normalvariate((envir.marks[WALK][ECOLOGY]/2),(envir.marks[WALK][ECOLOGY]/4))
                self.biasMarks[WALK][COMFORT] = envir.marks[WALK][COMFORT] +random.normalvariate((envir.marks[WALK][COMFORT]/2),(envir.marks[WALK][COMFORT]/4))
                self.biasMarks[WALK][CHEAP] = envir.marks[WALK][CHEAP]+random.normalvariate((envir.marks[WALK][CHEAP]/2),(envir.marks[WALK][CHEAP]/4))
                self.biasMarks[WALK][SAFETY] = envir.marks[WALK][SAFETY]+random.normalvariate((envir.marks[WALK][SAFETY]/2),(envir.marks[WALK][SAFETY]/4))
                self.biasMarks[WALK][PRATICITY] = envir.marks[WALK][PRATICITY] + random.normalvariate((envir.marks[WALK][PRATICITY]/2),(envir.marks[WALK][PRATICITY]/4))
                self.biasMarks[WALK][FAST] = envir.marks[WALK][FAST] + random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/4))"""
        
        #Biais de sous/sur estimation seul (atm juste la distance peut etre ajouter le prix)
        if estimation==True and confirmation==False:
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
        if estimation==True and confirmation==True:
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
      
        

        # Notation de chacun des modes de transport en fonction de l'evaluation de chaque mode
        i=0
        for mode in LISTMODES:
            
            j=0
            for key in CRITERIAS:
               
                self.mark[i]=self.mark[i]+(self.biasMarks[mode][key]*self.critAgent[j])
                
                j+=1
            
            i+=1
        


        
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
                #print("I'd like to use  "+choice+" transport mode, but it is currently unaivalable to me.")
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

        #print("As a biased agent i chose "+choice+" has a mode of transportation.")
        self.biasChoise=choice
        #self.updateHabits(self.biasChoise)
        self.habitualChoice()
