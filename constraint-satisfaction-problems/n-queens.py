from numpy import random
"""
	N-queens problem is a classic Constraint Satisfaction Problem.
	This implementation solves it using Min-Conflicts Heuristic,
	where all queens are initialized at a random position and
	for every iteration a random selected queen which violates 
	the problem constraint (queens can't attack each other) is
	moved to the position with less conflicts (less number of
	other queens attack). This movement is repeated until all
	queens are at a safe position. 

"""
class Queens:
	def __init__(self, n=8):
		self.pos = None

		if n > 0:
			self.solve(n)

	def __check_consistency__(self, n):
		conflict_list = []
		for i in range(n):
			for j in range(n):
				if i != j:
					if self.pos[i] == self.pos[j] or \
						abs((self.pos[i] - self.pos[j])/(i - j)) == 1:
						conflict_list += [j, i]

		return random.choice(list(set(conflict_list))) if conflict_list else -1

	def __minimum_conflict_pos__(self, queen_id, n):
		conflict_counter = [0] * n

		# Maximum value possible, equivalent to
		# infinity in this problem
		conflict_counter[self.pos[queen_id]] = n
	
		for i in range(n):
			if i != self.pos[queen_id]:
				for j in range(n):
					if j != queen_id:
						# Check horizontal conflicts
						conflict_counter[i] += self.pos[j] == i
						# Check diagonal conflicts
						conflict_counter[i] += abs((self.pos[j] - i)\
							/(j - queen_id)) == 1

		min_conflict_pos = self.pos[queen_id]
		for i in range(len(conflict_counter)):
			if conflict_counter[min_conflict_pos] > conflict_counter[i]:
				min_conflict_pos = i

		return min_conflict_pos

	def solve(self, n=8):
		# Init all queens at random positions
		self.pos = [random.randint(n)] * n

		conflicted_id = 0
		while conflicted_id != -1:
			conflicted_id = self.__check_consistency__(n)
			if conflicted_id != -1:
				new_queen_pos = \
					self.__minimum_conflict_pos__(conflicted_id, n)
				self.pos[conflicted_id] = new_queen_pos

		return self.pos

	def print(self):
		for i in range(len(self.pos)):
			for queen_pos in self.pos:
				print("Q" if i == queen_pos \
					else "_", end="")
			print()
			

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], "[n - default to 8]")
		exit(1)

	try:
		n = int(sys.argv[1])
		if n <= 0:
			print("Warning: \"n\" must be a positive integer")
			raise Exception
		if n in {2, 3}:
			print("Warning: \"n\" can't be neither 2 nor 3!")
			raise Exception
	except:
		n = 8

	Queens(n).print()
	
