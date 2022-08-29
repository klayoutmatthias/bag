
from .via_generator import ViaGenerator
from .layer_table import LayerTable
import klayout.db as db
from bag.layout.objects import ViaInfo

class StandardViaGenerator(ViaGenerator):

	"""
	ViaGenerator implementation for the standard via

	Standard vias are defined by a lower layer, a cut layer and an upper layer.
	"""

	def __init__(self, lower_metal: (str, str), via: (str, str), upper_metal: (str, str)):
		self.lower_metal = lower_metal
		self.via = via
		self.upper_metal = upper_metal

	def generate_via(self, cell: db.Cell, via_def: ViaInfo, layer_table: LayerTable) -> None:

		layout = cell.layout()

		lower_metal_ld = layer_table.get(*self.lower_metal)
		via_ld = layer_table.get(*self.via)
		upper_metal_ld = layer_table.get(*self.upper_metal)

		lower_metal_lid = layout.layer(*lower_metal_ld)
		via_lid = layout.layer(*via_ld)
		upper_metal_lid = layout.layer(*upper_metal_ld)

		w = via_def.num_cols * via_def.cut_width + (via_def.num_cols - 1) * via_def.sp_cols
		h = via_def.num_rows * via_def.cut_height + (via_def.num_rows - 1) * via_def.sp_rows

		(l, r, b, t) = via_def.enc1
		cell.shapes(lower_metal_lid).insert(db.DBox(-0.5 * w - l, -0.5 * h - b, 0.5 * w + r, 0.5 * h + t))

		(l, r, b, t) = via_def.enc2
		cell.shapes(upper_metal_lid).insert(db.DBox(-0.5 * w - l, -0.5 * h - b, 0.5 * w + r, 0.5 * h + t))

		px = via_def.sp_cols + via_def.cut_width
		py = via_def.sp_rows + via_def.cut_height
		for i in range(0, via_def.num_cols):
			for j in range(0, via_def.num_rows):
				via_box = db.DBox(0, 0, via_def.cut_width, via_def.cut_height)
				via_box.move(i * px, j * py)
				via_box.move(-0.5 * w, -0.5 * h)
				cell.shapes(via_lid).insert(via_box)

