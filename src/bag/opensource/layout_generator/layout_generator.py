
from bag.layout.objects import ViaInfo, PinInfo

class LayoutGenerator(object):

	def generate(self, lib_name: str, structure: dict):
		"""
		Generates the layout with the given library name.
		Depending on the generator this may create a file or
		a file structure.

		Parameters
		----------
		library_name : str
			The library name
		structure : dict
			The BAG2 dict containing the layout definition
		----------
		"""
		for s in structure:

			(cell, instances, shapes, vias, pins) = s[0:5]

			self.open_cell(cell)

			for i in instances:
				inst_lib = i["lib"]
				inst_cell = i["cell"]
				view = i["view"]
				name = i["name"]
				(x, y) = i["loc"]
				orient = i["orient"]
				num_rows = i["num_rows"]
				num_cols = i["num_cols"]
				sp_rows = i["sp_rows"]
				sp_cols = i["sp_cols"]
				self.create_instance(inst_lib, inst_cell, view, name, x, y, orient, num_rows, num_cols, sp_rows, sp_cols)

			for s in shapes:
				if "bbox" in s:
					(name, purpose) = s["layer"]
					bbox = s["bbox"]
					self.create_box(name, purpose, bbox)
				else:
					raise Exception("LayoutGenerator.generate assertion - unknown shape type " + repr(s))

			for v in vias:
				if not type(v) is ViaInfo:
					raise Exception("Unexpected object type in via info array")
				self.create_via(v)

			for p in pins:
				if not type(p) is PinInfo:
					raise Exception("Unexpected object type in pin info array")
				(name, purpose) = p.layer
				label = p.label
				bbox = p.bbox
				# BoxInfo to list for compatibility with shape list
				bbox = ((bbox.left, bbox.bottom), (bbox.right, bbox.top))
				make_rect = p.make_rect
				if make_rect:
					self.create_box(name, purpose, bbox)
				self.create_label(name, purpose, label, bbox)

			self.close_cell(cell)

		self.write(lib_name)

	def open_cell(self, name: str) -> None:
		"""
		This method is called when a new cell is created

		Parameters
		----------
		name : str
		 	The cell name
		----------
		"""
		pass

	def close_cell(self, name: str) -> None:
		"""
		This method is called after a new cell was created
		
		Parameters
		----------
		name : str	
		 	The cell name
		----------
		"""
		pass

	def create_box(self, name: str, purpose: str, box: list) -> None:
		"""
		This method is called to create a box on the given layer/purpose

		Parameters
		----------
		name : str
		 	The layer name
		purpose : str
			The layer purpose
		box : list
		 	A two-element tuple of tuples ((l, b), (r, t))
		-------
		"""
		pass

	def create_label(self, name: str, purpose: str, label: str, box: list) -> None:
		"""
		This method is called to create a label

		Parameters
		----------
		name : str
		 	The layer name
		purpose : str
			The layer purpose
		label : str
			The label text
		box : list
		 	A two-element tuple of tuples ((l, b), (r, t))
			specifies the bounding box of the pin shape
		-------
		"""
		pass

	def create_via(self, via_info: ViaInfo) -> None:
		"""
		This method is called to create a via

		Parameters
		----------
		via_info : ViaInfo
			The ViaInfo structure for the via to create
		-------
		"""
		pass

	def create_instance(self, inst_lib: str, inst_cell: str, view: str, name: str, x: float, y: float, orient: str,
						num_rows: int, num_cols: int, sp_rows: float, sp_cols: float) -> None:
		"""
		This method is called to create a cell instance

		Parameters
		----------
		inst_lib : str
			The library name for the cell to instantiate
		inst_cell : str
			The name of the cell to instantiate
		view : str
			The name of the view to instantiate
		name : str
			The name of the instance
		x : float
			The x position of the instance
		y : float
			The y position of the instance
		orient : str
			The orienation ("R0", "R90", ... in Cadence notation)
		num_rows : int
			(if array) The number of rows
		num_cols : int
			(if array) The number of columns
		sp_rows : float
			(if array) The row spacing (pitch)
		sp_cols : float
			(if array) The column spacing (pitch)
		-------
		"""
		pass

	def write(self, lib_name: str) -> None:
		"""
		Writes the layout

		Parameters
		----------
		lib_name : str
			The name of the library to generate
		-------
		"""
		pass
