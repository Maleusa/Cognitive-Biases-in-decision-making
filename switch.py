

	

## computation of habits from observations
## 1er décembre 2021, après réunion avec Alice
import random



####################################
###       USEFUL CONSTANTS       ###
####################################

# useful constants
MODE = "mode"

# elements of context
RAINY = "rainy"
#HOT = "hot"
TEMPOK = "temperature ok"
PEAKHOUR = "peak hour"
LIGHT = "light"
CONTEXTBOOLS = [RAINY,TEMPOK,PEAKHOUR,LIGHT]

# transportation modes
BIKE = "bike"
CAR = "individual car"
BUS = "public transport"
WALK = "walk"
LISTMODES = [BIKE,CAR,BUS,WALK]

# rational evaluation criteria, all in the same direction 
# higher value if more ecological, cheaper (lower price), faster (lower time)
ECOLOGY = "ecology"
COMFORT = "comfort"
CHEAP = "cheap"
SAFETY = "safety"
PRATICITY = "praticity"
FAST = "fast"
CRITERIAS = [ECOLOGY, COMFORT, CHEAP, SAFETY, PRATICITY, FAST]

# constraints on the activity
# all constraints of all activities in the sequence are added
FAR = "long distance away"
CHARGE = "must carry heavy stuff"
PASSENGERS = "has passengers"

# agent's features related to constraints
HASBIKE = "agent has bike"
HASCAR = "agent has car"
HASBUS = "agent is on bus line"
AGENTBOOLS = [HASBIKE, HASCAR, HASBUS]
FITNESS = "agent's fitness level"
AGENDA = "agenda of activities"

# activities
SCHOOL = "pick children from schools"
SHOPPING = "go shopping"
WORK = "commute to work"
LEISURE = "commute to leisure"
ACTIVITIES = [SCHOOL, SHOPPING, WORK, LEISURE]
ACTIVITY_CONSTRAINTS = {SCHOOL: [PASSENGERS], SHOPPING: [CHARGE], LEISURE: [FAR]}


#######################################
###       MOBILITY EVALUATION       ###
#######################################

## associating constraints to activities
def get_constraints(activities):
	constraints = []
	for act in activities:
		constraints.extend(ACTIVITY_CONSTRAINTS[act])
	return constraints

# constraints of transport modes
# receives agent, that has agenda (list of activities) and features (has bike, has car)
def get_available_modes(agent):
	modes = []
	constraints = get_constraints(agent[AGENDA])
	if agent[HASBIKE] and not CHARGE in constraints and not PASSENGERS in constraints and not FAR in constraints:
		modes.append(BIKE)
	if agent[HASCAR]:
		modes.append(CAR)
	if agent[HASBUS] and not CHARGE in constraints:
		modes.append(BUS)
	if agent[FITNESS] >= 20 and not CHARGE in constraints and not FAR in constraints:
		modes.append(WALK)
	return modes

## associating values of criteria to transport modes
## values indep from agent
def criteria_values(mode,criteria):
	# init dico
	dico = {}
	for mode in LISTMODES:
		dico[mode] = {}
		for crit in CRITERIAS:
			dico[mode][crit] = 0
	# now set specific values
	dico[BIKE][ECOLOGY] = 1
	#dico[BIKE][COMFORT] = round(agent

## setting values that depend on each agents

## associating context with changes in values of criterias?
## eg bike less comfy if temperature not ok



###################################################
###       RATIONAL EVALUATION OF MOBILITY       ###
###################################################

# modify environmental marks based on context elements
# rain/hot/cold/no light / peak hour modify the marks for the modes
### TODO
def updateEnv(env,context):
	# rain decreases comfort/safety/fast of bike/walk
	# hot decreases slightly comfort of bike/walk, 
	# hot increases comfort of car/bus (clim)
	# cold decreases comfort of bike/walk, increases for car/bus (heating)
	# peakhour decreases FAST
	# light
	pass

# mark given by one agent to one mode in one environment
def agentMarkMode(agent,mode,enviro):
	mark = 0
	# sum values*prio
	for crit in CRITERIAS:
		mark += agent[crit] * enviro[mode][crit]
	mark /= sum([agent[crit] for crit in CRITERIAS])
	return mark


def rationalMode(agent,enviro):
	# TODO = assuming that the enviro was modified by the daily context
	agentMarks = {}
	for mode in LISTMODES:
		agentMarks[mode] = agentMarkMode(agent,mode,enviro)

	# find the max
	maxmark = -1   # will find better
	for mode in LISTMODES:
		# TODO: what if equal prefs for several modes?
		if agentMarks[mode] > maxmark:
			prefmode = mode
	return prefmode



#####################################################
###       OBSERVATIONS, AGGREGATION, HABITS       ###
#####################################################

## random generation of observations
# in the form of a dictionary
def generateObservation():
	obs = {}
	obs[MODE] = random.choice(LISTMODES)
	for elem in CONTEXTBOOLS:
		obs[elem] = random.choice([True,False])
		# TODO: could define different probabilities for each
	return obs


# count occurrences of a mode in a given elem of context
# return -1 if no occurrence of that elem (= unknown status)
# not optimal, parses whole observations for each
# replaced by aggregateObservations
def countModeElem(observations, mode, elem, value):
	# directly count
	countmode = 0
	countother = 0
	for obs in observations:
		# if the relevant context element has the wanted value
		if obs[elem] == value:
			if obs[MODE] == mode:
				countmode += 1
			else:
				countother += 1
	# no occurrence of that element of context: unknown habit
	if countmode+countother == 0:
		return -1
	else:
		return countmode/(countmode+countother)

# aggregation = count different values of each context element
#    for each time a mode of mobility was chosen by this agent
def aggregateObservations(observations,memory=0):
	# memory provides the size of sliding window (def 0: full memory)
	habits = {}
	for mode in LISTMODES:
		habits[mode] = {}
	# count everything at the same time

	# for each observation
	# if memory depth provided, only take a slice of observations
	for obs in observations:
		# for each element of context (eg rain)
		for elem in CONTEXTBOOLS:
			# add its value in this observation to the habits
			if elem not in habits[obs[MODE]]:
				# first time: create empty list
				habits[obs[MODE]][elem] = []

			habits[obs[MODE]][elem].append(obs[elem])
	# return habits
	return habits

# TODO updateAggreg(aggreg,obs)
# add one more observation, update the dictionary without recomputing everything



# compute/build habits
# for a given mode + context, provide a proba to take it
# memory depth could play a role only here, on how far to look in aggregated obs
# similar to Vigiflood decision process
# 2 strategies (TODO test both) : max (most important elem of context)
# 		or avg (all elems play a role; eg if everything else is favourable, rain alone cannot prevent from cycling
def habit(aggreg,mode,context,memdepth=0):
	# return proba to take it
	probas = {}
	for elem in context:
		# list of booleans regarding the value of this elem of context
		li = aggreg[mode][elem]
		# memory depth TODO: take the last slice
		# proba to take this mode in the given context
		if len(li) == 0:
			# no occurrence: unknown proba
			p = -1
		else:
			p = li.count(context[elem]) / len(li)
		probas[elem] = p
	print("probas",probas)
	#return probas 

	# with max strategy, only the most important criteria decides
	return max(probas.values())
	# with the average, all probas take a role (lower habit in the end)
	# return sum(probas.values())/len(probas)


# read memory depth in agent if needed
# TODO: should store aggregated observations (aggreg) in the agent ?
def habitualMode(agent,aggreg,context):
	agentProbas = {}
	for mode in LISTMODES:
		agentProbas[mode] = habit(aggreg,mode,context)
	# find max 
	maxmark = -1   # will find better
	for mode in LISTMODES:
		# TODO: what if equal prefs for several modes?
		if agentProbas[mode] > maxmark:
			prefmode = mode
	return prefmode,agentProbas[prefmode]



##################################
###       INITIALISATION       ###
##################################

# generate an agent with random priorities for the 6 criteria
def generateAgent():
	agent = {}
	for crit in CRITERIAS:
		agent[crit] = random.random()
	# TODO set proba to have car/bike as parameter
	agent[HASBIKE] = random.choice([True,False])
	agent[HASCAR] = random.choice([True,False])
	agent[HASBUS] = random.choice([True,False])
	agent[FITNESS] = random.randint(1,100)
	agent[AGENDA] = [random.choice(ACTIVITIES)]
	if random.choice([True,False]):
		onemore = random.choice(ACTIVITIES)
		if onemore != agent[AGENDA][0]:
			agent[AGENDA].append(onemore)
	return agent

def inputAgent():
	agent = {}
	for crit in CRITERIAS:
		x = float(input("Priority (0-1) of "+crit+" ? : "))
		while x<0 or x>1:
			x = float(input("Priority (0-1) of "+crit+" ? : "))
		# priority within 0-1
		agent[crit] = x
	for agtbool in AGENTBOOLS:
		answ = input(agtbool+" ? y/n : ")
		while answ not in ["y","n"]:
			answ = input(agtbool+" ? y/n : ")
		agent[agtbool] = (answ == "y")
	act = input("Activity in "+ACTIVITIES+"? : ")
	agent[AGENDA] = []
	while act in ACTIVITIES :
		agent[AGENDA].append(act)
		act = input("Activity in "+ACTIVITIES+" (or stop) ? : ")
	# typed unknown activity or stop
	return agent

# user chooses random or user-input agent
def setAgent():
	# generate agent at random, or input
	x = input("(r)andom agent priorities or (u)ser input ? : ")
	while x not in ["u","r"]:
		x = input("(u)ser agent priorities or (r)andom ? : ")
	if x == "u": agent = inputAgent()
	else: agent = generateAgent()
	return agent



# generate the environment that gives values for each mode for each criteria
# represents the urban / legal / infrastructures environment
# can be modified by the urban manager / player (here simplified)
# TODO could read from a file (many values)
def generateEnvironment():
	marks = {}
	# TODO not all values are random !!! cf GAMA code
	for mode in LISTMODES:
		marks[mode] = {}
		for crit in CRITERIAS:
			marks[mode][crit] = random.random()	
	return marks
	
# generate a random context (hot, rainy, peakhour, etc)
# for today
def generateContext():
	context = {}
	for elem in CONTEXTBOOLS:
		context[elem] = random.choice([True,False])
		# TODO: could define different probabilities for each
	return context

# def input context
def inputContext():
	context = {}
	for elem in CONTEXTBOOLS:
		answer = input(elem + " ? (y/n) : ")
		while answer not in ["y","n"]:
			answer = input(elem + " ? (y/n) : ")
		# answer is "y" or "n"
		context[elem] = (answer == "y")
	return context

# user set context or selects random
def setContext():
	x = input("(u)ser context or (r)andom ? : ")
	while x not in ["u","r"]:
		x = input("(u)ser context or (r)andom ? : ")
	if x == "u": context = inputContext()
	else: context = generateContext()
	return context





################################
###       MAIN PROGRAM       ###
################################

# function to test the program
def play():
	# initialise everything
	n = int(input("How many initial observations? : "))
	observations = [generateObservation() for i in range(n)]
	aggreg = aggregateObservations(observations)

	# generate agent at random, or input
	agent = setAgent()
	print("Agent = ",agent)

	# generate the environment (TODO completely random so far)
	enviro = generateEnvironment()

	# generate a daily context or read it from user
	context = setContext()
	print("Context today = ",context)
	# update enviro with this context (TODO !!)
	updateEnv(enviro,context)

	# compute rational mode in that context
	rational = rationalMode(agent,enviro)
	print("rational choice = ",rational)

	# compute habitual mode in the daily context
	habitual,prob = habitualMode(agent,aggreg,context)
	print("habitual mode in this context = ",habitual,"with proba",prob)

	# choose (ponder between rational and habit with proba)
	# strengthen habit indirectly by adding observation 
	# observations.append(obs)
	# and updating aggregation
	# updateAggregation(aggreg,obs)

	# TODO loop to try again in same city, same agent, different daily context


play()









def debug():
	# main test program
	observations = [generateObservation() for i in range(20)]
	aggreg = aggregateObservations(observations)
	print("aggreg=",aggreg)
	context = generateContext()
	print("context =",context)
	habitcar = habit(aggreg,CAR,context)
	print(habitcar)

	agent = generateAgent()
	enviro = generateEnvironment()
	print("enviro=",enviro)
	print("agent=",agent)
	print("mark for bike=",agentMarkMode(agent,BIKE,enviro))
	print("mark for car=",agentMarkMode(agent,CAR,enviro))

	
	


