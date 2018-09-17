import copy

"""
	NxN Sudoku solver using Domain Reduction technique + 
	Minimum Remaining Value (MRV): Choose the varible with
		the current smallest domain.
	Domain Reduction Propagation Heuristic

	An application of CSP (Constraint Satisfaction Problem).
"""

class Sudoku:
	def __init__(self, filepath=None, sep=",", empty_val=0, invalid_val=-1):
		self.board = None
		self.domain_matrix = None
		self.fixed_matrix = None
		self.empty_val = empty_val
		self.invalid_val = invalid_val
		self.board_size = 0
		self.subsquare_size = -1

		if filepath is not None:
			self.read_file(filepath, sep)

	def __set_position__(self, value, x, y):
		self.board[y][x] = value

		for i in range(self.board_size):
			if self.board[y][i] == self.empty_val and \
				value in self.domain_matrix[y][i]:
				self.domain_matrix[y][i].remove(value)

		for j in range(self.board_size):
			if self.board[j][x] == self.empty_val and \
				value in self.domain_matrix[j][x]:
				self.domain_matrix[j][x].remove(value)

		x_start = self.subsquare_size * (x // self.subsquare_size)
		y_start = self.subsquare_size * (y // self.subsquare_size)
		for j in range(y_start, y_start + self.subsquare_size):
			for i in range(x_start, x_start + self.subsquare_size):
				if self.board[j][i] == self.empty_val and \
					value in self.domain_matrix[j][i]:
					self.domain_matrix[j][i].remove(value)


	def __check_position__(self, value, x, y):
		for i in range(self.board_size):
			if self.board[y][i] == value:
				return False

		for j in range(self.board_size):
			if self.board[j][x] == value:
				return False

		x_start = self.subsquare_size * (x // self.subsquare_size)
		y_start = self.subsquare_size * (y // self.subsquare_size)
		for j in range(y_start, y_start + self.subsquare_size):
			for i in range(x_start, x_start + self.subsquare_size):
				if self.board[j][i] == value:
					return False

		return True

	def __undo_position__(self, value, x, y):
		self.board[y][x] = self.empty_val

		for i in range(self.board_size):
			if i != x and self.board[y][i] == self.empty_val and \
				self.__check_position__(value, i, y):
				self.domain_matrix[y][i].update({value})

		for j in range(self.board_size):
			if j != y and self.board[j][x] == self.empty_val and \
				self.__check_position__(value, x, j):
				self.domain_matrix[j][x].update({value})

		x_start = self.subsquare_size * (x // self.subsquare_size)
		y_start = self.subsquare_size * (y // self.subsquare_size)
		for j in range(y_start, y_start + self.subsquare_size):
			for i in range(x_start, x_start + self.subsquare_size):
				if self.board[j][i] == self.empty_val and \
					self.__check_position__(value, i, j):
					self.domain_matrix[j][i].update({value})


	def __minimum_remaining_val_id__(self):
		x = self.invalid_val
		y = self.invalid_val

		cur_domain_len = len(self.domain_matrix) + 1
		for j in range(self.board_size):
			for i in range(self.board_size):
				if self.board[j][i] == self.empty_val and \
					len(self.domain_matrix[j][i]) < cur_domain_len:

					cur_domain_len = len(self.domain_matrix[j][i])
					x, y = i, j

		return x, y

	def __recursive_fill__(self, x, y):
		if x == self.invalid_val or y == self.invalid_val:
			return True

		for value in self.domain_matrix[y][x]:
			self.__set_position__(value, x, y)

			new_x, new_y = self.__minimum_remaining_val_id__()

			if self.__recursive_fill__(new_x, new_y):
				return True

			self.__undo_position__(value, x, y)

		return False

	def __dom_init_check__(self):
		for j in range(self.board_size):
			for i in range(self.board_size):
				if self.fixed[j][i]:
					self.__set_position__(self.board[j][i], i, j)

	def read_file(self, filepath, sep=","):
		with open(filepath) as f:
			self.board = []
			if sep:
				for line in f:
					self.board.append(\
						list(map(int, line.strip().split(sep))))
			else:
				for line in f:
					self.board.append(list(map(int, line.strip())))

		if not self.board:
			self.board = None
		else:
			self.board_size = len(self.board)
			self.subsquare_size = self.board_size // 3

		return self.board

	def print(self):
		for line in self.board:
			print(" ".join(map(str, line)))

	def solve(self):
		if self.board is None:
			print("Can't solve: board is empty.")
			return

		if self.board_size != len(self.board[0]):
			print("Can't solve: board is not square.")
			return

		self.domain_matrix = [[set(range(1, self.board_size + 1)) \
			for j in range(self.board_size)] \
			for i in range(self.board_size)]

		self.fixed = [[1 <= self.board[j][i] <= self.board_size \
			for i in range(self.board_size)] \
			for j in range(self.board_size)]

		# Reduce domain based on the initial state
		# of the game board
		self.__dom_init_check__()

		x, y = self.__minimum_remaining_val_id__()

		return self.__recursive_fill__(x, y)

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], 
			"<filepath> [separator - default is \",\"]")
		exit(1)

	try:
		sep = sys.argv[2]
	except:
		sep = ","

	s = Sudoku(sys.argv[1], sep=sep)
	s.print()

	print()

	s.solve()
	s.print()
