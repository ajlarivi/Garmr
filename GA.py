import random

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
	def __init__(self, size):
		self.size = size #capacity of the room
		self.times = [] #array of time slots, each will contain a lecture object

def main():
	toolbox  = base.Toolbox
	#step 1: generate a population of chromosomes, each is an array of rooms
	#step 2: run genetic algorithm
		#step 2.1: run fitness function on each chromosome
		#step 2.2: select chromosomes for reproduction and cross over
		#step 2.3: repeat on offspring
	#step 3: display result in human readable way (print out chromosome somehow)

	print("hello world")

def crossover(parent1, parent2):
	#in crossover, iterate through each room, select classes from each parent

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
	pass

def hoursAccurate(chromosome):
	pass

def repeatProf(chromosome):
	pass

def slotsOnSameDay(chromosome):
	pass

if __name__ == '__main__':
	main()
