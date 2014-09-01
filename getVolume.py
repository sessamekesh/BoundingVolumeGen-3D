# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# (I took this from https://projects.blender.org/tracker/download.php/153/467/32555/22041/mesh_volume_tools.py)
# Really - the only modifications I made were so that this runs in my app instead of Blender.

from model_parse import *
import math

INPUT_FILE = "Resources/Cube.001.mesh.xml"
OUTPUT_FILE = "./Run.txt"
FILE_DATA = Parse(INPUT_FILE)

above = 0.
below = 0.

# File Data: vertices, then indices (in sets of three)
def dir_range(normal, mesh, mesh_to_world):
	"""Given an object and a normal defining a plane at the origin,
	returns the lowest and highest distances from the plane."""
	# Initialize with the first vertex...
	dist0 = ScalarProduct(normal, mesh_to_world * mesh[0][0])
	low = dist0
	high = dist0

	for i in range(1, len(mesh[0])):
		d = ScalarProduct(normal, mesh_to_world * mesh[0][i])
		if d < low:
			low = d
		if d > high:
			high = d

	return (low, high)

def intersect_line_plane(pt0, pt1, plane_coord, plane_normal, epsilon=0.0000001):
	u = pt1 - pt0
	w = pt0 - plane_coord
	dot = ScalarProduct(plane_normal, u)

	if abs(dot) > epsilon:
		""" The factor of the point between p0 -> p1. If (0-1), the point intersects
		with the segment. If not: it's either behind p0 or in front of p1."""
		fac = -ScalarProduct(plane_normal, w) / dot
		u *= fac
		return pt0 + u
	else:
		return None

def area_tri(v1, v2, v3):
	# Calculate area of projected triangle...
	side1 = abs((v1-v2).Magnitude())
	side2 = abs((v2-v3).Magnitude())
	side3 = abs((v3-v1).Magnitude())

	# Apply Heron's formula...
	s = (side1 + side2 + side3) / 2.
	area = (s * (s - side1) * (s - side2) * (s - side3)) ** 0.5
	return area

def getFaceNormal(p1, p2, p3):
	"""Input three vertices - output normal of those vertices in outward
	direction. This "outward direction" depends on the winding - they are
	wound clockwise."""
	return VectorProduct(p2 - p1, p3 - p1)

def volumeSplitPlane(normal, dist, mesh, mesh_to_world):
	"""Given a plane and a (clean, triangulated) mesh, returns
	a tuple (below, above) of the volume of the plane above and
	below the mesh. Plane is defined in world space with a normal
	and distance from the origin."""
	global below
	global above
	below = 0.
	above = 0.

	def height_to_vol(h1, h2, h3, area, sign):
		"""Given three heights, all positive or negative, updates below/above
		accordingly, making use of the projected triangle area..."""
		global below
		global above
		change = sign 
		change *= area
		change *= (h1 + h2 + h3) / 3.0

		if(h1 + h2 + h3) > 0.0:
			above += change
		else:
			below += change

	def do_face(v1, v2, v3, norm):
		"""Process a triangle"""
		# Start by getting its vertices...
		v1 = mesh_to_world * v1
		v2 = mesh_to_world * v2
		v3 = mesh_to_world * v3

		# Calculate distances to the plane...
		h1 = ScalarProduct(normal, v1) - dist
		h2 = ScalarProduct(normal, v2) - dist
		h3 = ScalarProduct(normal, v3) - dist

		# Project them back to the plane
		p1 = v1 - normal * h1
		p2 = v2 - normal * h2
		p3 = v3 - normal * h3

		# Check if the face is all on one side of the plane - the simple case...
		ph1 = h1 > 0.
		ph2 = h2 > 0.
		ph3 = h3 > 0.

		sign = 1. if ScalarProduct(normal, norm) > 0. else -1.

		if ph1 == ph2 and ph1 == ph3:
			area = area_tri(p1, p2, p3)

			# Make the update...
			height_to_vol(h1, h2, h3, area, sign)
		else:
			# Complex scenario: need to chop triangle into 3, where
			#  each is entirely on one side of the plane, handle each in turn...
			# Switch around vertices so that both v2 and v3 are on same side.
			if ph2 != ph3:
				if ph1 == ph2:
					v1, v3 = v3, v1
					h1, h3 = h3, h1
					p1, p3 = p3, p1
				else: #ph1 == ph3
					v1, v2 = v2, v1
					h1, h2 = h2, h1
					p1, p2 = p2, p1

			# Intercept the lines v1 - v2 and v1 - v3 with the plane...
			il2 = intersect_line_plane(v1, v2, normal * dist, normal)
			il3 = intersect_line_plane(v1, v3, normal * dist, normal)
			assert(il2 != None and il3 != None)

			# We have defined three triangles - pass each to the height_to_vol in turn:
			area = area_tri(p1, il2, il3)
			height_to_vol(h1, 0., 0., area, sign)

			area = area_tri(il2, p2, p3)
			height_to_vol(0., h2, h3, area, sign)

			area = area_tri(il2, p3, il3)
			height_to_vol(0., h3, 0., area, sign)

	# Process each triangle in the mesh in turn...
	for face in mesh[1]:
		norm = mesh_to_world.TransformDirn(getFaceNormal(mesh[0][int(face[0])], mesh[0][int(face[1])], mesh[0][int(face[2])]))
		norm = norm.Normal()

		do_face(mesh[0][int(face[0])], mesh[0][int(face[1])], mesh[0][int(face[2])], norm)

	return (below, above)

def findTotalVolume(mesh_data, mesh_transform):
	a, b = volumeSplitPlane(Vect3(0., 0., 1.), 0., mesh_data, mesh_transform)
	return a + b

def findVolumeData(mesh_data, mesh_transform, geometry_list):
	"""
	Returns: (totalVolume, includedVolume, excludedVolume, unusedVolume)

	Finds the volume enclosed by a group of binding geometry.
	-- Find vertex and index information for binding geometry.
	-- Create a "bound" list from the model geometry. If all three
	   points on a face are inside the bounding geometry, use that
	   face. If all three are outside the geometry, use instead the projection
	   of that face onto the collision geometry.
	-- Calculate the volume of the new included geometry.

	-- totalVolume is just the volume of the object
	-- includedVolume is the volume of the new included geometry
	-- excludedVolume is the volume of the object minus included volume
	-- unusedVolume is the geometry volume minus included volume
	"""

	totalVolume = findTotalVolume(mesh_data, Matrix4())

	# Generate list of included volume.
	includedGeometry = [[], []]

	# Vertices:
	for vert in mesh_data[0]:
		for geo in geometry_list:
			if(geo.Contains(mesh_data[0])):
				includedGeometry[0].append(vert)
			
	for face in mesh_data[1]:
		enc = [False, False, False]
		for geo in geometry_list:
			if(geo.Contains(mesh_data[0][face[0]])): enc[0] = True
			if(geo.Contains(mesh_data[0][face[1]])): enc[1] = True
			if(geo.Contains(mesh_data[0][face[2]])): enc[2] = True

		# Test for the simple case - all three verts enclosed by geometry.
		if enc[0] is True and enc[1] is True and enc[2] is True:
			includedGeometry[1].append()


print volumeSplitPlane(Vect3(0., 0., 1.), 0., FILE_DATA, Matrix4())
print findTotalVolume(FILE_DATA, Matrix4())