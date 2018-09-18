import sys
sys.path.insert(0, "../basic-graph-search/Graph")

from domgraph import DomainGraph

"""
	This class runs the Arc Consistency algoithm
	(Constraint Propagation), which detects bad
	choices very fast while solving a CSP, increa-
	sing the solution speed.
"""

class ArcConsistency(DomainGraph):
	def solve(self):
		"""
			Run Arc Consistency algorithm.
		"""

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], 
			"<filepath> [separator - default is \",\"]")
		exit(1)

	try:
		sep = sys.argv[2]
		if not sep:
			raise Exception
	except:
		sep = ","

	ac = ArcConsistency(filepath=sys.argv[1], sep=sep)

	ac.print_graph()

	ac.solve()

	print(ac.domain)
