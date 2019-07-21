import random
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

	print("Lectures")
	for lecture in lectures:
		print(str(lecture.id) + "," + str(lecture.prof) + "," + str(lecture.hours) + "," + str(lecture.size))
	print("rooms")
	for room in rooms:
		print(str(room.id) + "," + str(room.size))

	#step 1: generate a population of chromosomes, each is an array of rooms
	#step 2: run genetic algorithm
		#step 2.1: run fitness function on each chromosome
		#step 2.2: select chromosomes for reproduction and cross over
		#step 2.3: repeat on offspring
	#step 3: display result in human readable way (print out chromosome somehow)


def crossover(parent1, parent2):
	#in crossover, iterate through each room, select classes from each parent
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

#returns a fitness value, the closer to zero the more fit the gene
def fitnessFunction(chromosome): 
	fitness = 0
	fitness = fitness + sameRoomeSameTime(chromosome) #adds to the fitness value for classes scheduled in the same room at the same time
	fitness = fitnesss + classCapacityExceeded(chromosome) #adds to the fitness value if a class is scheduled in a room that cant hold it
	fitness = fitness + hoursAccurate(chromosome) #adds to the fitness value if a lecture has too many or too few in a week
	fitness = fitness + repeatProf(chromosome) #(soft) adds to the fitness value for profs teaching in the same room two slots in a row
	fitness = fitness + slotsOnSameDay(chromosome) #(soft) adds to the fitness value for classes being schedules more than once per day
	return fitness

def sameRoomeSameTime(chromosome):
	pass

def classCapacityExceeded(chromosome):
	int i = 0
	int j = 0
		
	for i in range(len([chromsome])):
		for j in range(len([chromsome[i].times])):
			if chromosome[i].size < chromosome[i].times[j].size:
				return 100000
			
	return 0

def hoursAccurate(chromosome):
	pass

def repeatProf(chromosome):
	pass

def slotsOnSameDay(chromosome):
	pass

if __name__ == '__main__':
	main()
