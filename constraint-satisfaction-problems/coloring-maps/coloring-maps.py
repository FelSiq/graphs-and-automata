import sys
sys.path.insert(0, "../../basic-graph-search/")

from Graph.graph import Graph
from arcconsistency import ArcConsistency
import heapq

"""
	Heuristics for CSP (Constraint Satisfaction Problems):

	Choosing the next variable to be assigned:
		1. MRV ("Minimum Remaining Values" or 
			"Most Constrained Variable"):
			Choose the variable with smallest Domain.

		2. DH ("Degree Heuristic" or "Most Constraining Variable"):
			Used as tie-breaker for MRV. Between the
			variables with the smallest Domain subset,
			choose the one with the highest degree of
			Constraints between REMAINING variables.

		The combination of both heuristics prioritize the
		variables that are more likely to fail. The rea-
		soning behind this is if a given state is doomed
		to fail, then we better find it fast. Remembering
		that all variables must be assigned in a consistent
		way (respecting all constraints) in order to
		produce a Solution.

	Choosing the next value to be assigned:
		3. LCV ("Least Constraining Value"):
			Given a variable, attribute the value that
			less remove values from other variable's 
			domains.

		This heuristic tries to avoid failure, keeping up
		the maximum flexibility for the remaining variables,
		to find out a solution. Remembering that a problem
		may have multiple solutions, so we want to find one
		as fast as possible, too.

	Detecting failure earlier:
		4. FC ("Forward Checking"):
			Keep track of current Legal Domain (values
			that a variable may assume mantaining the
			state consistency) of each variable, and
			backtrack if any legal domain becomes empty.

		5. CP ("Constraint Propagation"):
			Forward Checking just verify consistency
			between assigned and non-assigned states. The
			CP heurist verify constraints between two
			unassigned variables.

			Example of CP (here implemented): "Arc 
			Consistency"
"""

class Map(ArcConsistency):
	def __curstateissolution__(self):
		# Check if all variables has a value AND if
		# all values are consistent (in this case, no
		# vertex can have the same color of other adjacent
		# vertex).
		for vertex in self.value:
			if self.value[vertex] is None:
				return False

			for adj_vertex in self.transit_mat[vertex]:
				if self.value[adj_vertex] is None or \
					self.value[adj_vertex] == self.value[vertex]:
					return False
		return True

	def __nextvariable__(self):
		# Apply MVR (choose the variable with the smallest
		# current domain), and use DH (variable with highest
		# number of constraints) to tie-breaker for MRV.

		# Construct a MIN-HEAP which uses the domain size (MRV) as main key
		# and the NEGATIVE count of adjacent vertexes of a given vertex
		# as a tie-breaker (DH). In the worst-case scenario, the vertex will 
		# be chosen alphabetically.
		domain_sizes = [(
			len(self.domain[v]), -len(self.transit_mat[v]), v) 
			for v in self.value]

		heapq.heapify(domain_sizes)

		for domain_size, neg_const_count, var in domain_sizes:
			# The "domain_size == 0" thing isn't this function business.

			if self.value[var] is None and domain_size > 0:
				return var
		return None

	def __listvalsbylcv__(self, variable):
		# Apply LCV to find the best value of "variable's"
		# Domain to apply. As mentioned above, the LCV heurist
		# choose the value which less affect adjacent vertex
		# domains (under the constraint graph perspective).
		# Therefore, the choosen value mantains the highest
		# flexibility over the CSP path to solution, speeding
		# up the solution search. Also, it is a good idead to
		# apply FC heuristic here too, which verificates when
		# the selected value is the single possible value to
		# some adjacent vertex and, therefore, can not be attri-
		# buted consistently to the current variable.

		sorted_vals = []
		for val in self.domain[variable]:
			forward_checking = True
			count_val_neighbor = 0

			for neighbor in self.transit_mat[variable]:
				if val in self.domain[neighbor]:
					count_val_neighbor += 1

					# Apply FC
					if self.domain[neighbor] == {val}:
						forward_checking = False
						break

			# If is safe the attribution of current value...
			if forward_checking:
				sorted_vals.append((count_val_neighbor, val))

		if sorted_vals:
			# Sort values to pick based on LCV (+ FC) Heuristic(s)
			sorted_vals.sort(key = lambda k : k[0])
			return [val[1] for val in sorted_vals]

		return None

	def __undochanges__(self, changes_list):
		# Backtracking: undo all changes if change list
		# Changes are in format (vertex, value removed)
		for vertex, rem_value in changes_list:
			self.domain[vertex].update({rem_value})

	def paint(self):
		changes = []
		activated_vertexes = []

		while not self.__curstateissolution__():
			if not activated_vertexes:
				var = self.__nextvariable__() # Apply MRV + DH
				values = self.__listvalsbylcv__(var) # Apply LCV + FC
			else:
				# Recovery from a backtracking
				var, values = activated_vertexes.pop()

			attribution = False
			while values:
				val = values.pop()
				# Guaranteed consistent attribution +
				# Arc Consistency (Constraint propagation 
				# algorithm) execution
				new_changes = self.consistentAttrib(var, val)

				# If attribution was successfully...
				if new_changes is not None:
					# Store the changes made, break "while" loop
					# and signal out that a attribution was made.
					# Also, store current state (variable, cur_domain)
					# in case of backtracking.
					changes.append(new_changes)
					attribution = True
					activated_vertexes.append((var, values))
					values = []

			# If no attribution was successful 
			# with current variable, bracktrack.
			if not attribution:
				self.__undochanges__(changes.pop())

		# End of coloring maps CSP
		return self.value
			

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], 
			"<filepath> [separator - default is \",\"]")
		exit(1)

	try:
		sep = sys.argv[2]
	except:
		sep = ","

	m = Map(filepath=sys.argv[1], sep=sep)

	m.print_graph()

	ans = m.paint()

	print("\nSolution:")
	for vertex in ans:
		print(vertex, "\t:", ans[vertex])
