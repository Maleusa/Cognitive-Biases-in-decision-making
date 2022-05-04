import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from user import *
from constant import *

def plotDecision(list=list):
    rationalDecision=[0,0,0,0]
    biasedDecision=[0,0,0,0]
    habitualDecision=[0,0,0,0]
    decisio=[None]*len(list)
    crit=[None]*len(list)
    for agent in list:
        
        if agent.biasChoise==BIKE:
            biasedDecision[0]+=1
        if agent.biasChoise==CAR:
            biasedDecision[1]+=1
        if agent.biasChoise==BUS:
            biasedDecision[2]+=1
        if agent.biasChoise==WALK:
            biasedDecision[3]+=1
    for agent in list:
        if agent.rationalChoice==BIKE:
            rationalDecision[0]+=1
        if agent.rationalChoice==CAR:
            rationalDecision[1]+=1
        if agent.rationalChoice==BUS:
            rationalDecision[2]+=1
        if agent.rationalChoice==WALK:
            rationalDecision[3]+=1
    for agent in list:
        if agent.habiChoice==BIKE:
            habitualDecision[0]+=1
        if agent.habiChoice==CAR:
            habitualDecision[1]+=1
        if agent.habiChoice==BUS:
            habitualDecision[2]+=1
        if agent.habiChoice==WALK:
            habitualDecision[3]+=1
    names = LISTMODES
   
    

    plt.figure(figsize=(9, 3))

    plt.subplot(131)
    plt.title('Rational Decision')
    plt.bar(names, rationalDecision)
    print(rationalDecision)
    plt.subplot(132)
    plt.title('Biased Decision')
    plt.bar(names, biasedDecision)
    print(biasedDecision)
    plt.subplot(133)
    plt.title('Habitual Decision')
    plt.bar(names, habitualDecision)
    print(habitualDecision)
    plt.suptitle('Bias effect on decision making')
    
    plt.show()
    