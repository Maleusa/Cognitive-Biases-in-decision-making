from os import environ
from environnement import *
from user import *

off = False
envir=environnement
actifAgent=user
aCount=0
eCount=0
while off != True:
  
    x= input("Do you want to create a new (e)nvironement, manipulate or create an (a)gent, e(x)it the program ? : ")
    while x not in ["e","a","x"] :
        x= input("Do you want to create a new (e)nvironement, manipulate or create an (a)gent, e(x)it the program ? : ")
    if x=="x":
        off=True
    if x=="e" :
        print("Creanting an environement")
        envir=environnement()
        eCount+=1
    if x=="a":
        if aCount==0 and eCount==0:
            y=input("There is no actif environement, you can not create or manipulate agent without there environement, would you like to create one? (y)/(n) : ")
            while y not in ["y","n"] :
                y=input("There is no actif environement, you can not create or manipulate agent without there environement, would you like to create one? (y)/(n) : ")
            if y=="y":
                print("Creating an environement :")
                envir=environnement()
                eCount+=1
            if y=="n":
                print("Then there is nothing i can do for you, goodbye !")
                off=True
                break
        if aCount==0 and eCount!=0:
            y=input("There is no actif agent in the enviroment, would you like to create one ? (y)/(n) :")
            while y not in ["y","n"] :
                y=input("There is no actif agent in the enviroment, would you like to create one ? (y)/(n) :")
            if y=="y":
                print("Creating an agent :")
                actifAgent=user(envir)
                aCount+=1
            if y=="n":
                print("Then there is nothing i can do for you, goodbye !")
                off=True
                break
        if aCount!=0:
            y=input("Would you like to create a new (a)gent or (m)anipulate the activ one ? : ")
            while y not in ["a","m"]:
                y=input("Would you like to create a new (a)gent or (m)anipulate the activ one ? : ")
            if y=="a":
                print("Creating an agent :")
                actifAgent=user(envir)
                aCount+=1
            if y=="m":
                print("Manipulation is a bad habit quit it !") #TODO ici proposer les differentes options de manipulation de l'agent actif
                break
            


