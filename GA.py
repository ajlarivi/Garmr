import random
import copy
import math
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
		self.times = [None]*36 #array of time slots, each will contain a lecture object

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

	print("Lectures")
	for lecture in lectures:
		print(str(lecture.id) + "," + str(lecture.prof) + "," + str(lecture.hours) + "," + str(lecture.size))
	print("rooms")
	for room in rooms:
		print(str(room.id) + "," + str(room.size))

	#geneticAlgorithm(lectures,rooms,10,300)

	#step 1: generate a population of chromosomes, each is an array of rooms
	#step 2: run genetic algorithm
		#step 2.1: run fitness function on each chromosome
		#step 2.2: select chromosomes for reproduction and cross over
		#step 2.3: repeat on offspring
	#step 3: display result in human readable way (print out chromosome somehow)

def geneticAlgorithm(lectures, rooms, popSize, iterations):
	random.seed(datetime.now())
	population = initPopulation(rooms, lectures, popSize)

	for i in range(iterations):
		population = random.shuffle(population)

		for chromosome in population:
			chromosome[0] = fitnessFunction(chromosome)

		selected = selection(population)
		for pair in selected:
			population.append(crossover(pair[0], pair[1]))

		population.sort(key=lambda x: x[0], reverse=False)
		population = population[:popSize]
			
	return population[0]

#returns a fitness value, the closer to zero the more fit the chromosome
def fitnessFunction(chromosome): 
	fitness = 0
	fitness = fitness + duplicateLecture(chromosome) #adds to the fitness value for classes scheduled in the same room at the same time
	fitness = fitnesss + classCapacityExceeded(chromosome) #adds to the fitness value if a class is scheduled in a room that cant hold it
	fitness = fitness + hoursAccurate(chromosome) #adds to the fitness value if a lecture has too many or too few in a week
	fitness = fitness + repeatProf(chromosome) #(soft) adds to the fitness value for profs teaching in the same room two slots in a row
	fitness = fitness + slotsOnSameDay(chromosome) #(soft) adds to the fitness value for classes being schedules more than once per day
	return fitness

def duplicateLecture(chromosome):
	private int i = 0
	private int j = 0
	private int k = 0
		
	for j in range(len([chromsome].times])):
		i = 0
		for i in range(len([chromsome])):
			k = i + 1
			for k in range(len([chromosome])):
				if ((chromosome[i].times[j].id = chromosome[k].times[j].id)and(i!=k)):
					return 100000
			
	return 0

def classCapacityExceeded(chromosome):
	private int i = 0
	private int j = 0
		
	for i in range(len([chromsome])):
		for j in range(len([chromsome[i].times])):
			if chromosome[i].size < chromosome[i].times[j].size:
				return 100000
			
	return 0

def hoursAccurate(chromosome):
	pass

def repeatProf(chromosome):
	private int h = 0
	private int i = 0
	private int j = 0
	private int k = 0
	private int x = 0
		
	for i in range(len([chromsome])):
		for h in range(len([chromsome])):
			for j in range(len([chromosome[i])):
				k = j + 1
				if ((chromosome[i].times[j].prof = chromosome[h].times[k].prof)):
					x = x + 100
			
	return x

def slotsOnSameDay(chromosome):
	pass

#returns a list of tuples, each being a mating pair of chromosomes, chromosomes are more likely to be selected for mating the lower their fitness value is
def selection(population):
	popCopy = copy.deepCopy(population)
	numPairs = int(math.ceil(len(popCopy)/4))
	matingPairs = []

	maxFitness = 0
	for chromosome in popCopy:
		if chromosome[0] > maxFitness:
			maxFitness = chromosome[0]

	for chromosome in popCopy:
		chromosome.append(1 - chromosome[0]/maxFitness)

	for i in range(numPairs):
		chromosone1 = selectOne(popCopy)
		popCopy.remove(chromosone1)
		chromosome2 = selectOne(popCopy)
		popCopy.remove(chromosome2)
		matingPairs.append((chromosone1,chromosome2))

	return matingPairs

def selectOne(population):
	maxRange = sum([chromosome[1] for chromosome in population])
	pick = random.uniform(0, maxRange)
	current = 0
	for chromosome in population:
		current += chromosome[1]
		if current > pick:
			return chromosome




#returns a child of two parent chromosomes, by selectings schedulings from each parent and acdding them to the child
def crossover(parent1, parent2):
	random.seed(datetime.now())
	child = []

	for i in range(len(parent1)):
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

		
	return child

if __name__ == '__main__':
	main()
