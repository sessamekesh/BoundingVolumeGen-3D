from geometry import *
import xml.etree.ElementTree as ET

### Parse ogre file:
### Result will be [vertexBuffer, indexBuffer]
# vertexBuffer will be a list of Vect3 objects, indexBuffer a list of faces forming triangles.
def Parse(inputFileName):
	tree = ET.parse(inputFileName)
	root = tree.getroot()

	# Okay, we have vertex and face information now.
	vertexBuffer = StripVertexData(root)
	indexBuffer = StripIndexData(root)

	return [vertexBuffer, indexBuffer]

def PrintData(inputNode, level):
	toPrint = ""
	for i in range(0, level):
		toPrint += "  "
	for child in inputNode:
		PrintData(child, level+1)

def StripVertexData(tree):
	# Get to vertex buffer element.
	vertexData = []
	for vertex in tree.iter('vertex'):
		for pos in vertex.iter('position'):
			vertexData.append(Vect3(pos.get("x"), pos.get("y"), pos.get("z")))
	return vertexData

def StripIndexData(root):
	# Get to index buffer element
	indexData = []
	for face in root.iter('faces'):
		for data in face.iter('face'):
			indexData.append([data.get("v1"), data.get("v2"), data.get("v3")])
	return indexData