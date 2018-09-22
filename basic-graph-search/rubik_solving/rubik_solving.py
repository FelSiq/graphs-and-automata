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

		for color in self.COLORS:
			self.__addrmat[color] = array([[i] * 5 for i in range(5)])

	def __matrot__(self, color, clockwise=True):
		"""
			Rotates a 5x5 matrix pi/2 radians (or 90 degrees)
			clockwise or counter-clockwise.
		"""
		aux_mat = array([[None] * 5 for _ in range(5)])
		mat = self.__addrmat[color]

		for i in range(5):
			for j in range(5):
				if clockwise:
					aux_mat[j, 4-i] = mat[i, j]
				else:
					aux_mat[4-j, i] = mat[i, j]

		self.__addrmat[color] = aux_mat

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
					self.config[color].append([(elem,) for elem in line])
				

	def solve(self):
		if self.config is None:
			print("Error: no configuration loaded. Please use",
				"Rubik.read_file(filepath) method to load",
				"a input file")
			return False

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
				self.config[color][counter])), sep="", end=end)
			counter = (counter + 1) % 3

	def print_sol(self):
		i = 1
		for step in self.solution:
			print(i, "\t:", step)
			i += 1

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

	r.__matrot__("W", True)
