from graph import Graph
import re

class DomainGraph(Graph):
	def __init__(self, filepath=None, sep=","):
		super().__init__(filepath=filepath)

		self.domain = {}
		for vertex in self.transit_mat:
			self.domain[vertex] = set()

		if filepath:
			self.__filldomain__(filepath, sep)

	def __filldomain__(self, filepath, sep=","):
		"""
			Domain specification format fostered:
			(input file format)

			o <vertex identifier> <domain values separated by given "sep">

			Example 01:
				o vertex_a 1,2,3,4,5
				o vertex_b 3,5,1
				o vertex_c 6

			You may specify the same vertex domain more than once. In
			this case, the values will be put in the same set (so repe-
			titions of a same value will be removed automatically)

			Example 02:
				o vertex_id a,b,c
				o vertex_id b,c,d,e

			vertex_id domain will be the set {a, b, c, d, e}

			If you specify a domain of a vertex which was not declared
			previously, the domain will be added but no new vertex will
			be created and a WARNING will be given.
		"""

		re_domain = re.compile(r"""
			\s*[Oo]		# Get the domain "o" identifier
			\s*([^\s]+)	# Get the vertex identifier
			\s*(.+)		# Get the domain values separated by "sep"
			""", re.VERBOSE)

		with open(filepath) as f:
			for line in f:
				match = re_domain.match(line)
				if match:
					vertex_id = match.group(1)
					domain_vals = match.group(2).split(sep=sep)

					if vertex_id not in self.domain:
						print("WARNING: vertex \"" + vertex_id + \
							"\" is not defined before domain values attribution.")
						self.domain[vertex_id] = set()

					self.domain[vertex_id].update(set(domain_vals))

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], 
			"<filepath> [sep - default to \",\"]")
		exit(1)

	try:
		sep = sys.argv[2]
		if not sep:
			raise Exception
	except:
		sep = ","

	d_graph = DomainGraph(sys.argv[1], sep)

	print(d_graph.domain)
