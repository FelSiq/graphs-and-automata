from Graph.graph import Graph
import copy

"""
	Implementation of both Depth-First Search (DFS) and Bread-
	th-First Search (BFS) Algorithms. The only difference bet-
	ween these two are a single code line (the activated vertexes
	are put in a stack (LIFO data scruture) in DFS algorithm, while 
	BFS uses a queue (FIFO data structure).

	Also, this code includes the Iterative deepening strategy for
	DFS algorithm, where, at each interation, the maximum deepness
	of the search is a fixed integer number. This number is incremented
	each iteration. This strategy turns the DFS algorithm a complete-
	type search (it will find a solution, if any exists) and, if the
	weights of all edges are the same constant value, optimal.

	However, this single difference is not negligible, as it does
	change every property of the search strategy.

	BFS characteristics:
		It's a blind-type search, meaning that any given heuris-
		tic costs will be useless.

		When all edge weights are the same constant value, the
		result of this algorithm is optimal (iff).

		It is a complete-type search, which means that if exists
		at least one path from A to B, this algorithm will find
		one of then.

	DFS characteristics:
		Just like BFS, the DFS algorithm is a blind-type search.

		DFS is not optimal.

		DFS is complete if and only if the search domain is finite.

	DFS w/ Iterative Deepning:
		At each iteration, the maximum deepness of the search is
		fixed at a constant value l = 0, 1, 2, (...), until a
		solution is found. The DFS alogrithm is runned for every 
		l, respecting the imposed max deepness constraint.

		IDDFS is complete and uses much less memory than the BFS
		strategy, therefore is a good strategy if one whants a 
		complete blind search strategy but has limited memory.
"""

class BlindSearch(Graph):
	def search(self, start, end, 
		depth_first=False, 
		full_output=False, 
		sort_states=False):

		ans = {
			"strategy": "DFS" if depth_first else "BFS",
			"found_path": [],
			"visit_order": [],
			"total_cost": -1.0
		}

		# List of activated vertexes
		activated = [start]

		# Structure needed to reconstruct the found path, if
		# it exists, at the end of the algorithm
		predecessor_track = {start : None}

		while activated:
			if depth_first:
				# Depth-first Search (DFS) uses a stack
				# to keep track of activated vertexes
				# (LIFO - Last In First Out pattern)
				cur_vertex = activated.pop()
			else:
				# Meanwhile, Breadth-First Search (BFS)
				# uses a queue (FIFO - First In First Out).
				cur_vertex = activated.pop(0)
		
			ans["visit_order"].append(cur_vertex)	

			if cur_vertex == end:
				activated = []

			else:
				edges_list = self.transit_mat[cur_vertex].keys()
				if sort_states:
					# The sorting must be reserve for DFS
					# because the structure used is (FIFO),
					# which means that the latter states
					# would be the first ones to be visited
					edges_list = sorted(edges_list, reverse=depth_first)

				for adj_vertex in edges_list:
					if adj_vertex not in predecessor_track:
						predecessor_track[adj_vertex] = cur_vertex
						activated.append(adj_vertex)

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

		if full_output:
			return ans

		return ans["found_path"]

	def iterative_deepening(
		self, start, end, 
		full_output=False, 
		sort_states=False,
		max_deepness=-1):

		visit_order_bookkeeping = {}

		cur_max_deepness = 0

		has_next_iteration = True
		while has_next_iteration:
			has_next_iteration = False

			ans = {
				"found_path" : [],
				"visit_order": [],
				"total_cost": -1.0,
				"total_deepness": 0
			}

			# List of activated vertexes
			activated = [{
				"vertex": start, 
				"deepness": 0
			}]

			# Structure needed to reconstruct the found path, if
			# it exists, at the end of the algorithm
			predecessor_track = {start : None}

			while activated:
				cur_state = activated.pop()

				cur_vertex = cur_state["vertex"]
				cur_deepness = cur_state["deepness"]
			
				ans["visit_order"].append(cur_vertex)
				ans["total_deepness"] = max(ans["total_deepness"], cur_deepness)

				if cur_vertex == end:
					activated = []

				else:
					edges_list = self.transit_mat[cur_vertex].keys()

					if cur_deepness >= cur_max_deepness:
						# Max Current Deepness reached, just check
						# if there is more levels to be visited in
						# the next iteration. Otherwise, the algorithm
						# did not found any solution.
						for vertex in edges_list:
							has_next_iteration |= vertex not in predecessor_track

					else:
						if sort_states:
							# The sorting must be reserve for DFS
							# because the structure used is (FIFO),
							# which means that the latter states
							# would be the first ones to be visited
							edges_list = sorted(edges_list, reverse=True)

						for adj_vertex in edges_list:
							if adj_vertex not in predecessor_track:
								predecessor_track[adj_vertex] = cur_vertex
								activated.append({
									"vertex": adj_vertex,
									"deepness": cur_deepness + 1
								})
			cur_max_deepness += 1
			if max_deepness >= 0:
				has_next_iteration &= cur_max_deepness <= max_deepness

			visit_order_bookkeeping[cur_max_deepness] = copy.copy(ans["visit_order"])

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

		ans["all_visit_orders"] = visit_order_bookkeeping
		ans["strategy"] = "IDDFS"

		if full_output:
			return ans

		return ans["found_path"]


if __name__ == "__main__":
	import sys

	if len(sys.argv) < 4:
		print("usage:", sys.argv[0], 
			"<filepath> <start vertex>" \
			"<end vertex> [search type (BFS/DFS) - "\
			"default to BFS] [Iterative deepening "\
			"(0/1) - Only for DFS]")
		exit(1)

	g = BlindSearch(sys.argv[1])

	g.print_graph(fill_factor=5)

	try:
		search_type = sys.argv[4]
	except:
		search_type = "bfs"

	try:
		it_dp = int(sys.argv[5]) and search_type.lower() == "dfs"
	except:
		it_dp = False

	if it_dp:
		# Iterative deepening DFS strategy
		ans = g.iterative_deepening(
			start=sys.argv[2], 
			end=sys.argv[3], 
			full_output=True,
			sort_states=True)

	else:
		ans = g.search(
			start=sys.argv[2], 
			end=sys.argv[3], 
			depth_first=search_type.lower()=="dfs",
			full_output=True,
			sort_states=True)

	print("Result:")
	for attr in ans:
		print(attr, ":", ans[attr])
