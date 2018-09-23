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

			for adj_vertex in self.transit_matrix[vertex]:
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
		domain_sizes = heapq.heapify([(
			len(self.domain[v]), -len(self.transit_matrix[v]), v) 
			for v in self.value])

		for domain_size, neg_const_count, var in domain_sizes:
			# The "domain_size == 0" thing isn't this function business.

			if self.value[var] is None and domain_size > 0:
				return ret_var
		return None

	def __nextvalue__(self, variable):
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
				sorted_vals.append((count_val_neighbors, val))

		if sorted_vals:
			# Sort values and pick based on LCV Heuristic
			sorted_vals.sort(lambda k : k[0])
			return sorted_vals.pop()[1]

		return None

	def __undochanges__(self, changes_list):
		# Backtracking: undo all changes if change list
		# Changes are in format (vertex, value removed)
		for vertex, rem_value in changes_list:
			self.domain[vertex].update({rem_value})

		# The last value is a bit problematic, as it is
		# the bad attribution that caused all of this
		# backtracking thing, therefore is a bad idea
		# undo it. However, on the future backtracks,
		# this attribution may not be that bad and can
		# even be part of the answer, so it is not safe
		# to just remove that value from the correspondent
		# vertex, too.

		...

	def paint(self):
		changes = []
		no_solution = False

		while not self.__curstateissolution__() and not no_solution:
			var = self.__nextvariable__() # Apply MRV + DH
			value = self.__nextvalue__(var) # Apply LCV + FC

			if not value:
				# Domain's empty or no possible values
				# to apply to current var w/o getting
				# into a inconsistent state. Then, back-
				# track the last consistent change made
				if changes:
					self.__undochanges__(changes.pop())
				else:
					no_solution = True
			else:
				# Run Arc Consistency algorithm + attribution
				# if everything went just right
				new_changes = self.checkConsistency(var, value)

				# Check if Arc Consistency FAILED
				if new_changes is None:
					# ArcConsistency failed, therefore backtrack
					if changes:
						self.__undochanges__(changes.pop())
					else:
						no_solution = True
				else:
					# Arc consistency succeed. Add change list
					# into changes list due to a possible future
					# backtracking
					changes.append((new_changes,))

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

	print("Solution:", m.paint())
