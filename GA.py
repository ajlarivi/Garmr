import random
import copy
import math
import collections
import sys
from datetime import datetime


class Lecture:
	def __init__(self, id, prof, hours, size):
		self.id = id #id of lecture
		self.prof = prof # id of professor teaching the lecture
		self.hours = hours #required hours per week
		self.size = size #students registered in a lecture

class Room:
	def __init__(self, id, size):
		self.id = id #id of the room
		self.size = size #capacity of the room
		self.times = [None]*35 #array of time slots, each will contain a lecture object

def main():
	fileString = sys.argv[1]
	inputFile = open(fileString, "r")
	lectures = []
	rooms = []
	readingRooms = False
	counter = -1

	#start by reading the input file
	for line in inputFile:
		counter = counter + 1

		if line == "rooms: id, size\n": #check if we have started reading room inputs
			readingRooms = True
			continue

		line = line.strip("\n").split(",") #splice via commas and trim of the trailing newline

		if counter == 1: #set GA paramenters from first line of file
			populationSize = int(line[0])
			maxIterations = int(line[1])
			continue
		if counter == 0 or counter == 2: #skip info lines
			continue

		if not readingRooms: 
			lectures.append(Lecture(int(line[0]),int(line[1]),int(line[2]),int(line[3]))) #create lecture object from input and append to list of lectures
		else:
			rooms.append(Room(int(line[0]),int(line[1]))) #create room object from input and append to list of lectures

	solution, terminationType, actualIterations = geneticAlgorithm(lectures,rooms,populationSize,maxIterations) #run genetic algorithm

	printSolution(solution, terminationType, actualIterations) 


def geneticAlgorithm(lectures, rooms, popSize, iterations):
	random.seed(datetime.now()) #seed random to prevent patters arising
	population = initPopulation(rooms, lectures, popSize)
	terminationValue = None
	terminationCounter = 0
	terminationType = 0

	for i in range(iterations): #repeat for a maximum of the "iterations" parameter
		random.shuffle(population) #randomly shuffle the population, helps ensure random selection

		for chromosome in population: 
			chromosome[0] = fitnessFunction(chromosome, lectures) #evaluate the fitness of each individual in the population

		selected = selection(population) #select mating pairs within the population

		for pair in selected:
			population.append(crossover(pair[0], pair[1], lectures)) #add children of mating pairs to the population

		population.sort(key=lambda x: x[0], reverse=False) #sort population from lowest (best) fitness to highest (worst)
		population = population[:popSize] #trim population down to initial size (removes "least fit" individuals)


		sumFitness = 0
		for chromosome in population:
			sumFitness = sumFitness + chromosome[0]

		avgFitness = sumFitness/(len(population) + 1)
		topFitness = population[0][0]
		print("iteration: " + str(i+1) + ", avg fitness: " + str(avgFitness) + ", top fitness: " + str(topFitness))
		#print(str(i) + "," + str(population[0][0]) + "," + str(sumFitness/(len(population) + 1)))

		if terminationValue is None or terminationValue == topFitness:
			terminationCounter = terminationCounter + 1
		else:
			terminationCounter = 0

		terminationValue = topFitness

		if topFitness == 0: #if an individual has a fitness of zero we have found an ideal solution, algorithm can terminate
			terminationType = 1
			break 

		if terminationCounter > int(iterations/4): #if the top fitness hasnt changed for 1/4 of max iterations, the algorithm can be considered stuck and can terminate
			terminationType = 2
			break  

	return population[0], terminationType, i+1 #returns (the "most fit" individual, reason for termination, number of iterations)

#randomly generates an initial population of chromosomes of size popSize
def initPopulation(rooms, lectures, popSize):
	numLectures = len(lectures)
	population = []

	while len(population) < popSize:
		tempRooms = copy.deepcopy(rooms) #gotta deep copy to avoid weird Python referencing issues
		tempLectures = copy.deepcopy(lectures)

		while len(tempLectures) > 0: #run for total number of lectures
			randLecNum = getRandom(tempLectures)
			randLec = tempLectures[randLecNum] #pick random lecture from list to assign
			del tempLectures[randLecNum] #remove randomly chosen lecture from the running

			for i in range(randLec.hours): #have to add enough slots to cover required lecture hours
				randRoom = getRandom(tempRooms) #pick random room to put lecture in
				timeSlot = getNextFreeTime(tempRooms[randRoom])
				tempRooms[randRoom].times[timeSlot] = randLec #add chosen lecture to random time slot

		tempRooms.insert(0, 0) #add fitness value to start of chromosome
		population.append(tempRooms) #tack new chromosome onto the end of the population list

	return population

def getRandom(list):
	return random.randint(0, len(list) - 1)

def getNextFreeTime(room):
	randTime = getRandom(room.times)

	while room.times[randTime] is not None: #if slot value is not none there is a collision
		if randTime == len(room.times) - 1: #wrap back to 0 once we hit max lecture hour
			randTime = 0
		else: #otherwise, just increment by 1
			randTime += 1
	return randTime

#returns a fitness value, the closer to zero the more fit the chromosome
def fitnessFunction(chromosome, lectures):
	fitness = 0
	fitness = fitness + duplicateLecture(chromosome)
	fitness = fitness + classCapacityExceeded(chromosome)
	fitness = fitness + hoursAccurate(chromosome, lectures)
	fitness = fitness + repeatProf(chromosome)
	fitness = fitness + slotsOnSameDay(chromosome)
	return fitness

#adds to the fitness value for classes scheduled in two or more rooms at the same time
def duplicateLecture(chromosome):
	addFitness = 0

	for i in range(len(chromosome[1].times)):
		notNone = []

		iterChromosome = iter(chromosome)
		next(iterChromosome) #skip first element of chromosome (fitness value)

		for room in iterChromosome:
			if room.times[i] is not None: #create list of non-null lectures in a given timeslot across all rooms
				notNone.append(room.times[i].id)

		counter = collections.Counter(notNone) #count repititions of lectures  
		for item in counter.values():
			if item > 1: #if lecture is repeated, add to the fitness value
				addFitness = addFitness + 100000*(item - 1)

	return addFitness

#adds to the fitness value if a class is scheduled in a room that cant hold it
def classCapacityExceeded(chromosome):
	addFitness = 0

	for i in range(1, len(chromosome)):
		for j in range(len(chromosome[i].times)):
			if chromosome[i].times[j] is not None:
				if chromosome[i].size < chromosome[i].times[j].size:
					addFitness = addFitness + 100000

	return addFitness

#adds to the fitness value if a lecture has too many or too few in a week
def hoursAccurate(chromosome, lectures):
	addFitness = 0

	for lecture in lectures: #loop through all lectures
		totalTime = 0

		iterChromosome = iter(chromosome)
		next(iterChromosome) #skip first element of chromosome (fitness value)

		for room in iterChromosome:
			for timeslot in room.times:
				if timeslot is not None and timeslot.id == lecture.id:
					totalTime = totalTime + 1
		addFitness = addFitness + abs(lecture.hours - totalTime) * 1000 #add to fitness value for each hour missing or exceeded for a given lecture

	return addFitness

#(soft constraint) adds to the fitness value for profs teaching in the same room two slots in a row
def repeatProf(chromosome):
	addFitness = 0

	iterChromosome = iter(chromosome)
	next(iterChromosome) #skip first element of chromosome (fitness value)

	for room in iterChromosome:
		for i,j in enumerate(range(1,len(room.times))): #move through the list two at a time
			if room.times[i] is not None and room.times[j] is not None:
				if room.times[i].prof == room.times[j].prof:
					addFitness = addFitness + 100

	return addFitness

#(soft constraint) adds to the fitness value for classes being schedules more than once per day
def slotsOnSameDay(chromosome):
	addFitness = 0

	iterChromosome = iter(chromosome)
	next(iterChromosome) #skip first element of chromosome (fitness value)

	for room in iterChromosome:
		notNone = []
		for timeslot in room.times:
			if timeslot is not None: #create list of non-null lectures scheduled in a given room
				notNone.append(timeslot)

		counter = collections.Counter(notNone) #count repitions of non-null lectures
		for item in counter.values():
			if item > 1:
				addFitness = addFitness + 100 * (item - 1) #add to fitness for each identical lecture on the same day

	return addFitness

#returns a list of tuples, each being a mating pair of chromosomes, chromosomes are more likely to be selected for mating the lower their fitness value is
def selection(population):
	popCopy = copy.deepcopy(population) #dont want to be modifying actual population
	numPairs = int(math.ceil(len(popCopy)/4)) #only half the population gets selected as parents 
	matingPairs = []

	maxFitness = 0
	for chromosome in popCopy:
		if chromosome[0] > maxFitness:
			maxFitness = chromosome[0] #find the highest fitness value in the population

	for chromosome in popCopy:
		chromosome[0] = 1.1 - (chromosome[0]/maxFitness) #translate fitness value into a value between 0.1 and 1.1 (higher is now better)

	for i in range(numPairs):
		chromosone1 = selectIndividual(popCopy) #first parent
		popCopy.remove(chromosone1)
		chromosome2 = selectIndividual(popCopy) #second parent
		popCopy.remove(chromosome2)
		matingPairs.append((chromosone1,chromosome2)) #add tuple of mated pair to list

	return matingPairs

#selects an individual from a population using a weighted random chance. The higher an individuals adjusted fitness, the more likely it is to be selected
def selectIndividual(population):
	maxRange = sum([chromosome[0] for chromosome in population])
	pick = random.uniform(0, maxRange)
	current = 0

	for chromosome in population:
		current += chromosome[0]
		if current > pick:
			return chromosome

#returns a child of two parent chromosomes, by selectings schedulings from each parent and acdding them to the child
def crossover(parent1,parent2,lectures):
	child = []
	timesLength = len(parent1[1].times)

	for i in range(1, len(parent1)):
		randIndex = random.randint(1, timesLength - 2) #pick a random index between 1 and the second last list entry
		childTimes = parent1[i].times[:randIndex] + parent2[i].times[randIndex:] #splice the times array of each parent about randIndex (acheives crossover)

		childRoom = Room(parent1[i].id, parent1[i].size) #create new childRoom that is a copy of the parent (same id and size)
		childRoom.times = childTimes #assingn the spliced times array to the child room

		chance = random.randint(1,100)
		if chance <= 1: #1% chance of each room mutating
			random.shuffle(childRoom.times) #rearrange the timeslots of the mutated room

		child.append(childRoom) #add the room to the child chromosome

	child.insert(0, fitnessFunction(child, lectures)) #evaluate the fitness of the child chromosome and add this value to the first element of the list

	return child

#prints a single chromosome in a human readable form
def printSolution(chromosome, terminationType, actualIterations):
	for room in range(1, len(chromosome)):
		print("Room number " + str(chromosome[room].id))

		for time in range(len(chromosome[room].times)):
			if chromosome[room].times[time] is not None:
				print("Time slot number " + str(time) + ": " + str(chromosome[room].times[time].id)) #big fan of this chaining
			else:
				print("Time slot number " + str(time) + ": " + "No lecture")
		print("\n")
	print("\n")

	print("==============================================")
	print("solution fitness:\t" + str(chromosome[0]))
	print("reason for termination:\t", end='')
	if terminationType == 0:
		print("maximum iterations completed")
	elif terminationType == 1:
		print("ideal solution found")
	else:
		print("fitness no longer improving, algorithm cannot optimise any further")
	print("iterations completed:\t" + str(actualIterations))
	print("==============================================")

if __name__ == '__main__':
	main()
