# GLA class.
from geometry import *
from extras import *
from scoring import *
import random

FLOAT_PRECISION = 12
MAX_SIZE_TEST = 5.0
MAX_OBJECT_COUNT = 3    # Most objects can handle 3. You can generate with more or less, though. Each new object will cut score, as determined below.
ADD_OBJECT_COST = 0.2   # Cost of adding a new object - 1 means each object cuts score in half, 0 means no negative effect

##### HELPER FUNCTIONS ######

"""
Converts bits into a floating point number.
It's nice because the number of bits can be variable if you decide you want more precision.
This will return some fraction of the max_size given.
"""
def GeneToFloat(bitArray, max_size):
	toReturn = 0
	if len(bitArray) != FLOAT_PRECISION:
		print "Improper length of array!"
		return
	else:
		for i in range(0, FLOAT_PRECISION):
			toReturn *= 2
			if bitArray[-i] == 1:
				toReturn += 1
	maxReturn = 2 ** FLOAT_PRECISION - 1
	return (float(toReturn) / maxReturn) * max_size

def GenerateRandomGene(length):
	""" Create a random gene of given length """
	toReturn = []
	for i in range(0, length):
		toReturn.append(random.randint(0, 1))
	return toReturn

###### GENE STRUCTURE ######
"""
For each shape:
--- Type of shape (sphere, rectangular prism) (1 bit)
--- Origin in 3D World space (3 floats) (sizeof(float) * 3)
--- Axis of Rotation (3 floats) (sizeof(float) * 3)
--- Angle of Rotation (1 float) (sizeof(float))
--- Scale of object (3 floats) (sizeof(float) * 3)
    +++ Only first is used for radius of sphere if sphere.

Note: Most data is non-coding for spheres. All is used for cubes.
"""

class Gene:
	scale = MAX_SIZE_TEST
	def __init__(self):
		""" Initialize a default gene - random. """
		# Header data: size FLOAT_PRECISION for number of shapes.
		self.data = []
		self.data += GenerateRandomGene(FLOAT_PRECISION) # For number of shapes used in this gene.

		# Non-header data: This corresponds actually with shapes.
		for i in range(0, MAX_OBJECT_COUNT):
			self.data += GenerateRandomGene(1) # For type
			self.data += GenerateRandomGene(FLOAT_PRECISION * 3)  # Origin in world space
			self.data += GenerateRandomGene(FLOAT_PRECISION * 3) # Axis of rotation
			self.data += GenerateRandomGene(FLOAT_PRECISION) # Angle of rotation
			self.data += GenerateRandomGene(FLOAT_PRECISION * 3) # Scale of object
			# Total size per object: FLOAT_PRECISION * 10 + 1

	def Randomize(self):
		# Header data: size FLOAT_PRECISION for number of shapes.
		self.data = []
		self.data += GenerateRandomGene(FLOAT_PRECISION) # For number of shapes used in this gene.

		# Non-header data: This corresponds actually with shapes.
		for i in range(0, MAX_OBJECT_COUNT):
			self.data += GenerateRandomGene(1) # For type
			self.data += GenerateRandomGene(FLOAT_PRECISION * 3)  # Origin in world space
			self.data += GenerateRandomGene(FLOAT_PRECISION * 3) # Axis of rotation
			self.data += GenerateRandomGene(FLOAT_PRECISION) # Angle of rotation
			self.data += GenerateRandomGene(FLOAT_PRECISION * 3) # Scale of object
			# Total size per object: FLOAT_PRECISION * 10 + 1
		return self

	def GetType(self, objNum):
		if objNum < 0 or objNum >= MAX_OBJECT_COUNT:
			return "INVALID INDEX (gla->Gene::GetType)"
		index = FLOAT_PRECISION
		index += (FLOAT_PRECISION * 10 + 1) * objNum

		if self.data[index] == 0:
			return "Sphere"
		elif self.data[index] == 1:
			return "Box"
		else:
			return "B.D.I.A.G."

	def SetMaxSize(self, newSize):
		self.scale = newSize if newSize > 0 else 1

	def GetMaxSize(self):
		return self.scale

	def GetNumObjects(self):
		return int(GeneToFloat(self.data[0:FLOAT_PRECISION], float(MAX_OBJECT_COUNT) - 0.0000001)) + 1

	def GetOrigin(self, objNum):
		index = FLOAT_PRECISION + ((FLOAT_PRECISION * 10 + 1) * objNum)
		return Vect3(GeneToFloat(self.data[index+1:index+FLOAT_PRECISION+1], 5), GeneToFloat(self.data[index + FLOAT_PRECISION + 1 : index + 2 * FLOAT_PRECISION + 1], 5), GeneToFloat(self.data[index + FLOAT_PRECISION * 2 + 1 : index + 3 * FLOAT_PRECISION + 1], 5))

	def GetRotationAxis(self, objNum):
		index = FLOAT_PRECISION + ((FLOAT_PRECISION * 10 + 1) * objNum)
		return Vect3(GeneToFloat(self.data[index + 3 * FLOAT_PRECISION + 1 : index + 4 * FLOAT_PRECISION + 1], 2), GeneToFloat(self.data[index + 4 * FLOAT_PRECISION + 1 : index + 5 * FLOAT_PRECISION + 1], 2), GeneToFloat(self.data[index + 5 * FLOAT_PRECISION + 1 : index + 6 * FLOAT_PRECISION + 1], 5)).Normal()

	def GetRotationAngle(self, objNum):
		index = FLOAT_PRECISION + ((FLOAT_PRECISION * 10 + 1) * objNum)
		return GeneToFloat(self.data[index + 6 * FLOAT_PRECISION + 1 : index + 7 * FLOAT_PRECISION + 1], 2 * PI)

	def GetObjectScale(self, objNum):
		index = FLOAT_PRECISION + ((FLOAT_PRECISION * 10 + 1) * objNum)
		if(self.GetType(objNum) == 'Sphere'):
			return GeneToFloat(self.data[index + 7 * FLOAT_PRECISION + 1 : index + 8 * FLOAT_PRECISION + 1], self.scale)  # CHANGE THIS LATER
		else:
			return Vect3(GeneToFloat(self.data[index + 7 * FLOAT_PRECISION + 1 : index + 8 * FLOAT_PRECISION + 1], self.scale), GeneToFloat(self.data[index + 8 * FLOAT_PRECISION + 1 : index + 9 * FLOAT_PRECISION + 1], self.scale), GeneToFloat(self.data[index + 9 * FLOAT_PRECISION + 1 : index + 10 * FLOAT_PRECISION + 1], self.scale))

	### THE ALL IMPORTANT SCORING ALGORITHM ###
	def Score(self, scoreFunc, xmlData):
		# ScoreFunc form: Take in xmlData as first parameter, all objects in array as second parameter.
		geometryList = []
		for i in range(0, self.GetNumObjects()):
			if self.GetType(i) == 'Sphere':
				geometryList.append(Sphere(self.GetObjectScale(i), self.GetOrigin(i)))
			elif self.GetType(i) == 'Box':
				newBox = Box()
				newBox.setData(self.GetRotationAxis(i), self.GetRotationAngle(i), self.GetOrigin(i), self.GetObjectScale(i))
				geometryList.append(newBox)
			else:
				print "ERROR (gla->Gene::Score): Invalid type returned - ",self.GetType(i)
		return scoreFunc(xmlData, geometryList) / ((1 + ADD_OBJECT_COST) ** self.GetNumObjects())
	def Set(self, newData):
		if len(self.data) == len(newData):
			self.data = newData


	def __str__(self):
		toReturn = str(self.GetNumObjects())
		toReturn += " Object:" if self.GetNumObjects() == 1 else " Objects:"
		for i in range(0, self.GetNumObjects()):
			toReturn += " " + str(self.GetType(i)) + " "
		return toReturn

	def getString(self, objNum):
		index = FLOAT_PRECISION + ((FLOAT_PRECISION * 10 + 1) * objNum)
		if self.GetType(objNum) == 'Sphere':
			return "Sphere: Origin = <" + str(self.GetOrigin(objNum)) + ">, Radius = " + str(self.GetObjectScale(objNum))
		else:
			return "Box: Origin = <" + str(self.GetOrigin(objNum)) +  ">, Rotation: " + str(self.GetRotationAngle(objNum)) + " rad about <" + str(self.GetRotationAxis(objNum)) + ">, Halfsize <" + str(self.GetObjectScale(objNum)) + ">"

class gla:
	genes = []
	nGenes = 15 # Number of genes generated per population
	elite = True # Elitism means keeping the best unchanged between generations.
	mutateRate = 0.003 # Mutation rate - odds of a bit flipping.
	crossoverRate = 0.85 # Crossover rate - odds of a new gene being made up of two old ones
	immigrationRate = 0.3 # Immigration rate - this percentage of the population every generation is entirely new, random genes.
	def __init__(self, scoringFunc, meshData, numGenes = 100, elite = True, mutateRate = 0.003, crossoverRate = 0.85, immigrationRate = 0.3):
		self.score_method = scoringFunc
		self.mesh = meshData
		self.nGenes = numGenes
		self.elite = elite
		self.mutateRate = mutateRate
		self.crossoverRate = crossoverRate
		self.genes = []
		self.immigrationRate = 0.8
		for i in range(0, numGenes):
			x = Gene()
			x.Randomize()
			self.genes.append([x, x.Score(self.score_method, self.mesh)])
		Sort(self.genes)

	def __str__(self):
		toReturn = ""
		for i in self.genes:
			toReturn += str(i[1]) + ": " + str(i[0]) + "\n"
		return toReturn

	def RouletteWheel(self):
		total = 0
		for i in self.genes:
			total += i[1]
		rP = random.random() * total
		for i in self.genes:
			rP -= i[1]
			if rP < 0:
				return i
		return 0

	## Generation:
	def Generation(self):
		# If elitism is enabled, keep the very first gene.
		newGenes = []
		if self.elite is True:
			newGenes.append([self.genes[0][0], self.genes[0][1]])

		# Pick the n remaining chromosomes from crossovers of the others...
		## Method: Pick a chromosome. If a random number hits crossover rate,
		##    pick a different chromosome. Pick a position, and take everything
		##    to the left from ch1, and right from ch2.
		## After that's all done, apply mutation to every bit based on mutationRate.
		while len(newGenes) < ((1 - self.immigrationRate) * self.nGenes):
			ch1 = self.RouletteWheel()
			ch2 = ch1
			if random.random() < self.crossoverRate:
				# CLEVER HACK
				while ch2[1] == ch1[1]:
					ch2 = self.RouletteWheel()
			
			crossoverPoint = random.randint(0, len(self.genes[0][0].data))
			newGene1 = Gene()
			newGene1.Set(ch1[0].data[:crossoverPoint] + ch2[0].data[crossoverPoint:])
			newGenes.append([newGene1, newGene1.Score(self.score_method, self.mesh)])

		# Apply mutation to all but the first element
		i = 0
		for g in newGenes:
			if i == 0:
				i = 1
			else:
				for b in g[0].data:
					if random.random() < self.mutateRate:
						b = 0 if b == 1 else 1
				g[1] = g[0].Score(self.score_method, self.mesh)

		# Introduce immigrants:
		while len(newGenes) < self.nGenes:
			x = Gene()
			newGenes.append([x, x.Score(self.score_method, self.mesh)])

		# Finalize generation
		Sort(newGenes)
		self.genes = newGenes

random.seed()