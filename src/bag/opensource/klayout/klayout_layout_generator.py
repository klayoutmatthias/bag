import os

import klayout.db as db
from .layer_table import LayerTable
from .via_repository import ViaRepository
from ..layout_generator import LayoutGenerator
from bag.layout.objects import ViaInfo

class KLayoutLayoutGenerator(LayoutGenerator):

	def __init__(self, layer_table: LayerTable, via_repo: ViaRepository, dbu: float):

		self.layout = db.Layout()
		self.layout.dbu = dbu
		self.cell = None
		self.via_repo = via_repo
		self.layer_table = layer_table

	@staticmethod
	def make_generator(config: dict) -> LayoutGenerator:

		if "layermap_file" not in config:
			raise Exception("Mandatory configuration file entry missing: layermap_file")
		lm_file = config["layermap_file"] % os.environ
		layer_table = LayerTable()
		layer_table.read(lm_file)

		dbu = 0.001
		if "dbu" in config:
			dbu = config["dbu"]

		via_repo = ViaRepository(config)

		return KLayoutLayoutGenerator(layer_table, via_repo, dbu)

	def open_cell(self, name: str):
		self.cell = self.layout.create_cell(name)

	def close_cell(self, name: str):
		self.cell = None

	def create_box(self, name: str, purpose: str, box: list):
		ld = self.layer_table.get(name, purpose)
		lid = self.layout.layer(ld[0], ld[1])
		self.cell.shapes(lid).insert(db.DBox(*[db.DPoint(*b) for b in box]))

	def create_label(self, name: str, purpose: str, label: str, box: list):
		ld = self.layer_table.get(name, purpose)
		lid = self.layout.layer(ld[0], ld[1])
		# NOTE: uses bbox center for the label position, no label size
		dbox = db.DBox(*[db.DPoint(*b) for b in box])
		self.cell.shapes(lid).insert(db.DText(label, db.DTrans(dbox.center() - db.DPoint())))

	def create_instance(self, inst_lib: str, inst_cell: str, view: str, name: str, x: float, y: float, orient: str,
						num_rows: int, num_cols: int, sp_rows: float, sp_cols: float):
		if view != "layout":
			raise Exception(f"Cannot use view names other than 'layout' (got {view})")
		# @@@ TODO: need to qualify with libname in case of name clash?
		c = self.layout.cell(inst_cell)
		if not c:
			raise Exception("Hierarchy not being build bottom to top?")  # @@@
		self._create_instance(c, x, y, orient, num_rows, num_cols, sp_rows, sp_cols)

	def create_via(self, via_def: ViaInfo):
		vc = self.via_repo.get_via(self.layout, self.layer_table, via_def)
		self._create_instance(vc, via_def.loc[0], via_def.loc[1], via_def.orient, via_def.arr_ny, via_def.arr_nx, via_def.arr_spy, via_def.arr_spx)

	def write(self, lib_name: str):
		# @@@ how to provide path of file?
		self.layout.write(lib_name + ".gds")

	@staticmethod
	def _make_trans(orient: str, x: float, y: float) -> db.Trans:
		table = {
			"R0": 		db.DTrans.R0,
			"R90": 		db.DTrans.R90,
			"R180": 	db.DTrans.R180,
			"R270": 	db.DTrans.R270,
			"MX": 		db.DTrans.M0,
			"MXR90": 	db.DTrans.M45,  # @@@ TODO: confirm
			"MY": 		db.DTrans.M90,
			"MYR90": 	db.DTrans.M135  # @@@ TODO: confirm
		}
		if orient not in table:
			raise Exception(f"Invalid orientation code {orient}")
		return db.DTrans(table[orient], x, y)

	def _create_instance(self, cell: db.Cell, x: float, y: float, orient: str, num_rows: int, num_cols: int, sp_rows: float, sp_cols: float):
		if num_rows <= 1 and num_cols <= 1:
			self.cell.insert(db.DCellInstArray(cell.cell_index(), KLayoutLayoutGenerator._make_trans(orient, x, y)))
		else:
			self.cell.insert(db.DCellInstArray(cell.cell_index(), KLayoutLayoutGenerator._make_trans(orient, x, y), db.DVector(sp_cols, 0.0), db.DVector(0.0, sp_rows), num_cols, num_rows))
