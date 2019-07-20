import random
import copy
from datetime import datetime

from deap import base
from deap import creator
from deap import tools


class Lecture:
	def __init__(self, id, prof, hours, size):
		self.id = id
		self.prof = prof
		self.hours = hours
		self.size = size

class Room:
	def __init__(self, id, size):
		self.id = id
		self.size = size #capacity of the room
		self.times = [] #array of time slots, each will contain a lecture object

def initPopulation(rooms, lectures, popSize):
	numLectures = len(lectures)
	population = []

	while len(population) < popSize:
		tempRooms = copy.deepcopy(rooms)
		tempLectures = copy.deepcopy(lectures)
		random.seed(datetime.now())
		while len(tempLectures) > 0:
			randRoom = random.randint(0, len(tempRooms) - 1)
			randLecNum = random.randint(0, len(tempLectures) - 1)
			randLec = tempLectures[randLecNum]
			del tempLectures[randLecNum]
			tempRooms[randRoom].times.append(randLec)
		population.append(tempRooms)
	return population

def printPopulation(population):
	for x in range(len(population)):
		print("Chromosome number " + str(x + 1))
		for y in range(len(population[x])):
			print("Room number " + str(population[x][y].id))
			for z in range(len(population[x][y].times)):
				print(population[x][y].times[z].id)

def main():
	#step 1: generate a population of chromosomes, each is an array of rooms
	#step 2: run genetic algorithm
		#step 2.1: run fitness function on each chromosome
		#step 2.2: select chromosomes for reproduction and cross over
		#step 2.3: repeat on offspring
	#step 3: display result in human readable way (print out chromosome somehow)

	roomList = []
	lectureList = []

	for i in range(5):
		newRoom = Room(i, 50)
		roomList.append(newRoom)

	for j in range(10):
		newLecture = Lecture(j, "Scooter", 1, 40)
		lectureList.append(newLecture)

	startPop = initPopulation(roomList, lectureList, 2)
	printPopulation(startPop)


#returns a fitness value, the closer to zero the more fit the gene
def fitnessFunction(chromosome):
	fitness = 0
	fitness = fitness + sameRoomeSameTime(chromosome) #adds to the fitness value for classes scheduled in the same room at the same time
	fitness = fitnesss + classCapacityExceeded(chromosome) #adds to the fitness value if a class is scheduled in a room that cant hold it
	fitness = fitness + hoursAccurate(chromosome) #adds to the fitness value if a lecture has too many or too few in a week
	fitness = fitness + repeatProf(chromosome) #(soft) adds to the fitness value for profs teaching in the same room two slots in a row
	fitness = fitness + slotsOnSameDay(chromosome) #(soft) adds to the fitness value for classes being schedules more than once per day
	return fitness

if __name__ == '__main__':
	main()
