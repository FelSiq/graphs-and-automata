from Graph.graph import Graph

"""
	Greedy Best-First Search is pretty much Hill Climbing
	with backtracking, which means that all opened
	vertexes are kept until a solution is found.

	Just like Hill-Climbing (HC) it only considers
	the heuristic cost to choose between the adjacent
	nodes. Real cost between nodes are never taken
	into acount.

	This is not a complete-type search, as it may get
	stuck on loops.

	This search is not optimal.
"""

class BestFirst(Graph):
	def search(self, start, end, 
		track_visited=True, 
		full_output=False, 
		max_it=1e+5):
		
		ans = {
			"strategy": "Greedy Best-First Search" + 
				(" (tracking visits)" if track_visited else ""),
			"visit_order": [],
			"found_path": [],
			"total_cost": -1.0
		}

		activated = [start if track_visited else [start]]
		predecessor_track = {start : None}

		found_answer = False

		it = 0
		while activated and it < max_it:
			it += 1
			# If track_visited is False the activated list
			# must hold the entire path of each iteration in
			# order to return the found path.
			aux = activated.pop(0)

			if track_visited:
				# If tracking visited nodes, only the current
				# node must be kept on the activate list
				cur_vertex = aux
			else:
				# Otherwise, the full path must be kept, because
				# the predecessor_track structure will not work
				# anymore
				cur_path = aux
				cur_vertex = aux[-1]

			ans["visit_order"].append(cur_vertex)

			if cur_vertex == end:
				activated = []
				found_answer = True

			else:
				for adj_vertex in self.transit_mat[cur_vertex]:
					if not track_visited or adj_vertex not in predecessor_track:
						predecessor_track[adj_vertex] = cur_vertex
						if track_visited:
							activated.append(adj_vertex)
						else:
							activated.append(cur_path + [adj_vertex])
					
					if track_visited:
						activated.sort(key = lambda k: self.heuristic_cost[k])
					else:
						activated.sort(key = lambda k: self.heuristic_cost[k[-1]])

		if found_answer:
			if not track_visited:
				ans["found_path"] = cur_path
				ans["total_cost"] = 0.0

				next_vertex = cur_path[0]
				for i in range(1, len(cur_path)):
					cur_vertex = next_vertex
					next_vertex = cur_path[i]
					ans["total_cost"] += self.transit_mat[cur_vertex][next_vertex]
			else:
				"""
				If found a path from "start" to "end", follow backwards the
				predecessor_track from "end" to "start", recovering the
				transition costs and the found path.
				"""
				if end in predecessor_track:
					ans["total_cost"] = 0.0
					cur_vertex = end
					ans["found_path"].append(end)

					while cur_vertex != start:
						prev_vertex = cur_vertex
						cur_vertex = predecessor_track[cur_vertex]

						ans["total_cost"] += self.transit_mat[cur_vertex][prev_vertex]
						ans["found_path"].insert(0, cur_vertex)

		if it == max_it:
			print("Warning: max_iteration (" + str(max_it) + ") reached.")

		if full_output:
			return ans
		
		return ans["found_path"]

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 4:
		print("usage:", sys.argv[0], "<filepath>" \
			" <start> <end> [track visited (0/1) - default to 1]")
		exit(1)

	g = BestFirst(sys.argv[1])

	g.print_graph(fill_factor=5)

	try:
		track_visited = bool(int(sys.argv[4]))
	except:
		track_visited = True

	ans = g.search(
		start=sys.argv[2], 
		end=sys.argv[3], 
		track_visited=track_visited,
		full_output=True)

	print("Result:")
	for attr in ans:
		print(attr, ":", ans[attr])
	
