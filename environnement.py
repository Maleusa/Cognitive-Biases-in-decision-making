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

##Variable représentants le contexte 
gasPrice=float
subPrice=float
ratioCycleWay=float
busFrequency=int
busCapacity=int
carSpeed=int
bikeSpeed=int
walkSpeed=int
busSpeed=int

class environnement:

    TransportMode = LISTMODES
    crit = CRITERIAS

## Variables représentants la météo
    RAINY = "rainy"
    TEMPOK = "temperature ok"
    LIGHT = "light"
    CONTEXTBOOLS = [RAINY,TEMPOK,LIGHT]

    marks = {}
   

    def __init__(self) -> None:

        ##initialisation de la météo
        cpt = 0 
        for elem in self.CONTEXTBOOLS:
            answer = input(elem + " ? (y/n) : ")
            while answer not in ["y","n"]:
                answer = input(elem + " ? (y/n) : ")
            self.CONTEXTBOOLS[cpt] = (answer == "y")
            cpt += 1
        

        ##Initialisation de la note objective associée à chaque critères en fonction du moyen de transport
        
        for mode in self.TransportMode:
            self.marks[mode] = {}
            for crit in self.crit:
                self.marks[mode][crit]=0

        ##notes objectives 
        self.marks[BIKE][ECOLOGY] = 0.75
        self.marks[BIKE][COMFORT] = 0.25
        self.marks[BIKE][CHEAP] = 0.75
        self.marks[BIKE][SAFETY] = 0.25
        self.marks[BIKE][PRATICITY] = 0.25
        self.marks[BIKE][FAST] = 0.75
        self.marks[CAR][ECOLOGY] = 0.25
        self.marks[CAR][COMFORT] = 1
        self.marks[CAR][CHEAP] = 0.25
        self.marks[CAR][SAFETY] = 0.75
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
        self.marks[WALK][SAFETY] = 0.5
        self.marks[WALK][PRATICITY] = 0.5
        self.marks[WALK][FAST] = 0.25

        ##initailisation des variables de context
        ##L'utilisateur peut choisir d'utiliser les variables de contextes par défault ou de les rentrer soit même dans la console

        x = input("(s)tandart context variables or (u)ser input ? : ")
        while x not in ["u","s"]:
            x = input("(s)tandart context variables or (u)ser input ? : ")
        
        if x == "s":
            gasPrice=1.7 ##Prix SP95 le 14/04/2022
            subPrice=65.5 ##Prix moyen abonnement transport en france 2022
            ratioCycleWay = 0.5 ##Valeure prise dans Switch
            busFrequency=10 ##Fréquence de passage de bus par heure à grenoble 
            busCapacity=100 ##Cf wikipedia page sur les autobus
            carSpeed=42.3 ##km/h en moyenne en France en 2020
            bikeSpeed=14 ##km/h en moyenne à Lyon en 2020
            walkSpeed=6.4 ##Vitesse moyenne de marche normale et dynamique 
            busSpeed=10 ##Km/h vitesse moyenne des bus a Paris en 2020
        
        if x == "u":
            gasPrice= input("Gas price ?")
            subPrice= input("Bus subscription price ?")
            ratioCycleWay = input("Ration cycle way ?")
            busFrequency= input( "Bus frequency ?")
            busCapacity= input("Bus capacity ?")
            carSpeed= input("Car speed ?")
            bikeSpeed=input("Bike speed ?")
            walkSpeed=input("Walk speed ?")
            busSpeed=input("bus Speed ?")

    def getMarks(self) :
        return self.marks