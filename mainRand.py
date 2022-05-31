
from environnement import *
from user import *
from plot import *
randBool = True 
nbrAgent = int(input("How many agents do you want to create ? "))
agentList = list()

estimation = False
confirmation = False 
forbidden = False 

x = input("Do you want to see the effect oh the over/under estimation bias ? y/n")
while x not in ["y","n"]:
   x = input("Do you want to see the effect oh the over/under estimation bias ? y/n")
if x == "y":
    estimation = True

y = input("Do you want to see the effect of the confirmation bias ? y/n")
while y not in ["y","n"]:
   y = input("Do you want to see the effect oh the confirmation bias ? y/n")
if y == "y":
    confirmation = True

z = input("Do you want to see the effect of the confirmation bias ? y/n")
while z not in ["y","n"]:
   z = input("Do you want to see the effect oh the confirmation bias ? y/n")
if z == "y":
    forbidden = True


env = environnement()

for i in range(nbrAgent) :
    agent = user(env, "Auto",i+1,estimation,confirmation,forbidden)
    agentList.append(agent)
    agent.biasedResults(env,"Auto")
    #agent.result(env)

plotDecision(agentList.copy())