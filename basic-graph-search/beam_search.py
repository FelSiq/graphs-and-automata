from Graph.graph import Graph

"""
	
"""

class BeamSearch(Graph):
	def search(self, start, end, 
		k=5,
		stochastic=False, 
		full_output=False,
		track_visited=True):

		ans = {
			"strategy" : ("Stochastic " if stochastic else "") +\
				"Beam Search with width " + \
				(str(k) if k > 0 else "unlimited"),
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

			# Now, choose only the k best ones
			# based only on the heuristic cost
			if sons_activated:
				if track_visited:
					sons_activated.sort(key = lambda vertex: 
						self.heuristic_cost[vertex])
				else:
					sons_activated.sort(key = lambda path: 
						self.heuristic_cost[path[-1]])

				if k > 0:
					sons_activated = sons_activated[:k]

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

		return ans["visited_order"]


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
