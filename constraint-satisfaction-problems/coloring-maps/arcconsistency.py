import sys
sys.path.insert(0, "../../basic-graph-search/Graph")

from domgraph import DomainGraph
import copy

"""
	This class runs the Arc Consistency algoithm
	(Constraint Propagation), which detects bad
	choices very fast while solving a CSP, increa-
	sing the solution speed.
"""

class ArcConsistency(DomainGraph):
	def refreshDomain(self):
		for vertex in self.transit_mat:
			if self.value[vertex] is not None:
				for neighbor in self.transit_mat[vertex]:
					if self.value[vertex] in self.domain[neighbor]:
						self.domain[neighbor].remove(self.value[vertex])

	def __backtracking__(self, changes):
		for change in changes:
			vertex, val = change
			self.domain[vertex].update({val})

	def consistentAttrib(self, start_vertex, value, ret_changes=True):
		"""
			Run Arc Consistency algorithm.
		"""

		changes = []
		queue = []

		# The first step is the Forward checking: if the current
		# attribution empty a neighbor domain, then that attribution
		# will not lead to a solution and, therefore, must be cancelled.
		for neighbor in self.transit_mat[start_vertex]:
			if self.value[neighbor] is None:
				if self.domain[neighbor] == {value}:
					self.__backtracking__(changes)
					return None

				queue.append((start_vertex, neighbor))

		# Repeat for
		#	- All adjacent vertexes of current vertex, which must be
		#		the vertex of the last CSP iteration assigment
		#	- All vertex whose domain changed during the constraint
		#		propagation process 
		while queue:
			cur_edge = queue.pop(0)

			ascendant, incident = cur_edge

			# A consistent domain is a domain whose
			# for ALL values in it, there is AT LEAST ONE another consistent
			# value for all non-assigned neighbors.
			for val in copy.copy(self.domain[incident]):
				# If domain of ascendant (neighbor) vertex is just the current
				# value, then that value is inconsistent
				if self.domain[ascendant] == {val}:
					if self.domain[incident] == {val}:
						# If incident domain is just the current "val",
						# then the last assignment is inconsistent.
						# Undo changes and return False
						self.__backtracking__(changes)
						return None

					# Else, remove that value from the incident vertex domain,
					# and add all its neighbors to the queue to verify if it
					# created some inconsistency due to domain change
					self.domain[incident].remove(val)

					changes.append((incident, val))

					for incident_neighbor in self.transit_mat[incident]:
						# Just verify unassigned variables (neighbors)
						if self.value[incident_neighbor] is None:
							queue.append((incident, incident_neighbor))

		# Process of propagating constraints ended successfully
		self.value[start_vertex] = value

		# Remove given value just in case, due to backtracking possibilities
		self.domain[start_vertex].remove(value)
		changes.append((start_vertex, value))

		# The reason for returning the changes are to enable future
		# backtrackings, if necessary, in the next CSP iterations/states
		if ret_changes:
			return changes

		return None

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("usage:", sys.argv[0], 
			"<filepath> <start-vertex>",
			"<value-to-assign> [separator - default is \",\"]")
		exit(1)

	try:
		sep = sys.argv[4]
		if not sep:
			raise Exception
	except:
		sep = ","

	ac = ArcConsistency(filepath=sys.argv[1], sep=sep)

	ac.print_graph()

	ac.refreshDomain()

	changes = ac.consistentAttrib(sys.argv[2], sys.argv[3])

	print("\nValues:")
	for vertex in ac.value:
		print(vertex, "\t:", ac.value[vertex])

	print("\nDomains:")
	for vertex in ac.domain:
		print(vertex, "\t:", ac.domain[vertex])

	print("\nChanges made:", changes)
