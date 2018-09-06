from Graph.graph import Graph
from numpy import random
from numpy import array

"""
	The Beam Search algorithm is a informed-type
	search, which keeps only the  k most promising 
	states each iteration based only on the heuristic
	cost of that node (the real cost is never taken
	into account). It's pretty much like Hill Climbing,
	but with various possible paths running in parallel.

	There's no backtracking: discarded answers (ranking
	k + 1, k + 2, ...) are never recovered. Solutions,
	including optimal ones, can never been found due
	to this algorithm behavior.

	In fact, Beam Search with k = 1 is Hill Climbing.

	One could argue that if k -> +inf, then the Beam
	Search will behave just like Best-First Search. This
	is not always true, due to the fact that the Beam Search
	opens ALL adjacent vertexes of the current active ones,
	and then select k between they (in this case, because
	k -> +inf, all of then are selected and the list will
	be sorted just like the Best-First Search). The Best-
	First Search, however, select the best one each iteration,
	and does not give a chance to less promising nodes to
	show up theyr neighbors. Example:

	s0(15) -5-> s1(9) -8-> s4(2) -2-> s2(0)
	s0(15) -7-> s3(6) -2-> s5(7) -7-> s2(0)

	Suppose the graph above (the "two" s0 and "s2" are the
	same vertexes, just replicated to simply the notation).
	We start at s0 and want to reach s2. 

	Best-First Search iterations:
	#. Active list	Description:
	0. [s0] 	Start at s0
	1. [s1, s3] 	Activate s0 which holds {s1(9), s3(6)}, (sort and) pick up s3
	2. [s1, s5]	Activate s3 which holds {s5(7)}, (sort and) pick up s5
	3. [s1]		Activate s5 which holds {s2(0)}, (sort and) pick up s2
	4. [s1]		s2 is final, algorithm ends. Total cost: 7 + 2 + 7 = 16

	Beam Search (k -> +inf) iterations:
	#. Active list	Description:
	0. [s0]		Start at s0

	1. [s1, s3]	Activate s0, which holds {s1(9), s3(6)}, sort and pick all

	2. [s4, s5] 	Activate s1, holding {s4(2)}
			Activate s3, holding {s5(7)}
			Sort and pick up all

	3. [s2]		Activate s4, holding s2
			Activate s5, holding s2 (discard, as s4 already activated it)
			Sort and pick up all

	4. []		s2 is final, so algorithm ends. Total cost: 5 + 8 + 2 = 15
	

	[x]
	----------------------------------------------------------------

	It is not a complete-type search.

	The answer is not optimal.

	There's a stochastic version of Beam Search, also
	implemented in this code, which does not choose 
	necessarily the k most promising vertexes. Inste-
	ad, it uses probability to select between then. 
	The heuristic cost is used to derive a probability 
	to each vertex.
"""

class BeamSearch(Graph):
	def search(self, start, end, 
		k=5,
		stochastic=False, 
		stochastic_factor=2.0,
		full_output=False,
		track_visited=True):

		epsilon = 1.0e-8

		ans = {
			"strategy" : ("Stochastic " if (stochastic and k > 0) else "") +\
				(("Beam Search with width " +\
				(str(k) if k > 0 else "unlimited"))
				if k != 1 else "Hill Climbing") +\
				("" if track_visited else " (no visited vertex track)"),
			"found_path": [],
			"total_cost": 0.0,
			"found_answer": False,
			"visit_order": []
		}

		if track_visited:
			# Used only if tracking visited vertexes
			predecessor_track = {start : None}
			sons_activated = [start]
		else:
			# Else, predecessor info will not
			# help at identifying the found path,
			# so all paths must be saved every
			# iteration
			sons_activated = [[start]]

		# Keep track of current iteration vertexes
		activated = []

		while sons_activated:
			activated = sons_activated
			sons_activated = []

			if stochastic:
				# Used only in stochastic strategy
				selected_h_cost = []

			# First, open all the adjacent vertexes of
			# current activated vertexes
			while activated:
				aux = activated.pop()

				if track_visited:
					cur_vertex = aux
				else:
					cur_vertex = aux[-1]
					cur_path = aux

				ans["visit_order"].append(cur_vertex)

				if cur_vertex == end:
					# Some pseudocodes like to check if the end was 
					# reached while activating the vertexes. I disagree
					# with that decision. If your heuristic make some
					# sense, and the cost of the goal is 0 or a very
					# negligible value, then, while picking up the k
					# best vertexs, the answer will be popped first on
					# the next iteration. No bad algorithm decisions
					# will be implemented tonight: if this (somehow) causes 
					# some problem, then go fix your heuristic function.
					activated = []
					sons_activated = []
					ans["found_answer"] = True

					if not track_visited:
						ans["found_path"] = cur_path

				else:
					for adj_vertex in self.transit_mat[cur_vertex]:
						if not track_visited or adj_vertex not in predecessor_track:
							if track_visited:
								sons_activated.append(adj_vertex)
								predecessor_track[adj_vertex] = cur_vertex
							else:
								sons_activated.append(cur_path + [adj_vertex])

							if stochastic:
								selected_h_cost.append(self.heuristic_cost[adj_vertex])

			# Now, choose only the k best ones based only on the heuristic cost
			# If stochastic strategy is used, use probability to choosen
			# the k ones, based on its heuristic cost.
			if sons_activated:
				if not stochastic or k <= 0:
					if track_visited:
						sons_activated.sort(key = lambda vertex: 
							self.heuristic_cost[vertex])
					else:
						sons_activated.sort(key = lambda path: 
							self.heuristic_cost[path[-1]])

					if k > 0:
						sons_activated = sons_activated[:k]
				else:
					selected_h_cost = array([1.0 / (epsilon + \
						val**stochastic_factor) for val in selected_h_cost])
					selected_h_cost /= sum(selected_h_cost)

					try:
						# If tracking visited nodes, one can just
						# select random vertexes. If not, then the data
						# structure (list) does not help with random.choice,
						# so the indexes must the collected.
						aux = random.choice(sons_activated if track_visited \
							else range(len(sons_activated)),
							size=k, p=selected_h_cost, replace=False)
						if not track_visited:
							# Now, with the indexes, we must copy
							# the selected vertexes to the sons_activated
							# structure
							stoch_selected_sons = []
							for i in aux:
								stoch_selected_sons.append(sons_activated[i])
							
							sons_activated = stoch_selected_sons
						else:
							# Otherwise, our soul is free to just pick
							# up the fresh and shiny new vertexes. The only
							# concern is to remove the array data-type of aux
							# as we use [].pop() in this code.
							sons_activated = list(aux)

					except ValueError:
						# The only possible exception is when trying to
						# select k individuals in a population with size 
						# < k. In this case, simply select then all.
						aux = sons_activated
						

		if track_visited:
			# Build up the found path and total cost
			while cur_vertex != start:
				ans["found_path"].insert(0, cur_vertex)
				prev_vertex = cur_vertex
				cur_vertex = predecessor_track[cur_vertex]
				ans["total_cost"] += self.transit_mat[cur_vertex][prev_vertex]

			if cur_vertex != ans["found_path"][0]:
				ans["found_path"].insert(0, cur_vertex)
			
		else:
			# Build up the total cost
			next_vertex = start
			for i in range(1, len(ans["found_path"])):
				cur_vertex = next_vertex
				next_vertex = ans["found_path"][i]
				ans["total_cost"] += self.transit_mat[cur_vertex][next_vertex]

		if full_output:
			return ans

		return ans["found_path"]


if __name__ == "__main__":
	import sys

	if len(sys.argv) < 4:
		print("usage:", sys.argv[0], 
			"<filepath> <start> <end>",
			"[k - default to 5]",
			"[stochastic (0/1) - default to 0]",
			"[track visited (0/1) - default to 1]",
			"\n\nTip:",
			"Use a non-positive k to activate unlimited width of the Beam Search.")
		exit(1)

	g = BeamSearch(sys.argv[1])

	g.print_graph(fill_factor=5)

	try:
		k = int(sys.argv[4])
	except:
		k = 5

	try:
		stoc_flag = int(sys.argv[5])
	except:
		stoc_flag = False

	try:
		track_visited = int(sys.argv[6])
	except:
		track_visited = True

	ans = g.search(
		start=sys.argv[2],
		end=sys.argv[3],
		k=k,
		full_output=True,
		stochastic=stoc_flag,
		track_visited=track_visited)

	for attr in ans:
		print(attr, ":", ans[attr])
