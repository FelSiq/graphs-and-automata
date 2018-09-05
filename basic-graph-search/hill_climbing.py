from Graph.graph import Graph

"""
	Hill-Climbing (HC) implementation. This algorithm
	is a informed search which does not allow backtracking.

	Each step, HC move to the next step with the smallest
	heuristic cost. True costs are never taken into account.

	Just like its name, this algorithm is like climbing
	a hill - step by step - expecting to reach the goal.

	Due to its nature, HC is not a complete search algorithm.

	The answer is not optimal.

	This algorithm has problems with "Plateaus" and local
	optimum states.

	There are variations of Hill Climbing implementation. The
	original implementation, as described above, is identifi-
	ed in this code by "DF" (which stands for "DEFAULT").

	- ST ("STOCHASTIC"): chooses, at random, a neighbor bet-
		ween the ones better than the current state. The
		probability of each neighbor may depend to each 
		state heuristic value. It introduces non-determin-
		ism to the algorithm.

	- FC ("FIRST CHOICE"): choose the first neighbor that
		has better heuristic cost than the current node.
		Good when the number of neighbors is big.

	- RR ("RANDOM RESTART"): runs Hill Climbing algorithm
		k times, each time with a random starting point.
		At the end of the k iterations, the best answer
		between the iterations is returned.
"""

class HillClimbing(Graph):
	def search(self, start, end, strategy="DF", full_output=True):

		if strategy not in ("DF", "ST", "FC"):
			print("Error: unknown strategy",
				"selected (\"" + strategy + "\")")
			return None

		return None

	def random_restart(self, k=5, full_output=False):
		return None

if __name__ == "__main__":
	import sys
	
	if len(sys.argv) < 3:
		print("usage: " + sys.argv[0] + " <filepath> <strategy>",
			"Strategy availables are:",
			"\t\"DF\" (\"DEFAULT\"): standard HC implementation.",
			"\t\"ST\" (\"STOCHASTIC\"): HC choose a random better" +\
				" neighbor, not necessarily the best one.",
			"\t\"FC\" (\"FIRST CHOICE\"): HC choose the first better" +\
				" neighbor of each state (good when # of neighbors are big)",
			"\t\"RR\" (\"RANDOM RESTART\"): HC runs for k times, each one"+\
				" starting at a random point. The best global answer is returned.",
			"\nAdditional paramaters:\n",
			"If selected strategy is \"RR\":",
			"\t[iterations (default to 5)]",
			"Otherwise:",
			"\t<start> <end>", sep="\n")
		exit(1)

	g = HillClimbing(sys.argv[1])

	strategy = sys.argv[2].upper()

	ans = None
	if strategy in ("DF", "ST", "FC"):

		if len(sys.argv) < 5:
			print("Error: missing parameters for \""+
				strategy + "\" search strategy. (tip: run",
				"this script without parameters to get",
				"usage information)")
			exit(3)

		ans = g.search(
			start=sys.argv[3], 
			end=sys.argv[4],
			strategy=strategy,
			full_output=True)

	elif strategy == "RR":
		try:
			k = int(sys.argv[3])
		except:
			k = 5

		ans = g.random_restart(k=k, full_output=True)
	else:
		print("Error: unknown strategy",
			"selected (\"" + strategy + "\")")
		exit(2)

	if ans is not None:
		for attr in ans:
			print(attr, ":", ans[attr])

