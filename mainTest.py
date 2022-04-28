from environnement import *
from user import *

env = environnement()
agent = user(env)

user.rationalModeChoice(agent,env)
print(agent.rationalChoice)