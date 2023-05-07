
from constant import *
# Variable représentants le contexte 
gasPriceStandart=1.7 # Prix SP95 le 14/04/2022
subPriceStandart=65.5 # Prix moyen abonnement transport en france 2022
ratioCycleWayStandart = 0.5 # Valeure prise dans Switch
busFrequencyStandart=10 # Fréquence de passage de bus par heure à grenoble 
busCapacityStandart=100 # Cf wikipedia page sur les autobus
carSpeedStandart=42.3 # km/h en moyenne en France en 2020
bikeSpeedStandart=14 # km/h en moyenne à Lyon en 2020
walkSpeedStandart=6.4 # Vitesse moyenne de marche normale et dynamique 
busSpeedStandart=10 # Km/h vitesse moyenne des bus a Paris en 2020



class environnement:

    # Déclaration des varaibales de contexte 
    gasPrice= float
    subPrice= float
    ratioCycleWay = float
    busFrequency= float
    busCapacity= float
    carSpeed= float
    bikeSpeed=float
    walkSpeed=float
    busSpeed=float

    # Récupération de la liste des transports disponibles dans cetn environnement 
    TransportMode = LISTMODES

    # Récupération de la liste des critères de choix des agents 
    crit = CRITERIAS

    # Variables représentants la météo
    context = [None]*len(CONTEXTBOOLS)

    # Dictionnaire des notes qui pour chaque moyen de transport évaluera chaque critère
    marks = {}

    def __init__(self) :
        

        # Initialisation de la météo
        cpt = 0 
        for elem in CONTEXTBOOLS:
            answer = input(elem + " ? (y/n) : ")
            while answer not in ["y","n"]:
                answer = input(elem + " ? (y/n) : ")
            self.context[cpt] = (answer == "y")
            cpt += 1
        

        # Initialisation de la note objective associée à chaque critères en fonction du moyen de transport
        for mode in self.TransportMode:
            self.marks[mode] = {}
            for crit in self.crit:
                self.marks[mode][crit]=0

        # Notes objectives (à estimer avec questionnaire, définie arbitrairement pour le moment)
        self.marks[BIKE][ECOLOGY] = 1
        self.marks[BIKE][COMFORT] = 0.25
        self.marks[BIKE][CHEAP] = 1
        self.marks[BIKE][SAFETY] = 0.25
        self.marks[BIKE][PRATICITY] = 0.75
        self.marks[BIKE][FAST] = 0.75

        self.marks[CAR][ECOLOGY] = 0.25
        self.marks[CAR][COMFORT] = 1
        self.marks[CAR][CHEAP] = 0.25
        self.marks[CAR][SAFETY] = 0.5
        self.marks[CAR][PRATICITY] = 1
        self.marks[CAR][FAST] = 1

        self.marks[BUS][ECOLOGY] = 0.5
        self.marks[BUS][COMFORT] = 0.75
        self.marks[BUS][CHEAP] = 0.5
        self.marks[BUS][SAFETY] = 1
        self.marks[BUS][PRATICITY] = 0.75
        self.marks[BUS][FAST] = 0.5
        
        self.marks[WALK][ECOLOGY] = 1
        self.marks[WALK][COMFORT] = 0.5
        self.marks[WALK][CHEAP] = 1
        self.marks[WALK][SAFETY] = 0.75
        self.marks[WALK][PRATICITY] = 0.5
        self.marks[WALK][FAST] = 0.25

        

        # Initailisation des variables de context
        # L'utilisateur peut choisir d'utiliser les variables de contextes par défault ou de les rentrer soit même dans la console

        x = input("(s)tandart context variables or (u)ser input ? : ")
        while x not in ["u","s"]:
            x = input("(s)tandart context variables or (u)ser input ? : ")
        
        # Initialisation des variables d'environnement à leur valeur standart 
        if x == "s":
            self.gasPrice=gasPriceStandart
            self.subPrice=subPriceStandart
            self.ratioCycleWay=ratioCycleWayStandart
            self.busFrequency=busFrequencyStandart
            self.busCapacity=busCapacityStandart
            self.busSpeed=busSpeedStandart
            self.bikeSpeed=bikeSpeedStandart
            self.walkSpeed=walkSpeedStandart
            self.carSpeed=carSpeedStandart

        # Initialisation des variables d'environnement à des valeurs rentrées par l'utilisateur 
        if x == "u":
            self.gasPrice= float(input("Gas price ? "))
            self.subPrice= float(input("Bus subscription price ? "))
            self.ratioCycleWay = float(input("Ration cycle way ? "))
            self.busFrequency= float(input( "Bus frequency per hour? "))
            self.busCapacity= float(input("Bus capacity ? "))
            self.carSpeed= float(input("Car speed ? "))
            self.bikeSpeed=float(input("Bike speed ? "))
            self.walkSpeed=float(input("Walk speed ? "))
            self.busSpeed=float(input("bus Speed ? "))

            # Modification des notes en fonctions des variables d'environnement 
            self.marksVariable()

        # Modification des notes en fonction des booléens de contextes (météo + ville + heure de pointe)
        self.marksWeather()
    
    # fonction permettant de modifier les notes attribué à chaque items en fonction des variables contexte
    def marksVariable(self) :
        # Modification des notes liées au prix de l'essence
        self.marks[CAR][CHEAP] =  self.marks[CAR][CHEAP]*(1/self.coefMulti(self.gasPrice,gasPriceStandart))

        # Modification des notes liées au prix de l'abonnement de bus
        self.marks[BUS][CHEAP] = self.marks[BUS][CHEAP] * (1/self.coefMulti(self.subPrice,subPriceStandart))

        # Modification des notes liées à la proportion de pristes cyclables 
        self.marks[BIKE][SAFETY] =  self.marks[BIKE][SAFETY] * self.coefMulti(self.ratioCycleWay,ratioCycleWayStandart)
        self.marks[BIKE][FAST] =  self.marks[BIKE][FAST] * self.coefMulti(self.ratioCycleWay,ratioCycleWayStandart)

        # Modifications des notes liées à la fréquence de bus 
        self.marks[BUS][FAST] = self.marks[BUS][FAST] * self.coefMulti(self.busFrequency,busFrequencyStandart)

        # Modifications des notes liées à la capacité des bus 
        self.marks[BUS][COMFORT] = self.marks[BUS][COMFORT]*self.coefMulti(self.busCapacity,busCapacityStandart)

        # Modification des notes liées aux vitesses de déplacement des différents moyens de transport 
        self.marks[BIKE][FAST] = self.marks[BIKE][FAST] * self.coefMulti(self.bikeSpeed,bikeSpeedStandart)
        self.marks[BUS][FAST] =  self.marks[BUS][FAST] * self.coefMulti(self.busSpeed,busSpeedStandart)
        self.marks[CAR][FAST] =  self.marks[CAR][FAST] * self.coefMulti(self.carSpeed,carSpeedStandart)
        self.marks[WALK][FAST] = self.marks[WALK][FAST] * self.coefMulti(self.walkSpeed,walkSpeedStandart)

    def marksWeather(self):
        # Modification des notes liées à la présence de pluie
        # Si il pleut, le vélo devient moins confortable et plus dangereux, la marche devient moins confortable
        if self.context[0] == True :
            self.marks[BIKE][COMFORT] =  self.marks[BIKE][COMFORT]/2
            self.marks[BIKE][SAFETY] =  self.marks[BIKE][SAFETY]/2
            self.marks[WALK][COMFORT] =  self.marks[WALK][COMFORT]/2

        # Modification des notes liées à la température
        # Si il fait trop froid ou trop chaud, le vélo et la marche deviennent moins confortable
        if self.context[1] == False :
            self.marks[BIKE][COMFORT] =  self.marks[BIKE][COMFORT]/2
            self.marks[WALK][COMFORT] =  self.marks[WALK][COMFORT]/2

        # Modification des notes liées à la lumière
        # Si il y a pas de lumière, le vélo, la marche et la voiture deviennent plus dangereux 
        if self.context[2] == False :
            self.marks[BIKE][SAFETY] =  self.marks[BIKE][SAFETY]/2
            self.marks[WALK][SAFETY] =  self.marks[WALK][SAFETY]/2
            self.marks[CAR][SAFETY] = self.marks[CAR][SAFETY]/2

        # Modification des notes liées au fait de vivre en ville 
        # Si l'agent vit en ville, la voiture devient moins rapide et moins pratique 
        if self.context[3] == True :
            self.marks[CAR][FAST] = self.marks[CAR][FAST]/2
            self.marks[CAR][PRATICITY] = self.marks[CAR][PRATICITY]/2
        
        # Modification des notes liées au fait de circuler en heure de pointe 
        # Si l'agent circule en heure de pointe, la voiture devient moins rapide 
        if self.context[4] == True :
            self.marks[CAR][FAST] = self.marks[CAR][FAST]/2

    # Fonction permettant de calculer le coefficiant multiplicateur permettant de passer de valStandard à valUser
    def coefMulti(self,valUser,valStandard) :
        return valUser/valStandard

    # Fonction permettant de modifier les valeurs des différentes variables (booleens de contexte + variables d'environnement) après l'initialisation de l'environnement 
    def changVariable(self) :

        cpt = 0 
        for elem in CONTEXTBOOLS:

            # Modification des booléens de contexte
            answer = input(elem + " ? (y/n) : ")
            while answer not in ["y","n"]:
                answer = input(elem + " ? (y/n) : ")
            self.context[cpt] = (answer == "y")
            cpt += 1

        #Modification des variables d'environnement 
        self.gasPrice= float(input("Gas price ? "))
        self.subPrice= float(input("Bus subscription price ? "))
        self.ratioCycleWay = float(input("Ration cycle way ? "))
        self.busFrequency= float(input( "Bus frequency per hour? "))
        self.busCapacity= float(input("Bus capacity ? "))
        self.carSpeed= float(input("Car speed ? "))
        self.bikeSpeed=float(input("Bike speed ? "))
        self.walkSpeed=float(input("Walk speed ? "))
        self.busSpeed=float(input("bus Speed ? "))

        # Modification des notes en fonction des nouveaux booleens de contexte
        self.marksVariable()

        # Modification des notes en fonction des variables d'environnement 
        self.marksWeather()
        