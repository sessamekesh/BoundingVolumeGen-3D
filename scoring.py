from model_parse import *
from geometry import *

"""
Scoring Function 1: For each vertex in object, compare against bounding volumes.
  Take distance, square it. Add it to total score. Return some constant times inverse
  total distance - this yields high schores for lower squared sum distances.
"""
def Score_Brute(objectData, testGeometryList):
	vertexList = objectData[0]

	# Test against first geometry...
	# Vertices alone are used.
	vertexCount = 0
	totalScore = 0

	totalArea = 0
	for geometry in testGeometryList:
		totalArea += geometry.getVolume()

	for vertex in vertexList:
		# Test an individual vertex.
		vertexCount += 1
		minDist = testGeometryList[0].DistanceToSurface(vertex)
		for geometry in testGeometryList:
			# Test closest geometry distance to point for every piece of geometry in the list.
			test = geometry.DistanceToSurface(vertex)
			if test < minDist:
				minDist = test
		totalScore += minDist ** 2
	return float(vertexCount) / (float(totalScore) + float(totalArea) + 0.0001)

"""
Scoring function 2: Find volume of model enclosed by bounding volumes,
  find volume of model not enclosed by bounding volumes, scale to
  volume of model and return some combination of the two volume values.
"""

"""
Scoring function 3: Score by percentage of faces enclosed by bounding
  volume, also factoring in size of the collision geometry. faces
  partially enclosed can be partially included as well.
"""