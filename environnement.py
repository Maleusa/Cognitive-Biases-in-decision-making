class environnement:
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

    def __init__(self) -> None:

        ##initialisation de la météo
        cpt = 0 
        for elem in self.CONTEXTBOOLS:
            answer = input(elem + " ? (y/n) : ")
            while answer not in ["y","n"]:
                answer = input(elem + " ? (y/n) : ")
            self.weather[cpt] = (answer == "y")
            cpt += 1
        

        ##Initialisation de la note objective associée à chaque critères en fonction du moyen de transport
        dico={}
        for mode in self.LISTMODES:
            dico[mode] = {}
            for crit in self.CRITERIAS:
                dico[mode][crit]=0

        gasPrice=1.7 ##Prix SP95 le 14/04/2022
        subPrice=65.5 ##Prix moyen abonnement transport en france 2022
        ##ratioCycleWay = 
        busFrequency=10 ##Fréquence de passage de bus par heure à grenoble 
        busCapacity=100 ##Cf wikipedia page sur les autobus
        carSpeed=42.3 ##km/h en moyenne en France en 2020
        bikeSpeed=14 ##km/h en moyenne à Lyon en 2020
        walkSpeed=6.4 ##Vitesse moyenne de marche normale et dynamique 
        busSpeed=10 ##Km/h vitesse moyenne des bus a Paris en 2020