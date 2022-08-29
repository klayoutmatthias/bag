
from bag.layout.objects import ViaInfo
import klayout.db as db

class ViaGenerator(object):
	"""
	An interface providing a via generator for a specific via type
	"""

	def generate_via(self, cell: db.Cell, via_def: ViaInfo) -> None:

		"""
		Creates the via geometry from the via definition inside the
		given cell.
		"""
		# NOTE: location is the one of the center

		# Parameters accepted from the via definition:
		# via_def.num_cols      number of columns
		# via_def.num_rows      number of rows
		# via_def.sp_cols       x space(!)
		# via_def.sp_rows       y space(!)
		# via_def.cut_height	via rectangle height
		# via_def.cut_width     via rectangle width
		# via_def.enc1     		lower metal, left, right, bottom, top    @@@ TODO: confirm
		# via_def.enc2     		lower metal, left, right, bottom, top    @@@ TODO: confirm

		pass

