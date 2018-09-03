import re

class Graph:
	def __init__(self, filepath=None):
		self.transit_mat = {}
		self.heuristic_cost = {}
		self.cartesian_pos = {}
		self.directed = False

		if filepath is not None:
			self.__readfile__(filepath)

	def __add_vertex__(self, name, x=0.0, y=0.0):
		self.transit_mat[name] = {}
		self.cartesian_pos[name] = (
			float(x) if x else 0.0, 
			float(y) if y else 0.0)

	def __add_edge__(self, v_a, v_b, w=1.0):
		if v_a not in self.transit_mat:
			self.transit_mat[v_a] = {}

		if v_b not in self.transit_mat:
			self.transit_mat[v_b] = {}

		self.transit_mat[v_a][v_b] = float(w)
		if not self.directed:
			self.transit_mat[v_b][v_a] = float(w)

	def __add_heuristic_cost__(self, v, cost):
		self.heuristic_cost[v] = float(cost)

	def __readfile__(self, filepath):
		"""
		Adopted notation (always a single command per line):

		# [commentary]:		line is a commentary and is disconsidered.

		v <name> [x] [y]: 	line is a vertex. "x" and "y" are cartesian
					coordinates for that vertex. Default value
					is (x, y) = (0, 0).

		e <va> <vb> [w]: 	line is a new edge between edges "va" and 
					"vb" with weight "w". Default "w" value is 1.0.

		h <v> <cost>:		heuristic "cost" of vertex "v". Is optional.
					Default value of each vertex is 0.

		d:			Flag to toggle "directed" property. In this
					case, all edges will be inserted only once in
					the transition matrix, turning it into a non-
					symmetric matrix
		"""
		
		# Regex: remove commentaries
		re_rem_commentaries = re.compile(r"^\s*#.*$")

		# Regex: get vertex properties
		re_vertex = re.compile(r"""
			\s*[Vv]		# Get vertex "v" identifier
			\s*([^\s]+) 	# Get vertex name
			\s*([^\s]+)?	# Get vertex x coordinate
			\s*([^\s]+)?	# Get vertex y coordinate
			""", re.VERBOSE)

		# Regex: get edge properties
		re_edge = re.compile(r"""
			\s*[Ee]		# Get edge "e" identifier
			\s*([^\s]+)	# Get vertex a identifier
			\s*([^\s]+)	# Get vertex b identifier
			\s*([^\s]+)?	# Get edge weight
			""", re.VERBOSE)

		# Regex: get heuristic cost
		re_heuristic = re.compile(r"""
			\s*[Hh]		# Get heuristic "h" identifier
			\s*([^\s]+)	# Get vertex identifier
			\s*([^\s]+)	# Get vertex heuristic cost
			""", re.VERBOSE)

		# Regex: get "directed" property
		re_directed = re.compile(r"""
			\s*[Dd]		# Get "d" flag for "directed"
			""", re.VERBOSE)

		with open(filepath) as f:
			for line in f:
				if line != "" and not re_rem_commentaries.match(line):
					e_match = re_edge.match(line)
					v_match = re_vertex.match(line)
					h_match = re_heuristic.match(line)
					d_match = re_directed.match(line)

					if e_match:
						data = e_match.groups()
						self.__add_edge__(*data)
					elif v_match:
						data = v_match.groups()
						self.__add_vertex__(*data)
					elif h_match:
						data = h_match.groups()
						self.__add_heuristic_cost__(*data)
					elif d_match:
						self.directed = not self.directed

	def print_graph(self):
		sorted_transit_keys = sorted(self.transit_mat.keys())

		print(8 * " ", end=" ")
		for v in sorted_transit_keys:
			print("{val:<{fill}}  ".format(val=v, fill=8), end="")
		print()

		for v_a in sorted_transit_keys:
			print("{val:<{fill}}".format(val=v_a, fill=8), end=":")
			cur_vertex = self.transit_mat[v_a]
			for v_b in sorted_transit_keys:
				print("[{val:<{fill}}]".format(
					val=(cur_vertex[v_b] if v_b in cur_vertex else ""), 
					fill=8), end="")
			print()


if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], "<filepath>")
		exit(1)

	g = Graph(sys.argv[1])

	g.print_graph()
