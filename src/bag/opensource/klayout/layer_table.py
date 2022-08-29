
import os
import re

class LayerTable(object):
	"""
	This class represents a layer mapping table (Cadence layer name/purpose -> stream layer/datatype)
	"""

	def __init__(self):
		"""
		Creates an empty table
		"""
		self.table = {}

	def add(self, name: str, purpose: str, layer: int, datatype: int) -> None:
		"""
		Adds an entry to the table

		Parameters
		----------
		name: str
			The layer name (Cadence layer name)
		purpose: str
			The layer purpose (Cadence layer purpose)
		layer: int
			The stream layer number
		datatype: int
			The stream layer datatype
		-------

		"""
		self.table[(name, purpose)] = (layer, datatype)

	def get(self, name: str, purpose: str) -> (int, int):
		"""
		Gets the stream layer / datatype number pair for a given
		layer name / purpose.

		Parameters
		----------
		name: str
			The layer name
		purpose: str
			The purpose

		Returns: (int, int)
			A tuple with stream layer and datatype number
		-------

		The method raises an exception if the layer/purpose is not a valid pair
		"""
		if (name, purpose) not in self.table:
			raise Exception("Not found in layer table: " + name + "." + purpuse)
		else:
			return self.table[(name, purpose)]

	def read(self, path: str) -> None:
		"""
		Reads a stream layer mapping file

		Parameters
		----------
		path: str
			The path of the file

		Returns
		-------

		"""
		with open(path, "r") as file:
			lnum = 0
			for line in file.readlines():
				lnum += 1
				if re.match(r"^\s*#", line):
					# ignore comment lines
					pass
				elif re.match(r"^\s*$", line):
					# ignore empty lines
					pass
				else:
					m = re.match(r"^\s*(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s*(\s+.*)?$", line)
					if not m:
						raise Exception("Invalid line " + str(lnum) + ": " + line)
					# TODO: m.group(5) gives mask color and is ignored here!
					if not m.group(5):
						self.add(m.group(1), m.group(2), int(m.group(3)), int(m.group(4)))
