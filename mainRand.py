from environnement import *
from user import *
randBool = True 
nbrAgent = int(input("How many agents do you want to create ? "))

env = environnement(randBool)

for i in range(nbrAgent) :
    agent = user(env, randBool)
    agent.biasedResults(env)
    agent.result(env)