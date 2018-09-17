import sys
sys.path.insert(0, "../../basic-graph-search/")

from Graph.graph import Graph

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

class Map(Graph):
	def color()

if __name__ == "__main__":
