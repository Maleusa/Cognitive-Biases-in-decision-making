
from environnement import *
from user import *
from plot import *
randBool = True 

# Nombre d'agents créés par la simulation 
nbrAgent = int(input("How many agents do you want to create ? "))

# Liste des différents agents créés par la simulation
agentList = list()

# Booléens représentant l'activation des différents biais
estimation = False
confirmation = False 
forbidden = False 

# Demande à l'utilisateur si il veut activer le biais de sur/sous estimation des distances et modifie le booléen correspondant en conséquence
x = input("Do you want to see the effect oh the over/under estimation bias ? y/n")
while x not in ["y","n"]:
   x = input("Do you want to see the effect oh the over/under estimation bias ? y/n")
if x == "y":
    estimation = True

# Demande à l'utilisateur si il veut activer le biais de confirmation et modifie le booléen correspondant en conséquence
y = input("Do you want to see the effect of the confirmation bias ? y/n")
while y not in ["y","n"]:
   y = input("Do you want to see the effect oh the confirmation bias ? y/n")
if y == "y":
    confirmation = True

# Demande à l'utilisateur si il veut activer le biais du choix interdit et modifie le booléen correspondant en conséquence
z = input("Do you want to see the effect of the forbidden bias ? y/n")
while z not in ["y","n"]:
   z = input("Do you want to see the effect oh the forbidden bias ? y/n")
if z == "y":
    forbidden = True

# Définition de l'environnement de l'ensembles des agents 
env = environnement()

# création des agents et récupération de leur différentes décisions (rationnelle + biaisée + habituelle) et stockage de ces agents dans la liste agentList
for i in range(nbrAgent) :
    agent = user(env, "Auto",i+1)
    agentList.append(agent)
    agent.biasedResults(env,"Auto")
    #agent.result(env)

# Affiche du plot de résultats
plotDecision(agentList.copy())