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
		self.id = id
		self.size = size #capacity of the room
		self.times = [None]*35 #array of time slots, each will contain a lecture object

def main():
	fileString = sys.argv[1]
	inputFile = open(fileString, "r")
	lectures = []
	rooms = []
	readingRooms = False

	for line in inputFile:

		if line == "rooms\n":
			readingRooms = True
			continue

		line = line.strip("\n").split(",")

		if not readingRooms:
			lectures.append(Lecture(int(line[0]),int(line[1]),int(line[2]),int(line[3])))
		else:
			rooms.append(Room(int(line[0]),int(line[1])))

	# print("Lectures")
	# for lecture in lectures:
	# 	print(str(lecture.id) + "," + str(lecture.prof) + "," + str(lecture.hours) + "," + str(lecture.size))
	# print("rooms")
	# for room in rooms:
	# 	print(str(room.id) + "," + str(room.size))

	solution = geneticAlgorithm(lectures,rooms,10,100)
	print("==============================================")
	#printSolution(solution)

	#step 1: generate a population of chromosomes, each is an array of rooms
	#step 2: run genetic algorithm
		#step 2.1: run fitness function on each chromosome
		#step 2.2: select chromosomes for reproduction and cross over
		#step 2.3: repeat on offspring
	#step 3: display result in human readable way (print out chromosome somehow)

def geneticAlgorithm(lectures, rooms, popSize, iterations):
	random.seed(datetime.now())
	population = initPopulation(rooms, lectures, popSize)
	#printPopulation(population)

	for i in range(iterations):
		random.shuffle(population)

		for chromosome in population:
			chromosome[0] = fitnessFunction(chromosome, lectures)

		selected = selection(population)
		for pair in selected:
			population.append(crossover(pair[0], pair[1], lectures))

		population.sort(key=lambda x: x[0], reverse=False)
		population = population[:popSize]


		value = 0
		#print("[", end='')
		for chromosome in population:
			#print(str(chromosome[0]) + ", ", end='')
			value = value + chromosome[0]
		#print("]")
		print("avg fitness: " + str(value/(len(population) + 1)))



	return population[0]

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
	random.seed(datetime.now()) #seed random to avoid a pattern
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

#adds to the fitness value for classes scheduled in two rooms at the same time
def duplicateLecture(chromosome):
	addFitness = 0

	for i in range(len(chromosome[1].times)):
		notNone = []

		iterChromosome = iter(chromosome)
		next(iterChromosome)

		for room in iterChromosome:
			if room.times[i] is not None:
				notNone.append(room.times[i].id)

		counter = collections.Counter(notNone)
		for item in counter.values():
			if item > 1:
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

	for lecture in lectures:
		totalTime = 0

		iterChromosome = iter(chromosome)
		next(iterChromosome)

		for room in iterChromosome:
			for timeslot in room.times:
				if timeslot is not None and timeslot.id == lecture.id:
					totalTime = totalTime + 1
		addFitness = addFitness + abs(lecture.hours - totalTime) * 1000

	return addFitness

#(soft) adds to the fitness value for profs teaching in the same room two slots in a row
def repeatProf(chromosome):
	addFitness = 0

	iterChromosome = iter(chromosome)
	next(iterChromosome)

	for room in iterChromosome:
		for i,j in enumerate(range(1,len(room.times))):
			if room.times[i] is not None and room.times[j] is not None:
				if room.times[i].prof == room.times[j].prof:
					addFitness = addFitness + 100

	return addFitness

#(soft) adds to the fitness value for classes being schedules more than once per day
def slotsOnSameDay(chromosome):
	addFitness = 0

	iterChromosome = iter(chromosome)
	next(iterChromosome)

	for room in iterChromosome:
		notNone = []
		for timeslot in room.times:
			if timeslot is not None:
				notNone.append(timeslot)

		counter = collections.Counter(notNone)
		for item in counter.values():
			if item > 1:
				addFitness = addFitness + 100 * (item - 1)

	return addFitness

#returns a list of tuples, each being a mating pair of chromosomes, chromosomes are more likely to be selected for mating the lower their fitness value is
def selection(population):
	popCopy = copy.deepcopy(population)
	numPairs = int(math.ceil(len(popCopy)/4))
	matingPairs = []

	maxFitness = 0
	for chromosome in popCopy:
		if chromosome[0] > maxFitness:
			maxFitness = chromosome[0]

	for chromosome in popCopy:
		chromosome[0] = 1.1 - (chromosome[0]/maxFitness)

	for i in range(numPairs):
		chromosone1 = selectOne(popCopy)
		popCopy.remove(chromosone1)
		chromosome2 = selectOne(popCopy)
		popCopy.remove(chromosome2)
		matingPairs.append((chromosone1,chromosome2))

	return matingPairs

def selectOne(population):
	maxRange = sum([chromosome[0] for chromosome in population])
	pick = random.uniform(0, maxRange)
	current = 0

	for chromosome in population:
		current += chromosome[0]
		if current > pick:
			return chromosome

#returns a child of two parent chromosomes, by selectings schedulings from each parent and acdding them to the child
def crossover(parent1, parent2, lectures):
	random.seed(datetime.now())
	child = []

	for i in range(1, len(parent1)):
		childTimes = [None]*35
		for j in range(len(parent1[i].times)):
			if parent1[i].times[j] is not None and parent2[i].times[j] is None:
				childTimes[j] = parent1[i].times[j]

			if parent1[i].times[j] is None and parent2[i].times[j] is not None:
				childTimes[j] = parent2[i].times[j]

			if parent1[i].times[j] is not None and parent2[i].times[j] is not None:

				chance = random.randint(1,100)
				if chance <= 50:
					childTimes[j] = parent1[i].times[j]
				else:
					childTimes[j] = parent2[i].times[j]

		childRoom = parent1[i]
		childRoom.times = childTimes

		child.append(childRoom)

	child.insert(0, fitnessFunction(child, lectures))
	return child


def printPopulation(population):
	for chromosome in range(1, len(population)): #all chromosomes
		print("Chromosome number " + str(chromosome))

		for room in range(1, len(population[chromosome])):
			print("Room number " + str(population[chromosome][room].id))

			for time in range(len(population[chromosome][room].times)):
				if population[chromosome][room].times[time] is not None:
					print("Time slot number " + str(time) + ": " + str(population[chromosome][room].times[time].id)) #big fan of this chaining
				# else:
				# 	print("Time slot number " + str(time) + ": " + "No lecture")
			print("\n")
		print("\n")

def printSolution(chromosome):
	for room in range(1, len(chromosome)):
		print("Room number " + str(chromosome[room].id))

		for time in range(len(chromosome[room].times)):
			if chromosome[room].times[time] is not None:
				print("Time slot number " + str(time) + ": " + str(chromosome[room].times[time].id)) #big fan of this chaining
			else:
				print("Time slot number " + str(time) + ": " + "No lecture")
		print("\n")
	print("\n")
	print("solution fitness: " + str(chromosome[0]))


if __name__ == '__main__':
	main()
