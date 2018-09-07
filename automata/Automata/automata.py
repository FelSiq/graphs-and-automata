import re

class Automaton:
	def __init__(self,
		filepath=None,
		alphabet=None, 
		transit_matrix=None,
		initial_state=None, 
		final_state=None):

		# "transit_matrix" is already a formal representation
		# of both the set of automaton possible states and
		# the transition function.
		self.transit_matrix = transit_matrix if transit_matrix else {}
		self.alphabet = alphabet if alphabet else []
		self.initial_state = initial_state
		self.final_state = final_state if final_state else set()

		if filepath is not None:
			self.__read_automaton__(filepath)

	def __read_automaton__(self, filepath):
		# Regex used to get each state set of 
		# the transition matrix in the input file
		re_get_set = re.compile(r"{([^}]*)}")

		# Regex used to get the state identifier of
		# each entry of the transition matrix also
		# from the input file
		re_get_state = re.compile(r"^\s*([^\s,]+)\s*,")

		# This matrix determines if each state is a final
		# state. The identifier adopted in this application
		# for final states is [final_state_name] (between
		# square brackets [..]).
		re_det_final_state = re.compile(r"\[[^\]]+\]")
		re_sbrackets = re.compile(r"\[|\]")

		with open(filepath) as f:
			self.alphabet = f.readline().strip().split(",")
			self.initial_state = f.readline().strip()

			for line in f:
				new_state = re_get_state.search(line).group(1)
				# Check if state is a final state
				# Notation adopted: [final_state_name]
				# (in input file)
				if re_det_final_state.match(new_state):
					new_state = re_sbrackets.sub("", new_state)
					self.final_state.update({new_state})

				entries = {}
				for symbol, set_str in zip(self.alphabet, re_get_set.findall(line)):
					entries[symbol] = set(set_str.split(","))
					if "" in entries[symbol]:
						entries[symbol].remove("")

				self.transit_matrix[new_state] = entries
				
	def print(self):
		print("Automaton transition matrix:")
		for state in sorted(self.transit_matrix.keys()):
			print(state, end=":\t|")
			
			entries = self.transit_matrix[state]
			for c in self.alphabet:
				print(entries[c], end="|")
			print()

		print("\nAutomaton properties:",
			"\nalphabet:", self.alphabet,
			"\nstart state:", self.initial_state,
			"\nfinal states:", self.final_state)

	def gen_input_file(self):
		print(",".join(self.alphabet))
		print(self.initial_state)
		for state in sorted(self.transit_matrix.keys()):

			aux_label = state
			if state in self.final_state:
				aux_label = "["  + aux_label + "]"
			print(aux_label, end=",")

			for symbol in self.alphabet:
				aux_states = self.transit_matrix[state][symbol]
				if type(aux_states) != type(""):
					aux_states = ",".join(aux_states)
				print("{", aux_states, "}", sep="", 
					end="," if symbol != self.alphabet[-1] else "")
			print()
		
if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], "<filepath>")
		exit(1)

	g = Automaton(sys.argv[1])

	g.print()
