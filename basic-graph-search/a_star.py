from Graph.graph import Graph
import copy

"""
	This code implements the algorithm A*.

	A* is a informed-type graph search algorithm,
	whose solution is garanteed to be optimal if
	the search heuristic used is both consistent
	and admissible.

	A admissible heuristic is always equal or less
	the real cost. It is always "optimistic" about
	the effort necessary to get from A to B. For
	example, in a geographic context, the distance
	between vertex of city A and the vertex of city
	B is for sure equal or bigger the euclidean dis-
	tance (straight line) between these two, as a 
	stright line is the shortest distance between
	two points (in a geographic context). So, the
	euclidean distance is a admissible heuristic
	for the effort necessary to get from city A to
	city B.
"""

class Astar(Graph):
	def search(self, start, end, full_output=False):
		"""
		Runs A* algorithm in the given graph, from
		vertex "start" to vertex "end". 
		
		If "full_output" is false, this function only 
		returns a list with the shortest path between 
		the two given vertexes.
		
		Otherwise, the return value will be a dictionary
		with the following properties:

		"shortest_path": 	(List) shortest path between "start" and
					"end" vertexes, assuming the heuristic
					costs are admissible and consistent.

		"visit_order":		(List) Identifier of vertexes in
					the same order they were visited during
					algorithm execution.
		"""
		ans = {
			"shortest_path" : [],
			"visit_order": []
		}

		activated = [{
			"travel_path": [start], 
			"travel_total_cost": 0
		}]

		while activated:
			cur_state = activated.pop(0)

			# Just some auxiliary variables to keep
			# code clean and more readable
			cur_path = cur_state["travel_path"]
			cur_vertex = cur_path[-1]
			cur_total_cost = cur_state["travel_total_cost"]

			ans["visit_order"].append(cur_vertex)

			if cur_vertex == end:
				activated = []
				ans["shortest_path"] = cur_path
			else:
				for adj_vertex in self.transit_mat[cur_vertex]:
					activated.append({
						"travel_path": copy.copy(cur_path) + [adj_vertex],
						"travel_total_cost": cur_total_cost + 
							self.transit_mat[cur_vertex][adj_vertex]
					})

				activated.sort(key = lambda state: 
					state["travel_total_cost"] + 
					self.heuristic_cost[state["travel_path"][-1]])

		if full_output:
			return ans

		return ans["shortest_path"]

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 4:
		print("usage:", sys.argv[0], "<filepath> <start vertex> <end vertex>")
		exit(1)

	g = Astar(sys.argv[1])

	g.print_graph(fill_factor=5)

	ans = g.search(
		start=sys.argv[2], 
		end=sys.argv[3], 
		full_output=True)

	print("Visit order:", ans["visit_order"],
		"Shortest path:", ans["shortest_path"])

