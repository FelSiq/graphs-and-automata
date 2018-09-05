from Graph.graph import Graph
from numpy import random as rd

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
		has better heuristic cost than the current vertex.
		Good when the number of neighbors is big.

	- RR ("RANDOM RESTART"): runs Hill Climbing algorithm
		k times, each time with a random starting point.
		At the end of the k iterations, the best answer
		between the iterations is returned.
"""

class HillClimbing(Graph):
	def search(self, start, end, 
		strategy="DF", 
		stochastic_factor=2.0, 
		full_output=True, 
		sort_edges=True):

		if strategy not in ("DF", "ST", "FC"):
			print("Error: unknown strategy",
				"selected (\"" + strategy + "\")")
			return None

		if strategy == "ST":
			strategy_desc = "Stochastic"
		elif strategy == "FC":
			strategy_desc = "First Choice"
		else:
			strategy_desc = "Default"

		ans = {
			"strategy:" : "Hill Climbing" +\
				" (version \"" + strategy_desc + "\")", 
			"total_cost" : 0.0,
			"found_path" : [],
			"found_goal" : False,
			"edges_sorted" : sort_edges
		}
		# Fun fact: in HC, the "found_path" is exactly
		# the "visit_order" vector.

		# Hill Climbing is Beam Search with k=1,
		# which means that it don't need to keep
		# a activated vertex list, as it is a
		# greedy algorithm without backtracking.
		next_vertex = start

		while next_vertex:
			cur_vertex = next_vertex
			
			ans["found_path"].append(cur_vertex)

			if cur_vertex == end:
				next_vertex = None
				ans["found_goal"] = True

			else:
				if strategy == "ST":
					# Used just for STOCHASTIC strategy
					total_h_cost = 0.0
					better_neighbors = []
					neighbor_prob = []

				edges_list = self.transit_mat[cur_vertex].keys()
				if sort_edges:
					edges_list = sorted(edges_list)

				for adj_vertex in edges_list:
					# Note: if operator "<" is substitued by "<=", then the
					# algorithm will walk in plateaus instead of stopping when
					# it reaches one.
					if self.heuristic_cost[adj_vertex] < self.heuristic_cost[next_vertex]:
						if strategy != "ST":
							next_vertex = adj_vertex
						else:
							# If "Stochastic" strategy is used, each
							# better adjacent vertex has a probability
							# to be selected. This probability depends
							# on how promissing each vertex is (i.e how
							# small is its heuristic cost)
							total_h_cost += self.heuristic_cost[adj_vertex]
							better_neighbors.append(adj_vertex)
							neighbor_prob.append(self.heuristic_cost[adj_vertex])
						
						# If strategy is "First Choice", stop searching
						# for a better neighbor.
						if strategy == "FC":
							break

				if strategy == "ST" and len(better_neighbors):
					if end not in better_neighbors:
						# If we not found the desired end, pick a random next
						# state based on its heurist cost
						neighbor_prob = [total_h_cost / (val**stochastic_factor) for val in neighbor_prob]
						neighbor_prob = [val / sum(neighbor_prob) for val in neighbor_prob]
						next_vertex = rd.choice(better_neighbors, size=1, p=neighbor_prob)[0]
					else:
						# Otherwise, we're done.
						next_vertex = end

				if next_vertex == cur_vertex:
					next_vertex = None
				else:
					ans["total_cost"] += self.transit_mat[cur_vertex][next_vertex]
		
		if full_output:
			return ans

		return ans["found_path"]

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

	g.print_graph(fill_factor = 5)

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

