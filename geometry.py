# GLA class.

import math

PI = 3.141592653

######################## 3D Vector Stuff ########################
class Vect3:
	def __init__(self, x=0, y=0, z=0):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
	def __add__(self, other):
		if type(other) is type(self):
			return Vect3(self.x + other.x, self.y + other.y, self.z + other.z)

	def __iadd__(self, other):
		if type(other) is type(self):
			self.x += other.x
			self.y += other.y
			self.z += other.z
			return Vect3(self.x, self.y, self.z)

	def __sub__(self, other):
		if type(other) is type(self):
			return Vect3(self.x - other.x, self.y - other.y, self.z - other.z)

	def __isub__(self, other):
		if type(other) is type(self):
			self.x -= other.x
			self.y -= other.y
			self.z -= other.z
			return Vect3(self.x, self.y, self.z)

	def __mul__(self, other):
		if type(other) is int or type(other) is float:
			return Vect3(self.x * other, self.y * other, self.z * other)

	def __imul__(self, other):
		if type(other) is int or type(other) is float:
			self.x *= other
			self.y *= other
			self.z *= other
			return Vect3(self.x, self.y, self.z)

	def __div__(self, other):
		if type(other) is int or type(other) is float:
			return Vect3(self.x / other, self.y / other, self.z / other)

	def __idiv__(self, other):
		if type(other) is int or type(other) is float:
			self.x /= other
			self.y /= other
			self.z /= other
			return Vect3(self.x, self.y, self.z)

	def __str__(self):
		return "<" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ">"

	def Magnitude(self):
		return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

	def SqMagnitude(self):
		return (self.x ** 2 + self.y ** 2 + self.z ** 2)

	def Normal(self):
		m = self.Magnitude()
		if m == 0:
			return Vect3(0., 0., 0.)
		return Vect3(self.x / m, self.y / m, self.z / m)

def ScalarProduct(vec1, vec2):
	return (vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z)

def VectorProduct(vec1, vec2):
	return Vect3(vec1.y * vec2.z - vec1.z * vec2.y, vec1.x * vec2.z - vec1.z * vec2.x, vec1.x * vec2.y - vec1.y * vec2.x)

##### Transform Matrix #####
class Matrix4:
	def __init__(self, inData=[]):
		if len(inData) == 4 and len(inData[0]) == 4:
			self.data = inData
		else:
			self.data = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

	def __mul__(self, other):
		if type(other) is int or type(other) is float:
			x = Matrix4(self.data)
			for row in x.data:
				for col in row:
					col *= other
			return x
		elif other.__class__.__name__ == self.__class__.__name__:
			# Matrix multiplication
			newData = []
			newData.append([self.data[0][0] * other.data[0][0] + self.data[0][1] * other.data[1][0] + self.data[0][2] * other.data[2][0] + self.data[0][3] * other.data[3][0],
				self.data[0][0] * other.data[0][1] + self.data[0][1] * other.data[1][1] + self.data[0][2] * other.data[2][1] + self.data[0][3] * other.data[3][1],
				self.data[0][0] * other.data[0][2] + self.data[0][1] * other.data[1][2] + self.data[0][2] * other.data[2][2] + self.data[0][3] * other.data[3][2],
				self.data[0][0] * other.data[0][3] + self.data[0][1] * other.data[1][3] + self.data[0][2] * other.data[2][3] + self.data[0][3] * other.data[3][3]])
			newData.append([self.data[1][0] * other.data[0][0] + self.data[1][1] * other.data[1][0] + self.data[1][2] * other.data[2][0] + self.data[1][3] * other.data[3][0],
				self.data[1][0] * other.data[0][1] + self.data[1][1] * other.data[1][1] + self.data[1][2] * other.data[2][1] + self.data[1][3] * other.data[3][1],
				self.data[1][0] * other.data[0][2] + self.data[1][1] * other.data[1][2] + self.data[1][2] * other.data[2][2] + self.data[1][3] * other.data[3][2],
				self.data[1][0] * other.data[0][3] + self.data[1][1] * other.data[1][3] + self.data[1][2] * other.data[2][3] + self.data[1][3] * other.data[3][3]])
			newData.append([self.data[2][0] * other.data[0][0] + self.data[2][1] * other.data[1][0] + self.data[2][2] * other.data[2][0] + self.data[2][3] * other.data[3][0],
				self.data[2][0] * other.data[0][1] + self.data[2][1] * other.data[1][1] + self.data[2][2] * other.data[2][1] + self.data[2][3] * other.data[3][1],
				self.data[2][0] * other.data[0][2] + self.data[2][1] * other.data[1][2] + self.data[2][2] * other.data[2][2] + self.data[2][3] * other.data[3][2],
				self.data[2][0] * other.data[0][3] + self.data[2][1] * other.data[1][3] + self.data[2][2] * other.data[2][3] + self.data[2][3] * other.data[3][3]])
			newData.append([self.data[3][0] * other.data[0][0] + self.data[3][1] * other.data[1][0] + self.data[3][2] * other.data[2][0] + self.data[3][3] * other.data[3][0],
				self.data[3][0] * other.data[0][1] + self.data[3][1] * other.data[1][1] + self.data[3][2] * other.data[2][1] + self.data[3][3] * other.data[3][1],
				self.data[3][0] * other.data[0][2] + self.data[3][1] * other.data[1][2] + self.data[3][2] * other.data[2][2] + self.data[3][3] * other.data[3][2],
				self.data[3][0] * other.data[0][3] + self.data[3][1] * other.data[1][3] + self.data[3][2] * other.data[2][3] + self.data[3][3] * other.data[3][3]])
			return newData
		elif other.__class__.__name__ == 'Vect3':
			# Vector multiplication
			return Vect3(float(self.data[0][0]) * float(other.x) + float(self.data[0][1]) * float(other.y) + float(self.data[0][2]) * float(other.z) + float(self.data[0][3]),
				float(self.data[1][0]) * float(other.x) + float(self.data[1][1]) * float(other.y) + float(self.data[1][2]) * float(other.z) + float(self.data[1][3]),
				float(self.data[2][0]) * float(other.x) + float(self.data[2][1]) * float(other.y) + float(self.data[2][2]) * float(other.z) + float(self.data[2][3]))
	def __str__(self):
		return str(self.data)

	def SetMatrix(self, orientationQuat, positionVect):
		if orientationQuat.__class__.__name__ is not 'Quat' or positionVect.__class__.__name__ is not 'Vect3':
			print "Invalid Params for SetMatrix() - Types quat,vect3 wanted, got:",orientationQuat.__class__.__name__,positionVect.__class__.__name__
			return 0

		self.data[0][0] = 1 - (2 * orientationQuat.j ** 2 + 2 * orientationQuat.k ** 2)
		self.data[0][1] = 2 * orientationQuat.i * orientationQuat.j + 2 * orientationQuat.k * orientationQuat.r
		self.data[0][2] = 2 * orientationQuat.i * orientationQuat.k - 2 * orientationQuat.j * orientationQuat.r
		self.data[0][3] = positionVect.x

		self.data[1][0] = 2 * orientationQuat.i * orientationQuat.j - 2 * orientationQuat.k * orientationQuat.r
		self.data[1][1] = 1 - (2 * orientationQuat.i ** 2 + 2 * orientationQuat.k ** 2)
		self.data[1][2] = 2 * orientationQuat.j * orientationQuat.k + 2 * orientationQuat.i * orientationQuat.r
		self.data[1][3] = positionVect.y

		self.data[2][0] = 2 * orientationQuat.i * orientationQuat.k + 2 * orientationQuat.j * orientationQuat.r
		self.data[2][1] = 2 * orientationQuat.j * orientationQuat.k - 2 * orientationQuat.i * orientationQuat.r
		self.data[2][2] = 1 - (2 * orientationQuat.i ** 2 + 2 * orientationQuat.j ** 2)
		self.data[2][3] = positionVect.z

		self.data[3][0] = 0
		self.data[3][1] = 0
		self.data[3][2] = 0
		self.data[3][3] = 1

		return self

	def Inverse(self):
		toReturn = Matrix4()

		inv = []
		inv.append(self.data[1][1] * self.data[2][2] - self.data[2][1] * self.data[1][2]) # 0
		inv.append(-self.data[0][1]  * self.data[2][2] + self.data[2][1]  * self.data[0][2])

		inv.append(self.data[0][1] * self.data[1][2] - self.data[1][1] * self.data[0][2])
		inv.append(-self.data[0][1] * self.data[1][2] * self.data[2][3] + self.data[0][1] * self.data[1][3] * self.data[2][2] + self.data[1][1] * self.data[0][2] * self.data[2][3] - self.data[1][1] * self.data[0][3] * self.data[2][2] - self.data[2][1] * self.data[0][2] * self.data[1][3] + self.data[2][1] * self.data[0][3] * self.data[1][2])
		inv.append(-self.data[1][0] * self.data[2][2] + self.data[2][0] * self.data[1][2])
		inv.append(self.data[0][0]  * self.data[2][2] - self.data[2][0]  * self.data[0][2]) # 5
		inv.append(-self.data[0][0] * self.data[1][2] + self.data[1][0]  * self.data[0][2])
		inv.append(self.data[0][0] * self.data[1][2] * self.data[2][3] - self.data[0][0] * self.data[1][3] * self.data[2][2] - self.data[1][0] * self.data[0][2] * self.data[2][3] + self.data[1][0] * self.data[0][3] * self.data[2][2] + self.data[2][0] * self.data[0][2] * self.data[1][3] - self.data[2][0] * self.data[0][3] * self.data[1][2])
		inv.append(self.data[1][0] * self.data[2][1] - self.data[2][0] * self.data[1][1])
		inv.append(-self.data[0][0] * self.data[2][1] + self.data[2][0] * self.data[0][1])
		inv.append(self.data[0][0] * self.data[1][1] - self.data[1][0]  * self.data[0][1]) # 10
		inv.append(-self.data[0][0] * self.data[1][1] * self.data[2][3] + self.data[0][0] * self.data[1][3] * self.data[2][1] + self.data[1][0] * self.data[0][1] * self.data[2][3] - self.data[1][0] * self.data[0][3] * self.data[2][1] - self.data[2][0] * self.data[0][1] * self.data[1][3] + self.data[2][0] * self.data[0][3] * self.data[1][1])
		inv.append(0.0)
		inv.append(0.0)
		inv.append(0.0)
		inv.append(self.data[0][0] * self.data[1][1] * self.data[2][2] - self.data[0][0] * self.data[1][2] * self.data[2][1] - self.data[1][0] * self.data[0][1] * self.data[2][2] + self.data[1][0] * self.data[0][2] * self.data[2][1] + self.data[2][0] * self.data[0][1] * self.data[1][2] - self.data[2][0] * self.data[0][2] * self.data[1][1]) # 15

		det = self.data[0][0] * (self.data[1][1] * self.data[2][2] - self.data[1][2] * self.data[2][1]) - self.data[0][1] * (self.data[1][0] * self.data[2][2] - self.data[1][2] * self.data[2][0]) + self.data[0][2] * (self.data[1][0] * self.data[2][1] - self.data[1][1] * self.data[2][0])
		if det == 0:
			print "ERROR - singular matrix cannot be inverted!"
		else:
			det = 1.0 / det
			for i in range(0, 4):
				for j in range(0, 4):
					toReturn.data[i][j] = inv[i * 4 + j] * det

		return toReturn

	def TransformDirn(self, inVect):
		if inVect.__class__.__name__ != 'Vect3':
			return None

		# Simply transform the direction only:
		return Vect3(float(self.data[0][0]) * float(inVect.x) + float(self.data[0][1]) * float(inVect.y) + float(self.data[0][2]) * float(inVect.z),
				float(self.data[1][0]) * float(inVect.x) + float(self.data[1][1]) * float(inVect.y) + float(self.data[1][2]) * float(inVect.z),
				float(self.data[2][0]) * float(inVect.x) + float(self.data[2][1]) * float(inVect.y) + float(self.data[2][2]) * float(inVect.z))

class Quat:
	def __init__(self, _r=0, _i=0, _j=0, _k=0):
		self.r = _r
		self.i = _i
		self.j = _j
		self.k = _k

	def __str__(self):
		return "(" + self.r + " + " + self.i + "i " + self.j + "j " + self.k + "k)"

	def Normalize(self):
		d = self.r ** 2 + self.i ** 2 + self.j ** 2 + self.k ** 2

		# If zero length, use no-rotation quat
		if d == 0:
			self.r = 1.
			self.i = 0.
			self.j = 0.
			self.k = 0.

		d = (1.0 / (d ** 0.5))
		self.r *= d
		self.i *= d
		self.j *= d
		self.k *= d

	def __mul__(self, other):
		# Multiply by a quat
		if other.__class__.__name__ == "Quat":
			toReturn = Quat()
			toReturn.r = self.r * other.r - self.i * other.i + self.j * other.j - self.k * other.k
			toReturn.i = self.r * other.i + self.i * other.r + self.j * other.k - self.k * other.j
			toReturn.j = self.r * other.j + self.j * other.r + self.k * other.i - self.i * other.k
			toReturn.k = self.r * other.k + self.k * other.r + self.i * other.j - self.j * other.i
			return toReturn
		else:
			return 0

	def __imul__(self, other):
		# multiply in a quat
		self = self * other
		return self

	def SetAxisAngle(self, axis, angle):
		# Set quaternion to axis/angle orientation given
		if axis.__class__.__name__ == 'Vect3' and (type(angle) is float or type(angle) is int):
			unitAxis = axis.Normal()
			self.r = math.cos(angle / 2)
			s = math.sin(angle / 2)
			self.i = unitAxis.x * s
			self.j = unitAxis.y * s
			self.k = unitAxis.z * s
		else:
			print "Invalid paramters - looking for Vect3, float/int, got",axis.__class__.__name__, type(angle)

##### Sphere #####
class Sphere:
	def __init__(self, rad, pos):
		if(rad > 0):
			self.radius = rad
		else:
			self.radius = 1
		self.origin = pos

	def __str__(self):
		return "Sphere Origin: (" + str(self.origin) + "), Radius: " + str(self.radius)

	def getVolume(self):
		return PI * self.radius * self.radius

	# Does the sphere contain the given point?
	def Contains(self, point):
		# Get the distance to the origin....
		dist = point - self.origin

		# If the distance is greater than the radius, return false, else true
		return True if dist.Magnitude() <= self.radius else False

	def DistanceToSurface(self, point_ws):
		# Get the distance to the origin
		dist = point_ws - self.origin

		# Subtract radius, return absolute value of that:
		return dist.Magnitude() - self.radius if (dist.Magnitude() > self.radius) else self.radius - dist.Magnitude()

##### Cube #####
class Box:
	def __init__(self):
		self.transform = Matrix4()
		self.halfSize = Vect3(1., 1., 1.)
		self.setData(Vect3(0.,0., 0.), 0.0, Vect3(0.,0.,0.), Vect3(1., 1., 1.))

	def __str__(self):
		# Output vertex list:
		vertexList = []
		toReturn = ""
		z = 0
		toReturn += "Origin"+str(self.transform)
		toReturn += "\nSize:"+str(self.halfSize)+"\n"
		for i in range(0, 8):
			vertexList.append(Vect3(self.halfSize.x * (-1 if i / 4 % 2 == 0 else 1), self.halfSize.y * (-1 if i / 2 % 2 == 0 else 1), self.halfSize.z * (-1 if i / 1 % 2 == 0 else 1)))
		for n in vertexList:
			n = self.transform * n
			toReturn += "Vertex " + str(z) + ": " + str(n) + "\n"
			z += 1
		return toReturn

	def setData(self, axis, angle, translation, hSize):
		if axis.__class__.__name__ is not 'Vect3' or type(angle) is not float or translation.__class__.__name__ is not 'Vect3' or hSize.__class__.__name__ is not 'Vect3':
			print "INVALID PARAMETERS on Box.__init__(axis, angle, translation, halfSize) - should be Vect3, float, Vect3, Vect3"
		else:
			quat = Quat()
			quat.SetAxisAngle(axis, angle)
			self.transform = Matrix4()
			self.transform.SetMatrix(quat, translation)
			self.halfSize = hSize
		return self

	def getVolume(self):
		return self.halfSize.x * self.halfSize.y * self.halfSize.z

	def Contains(self, point):
		if point.__class__.__name__ is not 'Vect3':
			print "INVALID PARAMETER on Box.Contains(point) - should be Vect3"
			return False
		
		# First, translate point to local coordinates of box:
		localPt = self.transform.Inverse() * point
		
		# Next, compare against halfSize vector. If it is inside all 3 dimensions, return true.
		#  Otherwise, return false.
		if localPt.x <= self.halfSize.x and localPt.y <= self.halfSize.y and localPt.z <= self.halfSize.z:
			return True
		else:
			return False

	def DistanceToSurface(self, point_ws):
		# First, transform into local space... I don't know why this isn't inverse...
		localPt = self.transform * point_ws

		# Now, it's in local coords. One coord will be locked to half_size, that will be closest of the three.
		xDist = abs(abs(localPt.x) - self.halfSize.x)
		yDist = abs(abs(localPt.y) - self.halfSize.y)
		zDist = abs(abs(localPt.z) - self.halfSize.z)

		closestPoint = Vect3(0., 0., 0.)

		if xDist < yDist and xDist < zDist:
			closestPoint.x = self.halfSize.x if localPt.x > 0 else -self.halfSize.x
			closestPoint.y = self.halfSize.y if localPt.y > self.halfSize.y else -self.halfSize.y if localPt.y < -self.halfSize.y else localPt.y
			closestPoint.z = self.halfSize.z if localPt.z > self.halfSize.z else -self.halfSize.z if localPt.z < -self.halfSize.z else localPt.z
		elif yDist < zDist:
			closestPoint.y = self.halfSize.y if localPt.y > 0 else -self.halfSize.y
			closestPoint.x = self.halfSize.x if localPt.x > self.halfSize.x else -self.halfSize.x if localPt.x < -self.halfSize.x else localPt.x
			closestPoint.z = self.halfSize.z if localPt.z > self.halfSize.z else -self.halfSize.z if localPt.z < -self.halfSize.z else localPt.z
		else:
			closestPoint.z = self.halfSize.z if localPt.z > 0 else -self.halfSize.z
			closestPoint.y = self.halfSize.y if localPt.y > self.halfSize.y else -self.halfSize.y if localPt.y < -self.halfSize.y else localPt.y
			closestPoint.x = self.halfSize.x if localPt.x > self.halfSize.x else -self.halfSize.x if localPt.x < -self.halfSize.x else localPt.x

		# Get this up and running. Check edges, corners, faces.

		localPt -= closestPoint

		return localPt.Magnitude()