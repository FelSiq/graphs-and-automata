from graph import Graph
import re

class DomainGraph(Graph):
	def __init__(self, filepath=None, sep=","):
		super().__init__(filepath=filepath)

		self.value = {}
		self.domain = {}
		for vertex in self.transit_mat:
			self.domain[vertex] = set()
			self.value[vertex] = None

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

		"""
			Value specification format fostered:
			(input file format)
			
			a <vertex identifier> <value>
			
			Where "value" may be any symbol, preferably from given vertex 
			domain. If not, this may lead to inconsistencies, and is the
			user responsibility to prevent this.
		"""

		re_domain = re.compile(r"""
			\s*[Oo]		# Get the domain "o" identifier
			\s*([^\s]+)	# Get the vertex identifier
			\s*(.+)		# Get the domain values separated by "sep"
			""", re.VERBOSE)

		re_value = re.compile(r"""
			\s*[Aa]		# Get the value "a" identifier
			\s*([^\s]+)	# Get the vertex identifier
			\s*([^\s]+)	# Get the vertex value
			""", re.VERBOSE)

		with open(filepath) as f:
			for line in f:
				match_domain = re_domain.match(line)
				match_value = re_value.match(line)
				if match_domain:
					vertex_id = match_domain.group(1)
					domain_vals = match_domain.group(2).split(sep=sep)

					if vertex_id not in self.domain:
						print("WARNING: vertex \"" + vertex_id + \
							"\" is not defined before domain values attribution.")
						self.domain[vertex_id] = set()

					self.domain[vertex_id].update(set(domain_vals))

				elif match_value:
					vertex_id = match_value.group(1)
					value = match_value.group(2)
					if vertex_id not in self.domain or value not in self.domain[vertex_id]:
						print("WARNING: value \"" + value + \
							"\" is not in vertex \"" + vertex_id + "\" domain.")
					self.value[vertex_id] = value

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
