import copy
import pickle
from environnement import *
from math import *
import random
from constant import *



class user:
    
    ident=int
    dico = {}
    biasMarks ={}  
    ##
    biasChoise=str #choix biaisé de l'utilisateur
    fitness = 50
    means=[None]*AGENTBOOLS.__len__()
    critAgent=[None]*CRITERIAS.__len__()
    rationalChoice= "none" #choix rationnel de l'utilisateur
    mark = [0,0,0,0]
    habits = []
    habiChoice="none" #choix habituel de l'user
    env=environnement
    # Initialisation de l'utilsateur avec trois choix 

    def __init__(self,envir=environnement,mode=str,id=int):
        
        #initialisation de l'identifiant de l'agent
        if id==0:
            self.ident=random.randint(0,100)
        else:
            self.ident=id

        # initialisation de l'environnement de l'agent 
        self.env = envir

        # Initialisation des notes attribuées aux différents critères de choix en fonctions des moyens des transports 
        self.dico = copy.deepcopy(self.env.marks)
        self.biasMarks = copy.deepcopy(self.env.marks)
        
        if mode=="Manual":
            # Demande à l'utilisateur s'il souhaite créé son agent grâce à un fichier, de façon aléatoire ou à la main 
            x = input("(r)andom agent priorities or (u)ser input or (f)ile input? : ")
            while x not in ["u","r","f"]:
                x = input("(u)ser agent priorities or (r)andom ? : ")
        else:
            x="r"

        # Initialisation d'un agent par input via la console 
        if x == "u": 
            cpt=0
            for crit in CRITERIAS :
                x = float(input("Priority (0-1) of " + crit + " ? : "))
                while x<0 or x>1:
                    x = float(input("Priority (0-1) of "+crit+" ? : "))		
                self.critAgent[cpt] = x
                cpt += 1


            # Initialisation des poids associés aux différents critères de choix
            cpt=0
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

            # Initialisation de la valeur de fitness de l'agent
            x=float(input("Am i fit on a scale from 0 to 100 ? :"))
            while x<0 or x>100:
                x=float(input("Am i fit on a scale from 0 to 100 ? :"))
            self.fitness=x

            # Sauvegarde de l'agent dans un fichier 
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
            file = open("agent/Agent"+str(id)+".txt","rb")
            agent = pickle.load(file)
            self = agent
            file.close()

        # Initialisation des habitudes
        y="a"
        if mode=="Manual":
            y= input("Do you want to use the (h)abits file as is,(e)rase it or erase it and create a (s)et of habits ? :")
            while y not in ["h","e","s"] :
                y= input("Do you want to use the (h)abits file as is,(e)rase it or erase it and create a (s)et of habits ? :")

        #On efface le fichier habits.txt
        if y=="e":
            self.habits = []

        if y=="a":
            self.habits = []
            for i in range(1000):
                n=random.randint(0,3)
                stringHabits = LISTMODES[n]+" "
                for j in CONTEXTBOOLS :
                    random_bit = random.getrandbits(1)
                    stringHabits += str(bool(random_bit))+" "
                self.habits.append(stringHabits)
                    
               

        if y=="s":
            self.habits = []
            z=input("Do you want to (r)andomize a certain number of habits or (e)nter them by hand ? : ")
            while z not in ["r","e"]:
                z=input("Do you want to (r)andomize a certain number of habits or (e)nter them by hand ? : ")
            h=int(input ("How many habits would you like to create ? :"))
            
            if z=="r":
                self.habits = []
                for i in range(h):
                    n=random.randint(0,3)
                    stringHabits = LISTMODES[n]+" "
                    for j in CONTEXTBOOLS :
                        random_bit = random.getrandbits(1)
                        stringHabits += str(bool(random_bit))+" "
                    self.habits.append(stringHabits)
                    

            if z=="e":

                for i in range(h):
                    m=input("Did i use a (0)bike, (1)car, (2)bus or did i (3)walk ? : ")
                    while m not in ["0","1","2","3"]:
                        m=input("Did i use a (0)bike, (1)car, (2)bus or did i (3)walk ? : ")
                    stringHabits = LISTMODES[int(m)]+" "
                
                    cpt = 0 
                    for elem in CONTEXTBOOLS:
                        answer = input(elem + " ? (y/n) : ")
                        while answer not in ["y","n"]:
                            answer = input(elem + " ? (y/n) : ")
                        envir.context[cpt] = (answer == "y")
                        cpt += 1
                    for boole in envir.context:
                        stringHabits += str(boole) + " "
                    self.habits.append(stringHabits)
        
        
                    
        


    # Fonction de sauvegarde de l'agent dans un fichier      
    def saveAgent(self):
        agent = open("agent/Agent"+str(self.ident)+".txt","wb")
        pickle.dump(self,agent)
        agent.close()

    # Methode retournant le choix rationel d'un agent
    def rationalModeChoice(self,envir=environnement):
        self.mark=[0,0,0,0]
        # Notation de chacun des modes de transport en fonction de l'evaluation de chaque mode
        i=0
        for mode in LISTMODES:
            j=0
            for key in CRITERIAS:
                self.mark[i]=float(self.mark[i]+(self.dico[mode][key]*self.critAgent[j]))  
                j+=1
            i+=1
      
       
        # Augmentaion de la note associé au vélo et à la marche pour les agents sportifs 

        if self.fitness >= 95 :
            self.mark[0] = self.mark[0]*2
            self.mark[3] = self.mark[3]*2

        markmax = 0
        indexMarkMax = 0
        k=0

     
        for k in range(0,len(self.mark)):
            
            if (float(self.mark[k])>markmax) :
                markmax = float(self.mark[k])
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
        #print qui peut etre de commenté en mode un seul agent
        #print("If i was a rationnal agent i would have chosen "+choice+" has a mode of transportation.")
        self.rationalChoice=choice

    # Fonction de choix habituel 
    def habitualChoice(self):
        # self.readHabits()
        weightMod=[0,0,0,0]
        cont=""                    
        for bool in self.env.context:
            cont=cont+str(bool)+" "        # Initialisation du context actuelle
            
        
        for lines in range(len(self.habits)) : # Initialisation du tableau weightMod qui determine combien de fois on as fait le choix n si les circonstances étaient similiares
             split = self.habits[lines].split(' ', 1)[0]

             if self.habits[lines].split(' ', 1)[1] == cont :
                 if split  == BIKE :
                     weightMod[0]=weightMod[0]+1
                 if split == CAR :
                     weightMod[1]=weightMod[1]+1
                 if split == BUS:
                     weightMod[2]=weightMod[2]+1
                 if split == WALK:
                     weightMod[3]=weightMod[3]+1

        totweight=weightMod[0]+weightMod[1]+weightMod[2]+weightMod[3]
        
        if totweight==0:
            return
        for i in range(len(weightMod)):
            weightMod[i]=weightMod[i]/totweight

        for i in {1,2,3}: 
            weightMod[i]=weightMod[i]+weightMod[i-1]

        rand=float(random.randint(0,100)/100)

        

        for i in range(len(weightMod)):
           
            if rand<weightMod[i]:
                choice=LISTMODES[i]
                self.habiChoice=choice
                break
            
        #On peut activer le print ci dessous en mode agent unique
        #print("In the contexte that i am in if i follow my usual behavior i will choose "+self.habiChoice+" as a mode of transportation")
        # si jamais on veut ajouter le choix habituel self.updateHabits(self.habiChoice)
    
    # Fonction permettant d'effacer le contenu du fichier habits.txt et donc de d'oublier l'ensemble des abitudes de l'agent
    def refreshHabits(self):
        habits = open("habits/habits"+str(self.ident)+".txt","w")
        habits.flush()
        habits.close()


    # Fonction permttant de mettre à jour les abitudes de l'agent en ajoutant le choix du dernier trajet réalisé 
    def updateHabits(self,choice=str):
        stringHabits = choice + " "
        for bool in self.env.context:
            stringHabits += str(bool) + " "
        self.habits.append(stringHabits)
       

    # Fonction de lecture du fichier d'habitude (ca marche)
    def readHabits(self):
        habits = open("habits/habits"+str(self.ident)+".txt","r")
        f=habits.readlines()
        for lines in range(len(f)) :
            f[lines]=f[lines].strip('\n')
        self.habits=f
        habits.close()
        

    # Methode prenant en parametre deux strings  mods appartenant à LISTMOD et crit apparentant a CRITERIAS retourne la valeur de biasmMarks[mods][crit]
    def getDicoAg(self,mods=str,crit=str):
        return self.dico[mods][crit]
    
    
    # Fonction permettant d'écrir dans un fichier le choix du moyen de transport avec et sans biais
    def result(self,env=environnement):
        res = open("result/Result"+str(self.ident)+".txt","a")
        res.write("Environemental conditions : \n Rainy : "+str(self.env.context[0])+" Good temperature : "+str(self.env.context[1])+ " Presence of light : "+str(self.env.context[2])+ " Do I live in a city ? : "+str(self.env.context[3])+ " Is it the rush hour ? : "+str(self.env.context[4])+"\n Gas Price :"+str(env.gasPrice)+"| Public Transport Price:"+str(env.subPrice)+"| Ratio Cycle Way : "+str(env.ratioCycleWay)+"| Bus frequency : "+str(env.busFrequency)+"| Bus Speed : "+str(env.busSpeed)+"| Bus Capacity : "+str(env.busCapacity)+"| Car speed : "+str(env.carSpeed)+"| Cycle Speed : "+str(env.bikeSpeed)+"| Walk speed : "+str(env.walkSpeed)+"\n")
        res.write("Habitual choice : "+self.habiChoice+"\n")
        res.write("Rationnal choice : "+self.rationalChoice+"\n")
        res.write("Biased choice : "+ self.biasChoise+"\n \n")
        res.close()

    # Ici les biais, en mode manual c'est cette fonction qui propose quels biais on desire activer en mode automatique c'est dans le main rand que l'on determine cela

    def biasedResults(self,envir=environnement,mode=str,estimation=bool,confirmation=bool,forbidden=bool):

        self.rationalModeChoice()
        self.habitualChoice()
        self.mark=[0,0,0,0]
        x=""
        y=""
        z=""
        aForbid=False
        aConf=False
        aEst=False
        if mode=="Manual":
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
        else :
            aForbid=forbidden
            aConf=confirmation
            aEst=estimation
        
        
        
        if aConf==True:
            #TODO faire un test pour determiner si on utilise le biais de confirmation ou la reactance

            # Confirmation en dessous
            if self.habiChoice  in [BIKE,CAR,BUS,WALK] :
                for mod in LISTMODES:
                    for crite in CRITERIAS:
                        if mod==self.habiChoice :
                            self.biasMarks[mod][crite]=self.dico[mod][crite] + random.normalvariate((envir.marks[mod][crite]/2),(envir.marks[mod][crite]/4))
                        else :
                            self.biasMarks[mod][crite]=self.dico[mod][crite] - random.normalvariate((envir.marks[mod][crite]/2),(envir.marks[mod][crite]/4))
        # Biais de sous/sur estimation seul (atm juste la distance peut etre ajouter le prix)
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
            self.biasMarks[CAR][FAST] = float(self.dico[CAR][FAST]) + random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4))#sous estimation du temps en voiture
            self.biasMarks[BUS][ECOLOGY] = envir.marks[BUS][ECOLOGY] 
            self.biasMarks[BUS][COMFORT] = envir.marks[BUS][COMFORT] 
            self.biasMarks[BUS][CHEAP] = envir.marks[BUS][CHEAP]
            self.biasMarks[BUS][SAFETY] = envir.marks[BUS][SAFETY]
            self.biasMarks[BUS][PRATICITY] = envir.marks[BUS][PRATICITY] 
            self.biasMarks[BUS][FAST] = float(self.dico[BUS][FAST]) - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4)) #sur estimation du temps en transport en commun
            self.biasMarks[WALK][ECOLOGY] = envir.marks[WALK][ECOLOGY] 
            self.biasMarks[WALK][COMFORT] = envir.marks[WALK][COMFORT]
            self.biasMarks[WALK][CHEAP] = envir.marks[WALK][CHEAP]
            self.biasMarks[WALK][SAFETY] = envir.marks[WALK][SAFETY]
            self.biasMarks[WALK][PRATICITY] = envir.marks[WALK][PRATICITY]
            self.biasMarks[WALK][FAST] = float(self.dico[WALK][FAST])- random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/3))#sur estimation du temps a pieds
        #Pareil qu'au dessus mais cette fois ci avec le biais de confirmation deja appliqué
        if aEst==True and aConf==True:
            
            self.biasMarks[CAR][FAST] = self.biasMarks[CAR][FAST] + random.normalvariate((envir.marks[CAR][FAST]/2),(envir.marks[CAR][FAST]/4)) #sous estimation du temps en voiture
            
            self.biasMarks[BUS][FAST] = self.biasMarks[BUS][FAST] - random.normalvariate((envir.marks[BUS][FAST]/2),(envir.marks[BUS][FAST] /4)) #sur estimation du temps en transport en commun
            
            self.biasMarks[WALK][FAST] = self.biasMarks[WALK][FAST] - random.normalvariate((envir.marks[WALK][FAST]/2),(envir.marks[WALK][FAST]/3)) #sur estimation du temps a pieds
        #Application du biais forbidden choice
        if aForbid==True:
            cpt=0
            if self.habiChoice==BIKE:
               
                for crit in CRITERIAS:
                    
                    if (envir.marks[BIKE][crit]>=0.5):
                        self.critAgent[cpt]=self.critAgent[cpt]+((1-self.critAgent[cpt])/2)
                    else :
                        if (envir.marks[BIKE][crit]<0.5):
                            self.critAgent[cpt]=self.critAgent[cpt]-((self.critAgent[cpt])/2)
                            cpt+=1
            if self.habiChoice==CAR:
                for crit in CRITERIAS:
                    
                    if (envir.marks[CAR][crit]>=0.5):
                        self.critAgent[cpt]=self.critAgent[cpt]+((1-self.critAgent[cpt])/2)
                    else :
                        if (envir.marks[CAR][crit]<0.5):
                            self.critAgent[cpt]=self.critAgent[cpt]-((self.critAgent[cpt])/2)
                    cpt+=1
            if self.habiChoice==BUS:
                for crit in CRITERIAS:
                    
                    if (envir.marks[BUS][crit]>=0.5):
                        self.critAgent[cpt]=self.critAgent[cpt]+((1-self.critAgent[cpt])/2)
                    else :
                        if float(envir.marks[BUS][crit])<0.5:
                            self.critAgent[cpt]=self.critAgent[cpt]-((self.critAgent[cpt])/2)
                    cpt+=1
            if self.habiChoice==WALK:
                for crit in CRITERIAS:
                    
                    if (envir.marks[WALK][crit]>=0.5):
                       self.critAgent[cpt]=self.critAgent[cpt]+((1-self.critAgent[cpt])/2)
                    else :
                        if float(envir.marks[WALK][crit])<0.5:
                            self.critAgent[cpt]=self.critAgent[cpt]-((self.critAgent[cpt])/2)
                    cpt+=1
            self.saveAgent()

        # Notation de chacun des modes de transport en fonction de l'evaluation de chaque mode
        i=0
        for mode in LISTMODES:
            
            j=0
            for key in CRITERIAS:
               
                self.mark[i]=float(self.mark[i]+(self.biasMarks[mode][key]*self.critAgent[j]))
                
                j+=1
            
            i+=1
        markmax = 0
        indexMarkMax = 0
        k=0

     
        for k in range(0,len(self.mark)):
            
            if (float(self.mark[k])>markmax) :
                
                markmax = float(self.mark[k])
                
                indexMarkMax = k

        choice = LISTMODES[indexMarkMax]

        # On verifie que notre mode favoris nous est accessible et si ce n'est pas le cas on prends le suivant dans la liste 
        n=4
        while n>0:
            if (choice==CAR and self.means[1]==False) or (choice==BUS and self.means[2]==False) or (choice==BIKE and self.means[0]==False) or  (choice==WALK and self.fitness<=10):
                #Print ci desssous que l'on peut de commenter si on utilise un seul agent
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

        #Print ci desssous que l'on peut de commenter si on utilise un seul agent
        #print("As a biased agent i chose "+choice+" has a mode of transportation.")
        self.biasChoise=choice
        self.updateHabits(self.biasChoise)
        self.habitualChoice()