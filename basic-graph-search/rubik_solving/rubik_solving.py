from numpy import array
"""
	An application of A* algorithm.
"""

class Rubik:
	def __init__(self, filepath=None, sep=None):
		self.config = None
		self.COLORS = ("W", "Y", "G", "R", "B", "O")
		self.solution = []
		self.__addrmat = None

		if filepath is not None:
			self.read_file(filepath, sep=None)
			self.__buildaddressmat__()

	def __buildaddressmat__(self):
		
		if self.config is None:
			return

		self.__addrmat = {}

		"""
			Mapping here (last step to finally apply A* and solve...)
			     [ O ]
			     [ B ]
			[ W ][ R ][ Y ]
			     [ G ]
		"""

		# Aux variable to reduce code verbosity level
		cb = self.config["B"]
		cr = self.config["R"]
		co = self.config["O"]
		cw = self.config["W"]
		cy = self.config["Y"]
		cg = self.config["G"]

		self.__addrmat["G"] = [
			[[None], cw[0, 0], cw[1, 0], cw[2, 0], [None]],
			[co[0, 2], cg[0, 0], cg[0, 1], cg[0, 2], cr[0, 0]],
			[co[1, 2], cg[1, 0], cg[1, 1], cg[1, 2], cr[1, 0]],
			[co[2, 2], cg[2, 0], cg[2, 1], cg[2, 2], cr[2, 0]],
			[[None], cy[2, 0], cy[1, 0], cy[0, 0], [None]],
		]

		self.__addrmat["O"] = [
			[[None], cw[0, 2], cw[0, 1], cw[0, 0], [None]],
			[cb[0, 2], co[0, 0], co[0, 1], co[0, 2], cg[0, 0]],
			[cb[1, 2], co[1, 0], co[1, 1], co[1, 2], cg[1, 0]],
			[cb[2, 2], co[2, 0], co[2, 1], co[2, 2], cg[2, 0]],
			[[None], cy[2, 0], cy[2, 1], cy[2, 2], [None]],
		]

		self.__addrmat["B"] = [
			[[None], cw[2, 2], cw[1, 2], cw[0, 2], [None]],
			[cr[0, 2], cb[0, 0], cb[0, 1], cb[0, 2], co[0, 0]],
			[cr[1, 2], cb[1, 0], cb[1, 1], cb[1, 2], co[1, 0]],
			[cr[2, 2], cb[2, 0], cb[2, 1], cb[2, 2], co[2, 0]],
			[[None], cy[0, 2], cy[1, 2], cy[2, 2], [None]],
		]

		self.__addrmat["Y"] = [
			[[None], cr[2, 0], cr[2, 1], cr[2, 2], [None]],
			[cg[2, 2], cy[0, 0], cy[0, 1], cy[0, 2], cb[2, 0]],
			[cg[2, 1], cy[1, 0], cy[1, 1], cy[1, 2], cb[2, 1]],
			[cg[2, 0], cy[2, 0], cy[2, 1], cy[2, 2], cb[2, 2]],
			[[None], co[2, 2], co[2, 1], co[2, 0], [None]],
		]

		self.__addrmat["R"] = [
			[[None], cw[2, 0], cw[2, 1], cw[2, 2], [None]],
			[cg[0, 2], cr[0, 0], cr[0, 1], cr[0, 2], cb[0, 0]],
			[cg[1, 2], cr[1, 0], cr[1, 1], cr[1, 2], cb[1, 0]],
			[cg[2, 2], cr[2, 0], cr[2, 1], cr[2, 2], cb[2, 0]],
			[[None], cy[0, 0], cy[0, 1], cy[0, 2], [None]],
		]

		self.__addrmat["W"] = [
			[[None], co[0, 2], co[0, 1], co[0, 0], [None]],
			[cg[0, 0], cw[0, 0], cw[0, 1], cw[0, 2], cb[0, 2]],
			[cg[0, 1], cw[1, 0], cw[1, 1], cw[1, 2], cb[0, 1]],
			[cg[0, 2], cw[2, 0], cw[2, 1], cw[2, 2], cb[0, 0]],
			[[None], cr[0, 0], cr[0, 1], cr[0, 2], [None]],
		]

		return

	def __matrot__(self, color, clockwise=True):
		"""
			Rotates a 5x5 matrix pi/2 radians (or 90 degrees)
			clockwise or counter-clockwise.
		"""
		aux_mat = array([[None] * 5 for _ in range(5)])
		mat = self.__addrmat[color]

		for i in range(5):
			for j in range(5):
				# Choosen the position + deference 
				# pointer (last "0" index)
				if clockwise:
					aux_mat[j, 4-i] = mat[j][i][0]
				else:
					aux_mat[4-j, i] = mat[j][i][0]

		# Change the values of the configuration via the
		# addrmat pointers. The main idea is that, as we are
		# using pointers, the values will be correctly updated
		# in every cube's face.
		for i in range(5):
			for j in range(5):
				self.__addrmat[color][j][i][0] = aux_mat[i, j]

		return

	def read_file(self, filepath, sep=None):
		"""
			Consider a Rubik Cube in the model:

			     [ O ]
			     [ B ]
			[ W ][ R ][ Y ]
			     [ G ]

			The input file is formed by six 3x3 side-by-side
			configuration.

			The sequence of colors in input file is
			I.	"W" for "White"
			II.	"Y" for "Yellow"
			III.	"G" for "Green"
			IV.	"R" for "Red"
			V.	"B" for "Blue"
			VI.	"O" for "Orange"

			The colors may or may not be separated with a se-
			parator character. In this case, that separator must
			be specified in the correspondent command line argu-
			ment before execution or given correctly as method
			argument.

		"""

		with open(filepath) as f:
			self.config = {}
			for color in self.COLORS:
				# Init the i side of the cube
				self.config[color] = []

				# This program is limited to 3x3x3 Rubik's cube
				# for simplicity
				for row in range(3):
					line = f.readline().strip().upper()
					if sep is not None:
						line = "".join(line.split(sep))

					# Each element must be a data structure to
					# simulate a pointer, as the address (and not
					# the value) will be necessary to make moves
					self.config[color].append([[elem] for elem in line])

				self.config[color] = array(self.config[color])

		return
				

	def solve(self):
		if self.config is None:
			print("Error: no configuration loaded. Please use",
				"Rubik.read_file(filepath) method to load",
				"a input file")
			return False

		"""
			Apply A* here and find a solution.
		"""

	def print(self):
		COLORS_PRINT_SEQ =\
			("O",) * 3 +\
			("B",) * 3 +\
			("W", "R", "Y") * 3 +\
			("G",) * 3

		if set(COLORS_PRINT_SEQ).difference(self.config):
			print("Error: bad configuration loaded,",
				"unknown color given.")
			return

		counter = 0
		for color in COLORS_PRINT_SEQ:
			offset = " " * (6 if color in {"O", "B", "G"} else 0)
			end = "\n" if color in ("O", "B", "Y", "G") else " "

			print(offset, " ".join(map(lambda k: str(k[0]), 
				self.config[color][counter,:])), sep="", end=end)

			if end == "\n":
				counter = (counter + 1) % 3

		return

	def print_sol(self):
		i = 1
		for step in self.solution:
			print(i, "\t:", step)
			i += 1

		return

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], "<filepath> [separator - default to None]")
		exit(1)

	try:
		sep = sys.argv[2]
	except:
		sep = None

	r = Rubik(sys.argv[1], sep)

	r.print()

	r.solve()

	print("\nStep-by-step Solution:")
	r.print_sol()
