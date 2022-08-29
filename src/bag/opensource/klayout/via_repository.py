
from .layer_table import LayerTable
from .standard_via_generator import StandardViaGenerator
import klayout.db as db
from bag.layout.objects import ViaInfo

class ViaRepository(object):

	def __init__(self, config):

		if "via_definitions" not in config:
			return

		self.table = {}
		self.via_cache = {}

		vd = config["via_definitions"]
		for id in vd.keys():
			# TODO: too cheap? Error checking?
			self.table[id] = StandardViaGenerator(*vd[id])

	def get_via(self, layout: db.Layout, layer_table: LayerTable, via_def: ViaInfo) -> db.Cell:
		# TODO: more efficient way of hashing?
		# TODO: we do not encode enclosure but assume it is identical for identical configuration
		via_key = f"{via_def.id},{via_def.num_cols},{via_def.num_rows},{via_def.sp_cols},{via_def.sp_rows},{via_def.cut_height},{via_def.cut_width}"
		if via_key not in self.via_cache:
			vc = self._make_via_cell(layout, layer_table, via_def)
			self.via_cache[via_key] = vc
		else:
			vc = self.via_cache[via_key]
		return vc

	def _make_via_cell(self, layout: db.Layout, layer_table: LayerTable, via_def: ViaInfo) -> db.Cell:
		cell = layout.create_cell(via_def.id)
		if via_def.id not in self.table:
			raise Exception(f"Not a valid via ID: {via_def.id}")
		self.table[via_def.id].generate_via(cell, via_def, layer_table)
		return cell

