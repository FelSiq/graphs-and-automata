from collections import OrderedDict
import copy
import re

class Automaton:
	def __init__(self,
		filepath=None,
		alphabet=None, 
		transit_matrix=None,
		initial_state=None, 
		final_states=None,
		regex=None):

		# "transit_matrix" is already a formal representation
		# of both the set of automaton possible states and
		# the transition function.
		self.transit_matrix = copy.deepcopy(transit_matrix) \
			if transit_matrix else OrderedDict()

		self.alphabet = copy.deepcopy(alphabet) if alphabet else []

		self.initial_state = initial_state

		self.final_states = copy.deepcopy(final_states) \
			if final_states else set()

		if filepath is not None:
			if regex is not None:
				print("Warning: ignoring \"regex\" parameter",
					"(\"filepath\" is specified)")
			self.__readautomaton__(filepath)
		else:
			self.load_regex(regex)

	def __readautomaton__(self, filepath):
		# Regex used to get each state set of 
		# the transition matrix in the input file
		re_get_set = re.compile(r"{([^}]*)}")

		# Regex used to get the state identifier of
		# each entry of the transition matrix also
		# from the input file
		re_get_state = re.compile(r"^\s*([^\s,]+)\s*,")

		# This matrix determines if each state is a final
		# state. The identifier adopted in this application
		# for final states is [final_states_name] (between
		# square brackets [..]).
		re_det_final_states = re.compile(r"\[[^\]]+\]")
		re_sbrackets = re.compile(r"\[|\]")

		with open(filepath) as f:
			self.alphabet = f.readline().strip().split(",")
			self.initial_state = f.readline().strip()

			for line in f:
				new_state = re_get_state.search(line).group(1)
				# Check if state is a final state
				# Notation adopted: [final_states_name]
				# (in input file)
				if re_det_final_states.match(new_state):
					new_state = re_sbrackets.sub("", new_state)
					self.final_states.update({new_state})

				entries = {}
				for symbol, set_str in zip(self.alphabet, re_get_set.findall(line)):
					entries[symbol] = set(set_str.split(","))
					if "" in entries[symbol]:
						entries[symbol].remove("")

				self.transit_matrix[new_state] = entries

	def __setequal__(self, a, b):
		# Verify if both sets are equal
		return len(a - b)==0 and len(b - a)==0

	def __searchset__(self, mapping, aux):
		for state in mapping:
			if self.__setequal__(mapping[state], aux):
				return state
		return None

	def __insertsinkstate__(self, state_id="SINK", dfa=True):
		keep_sink_state = False

		sink_transit = state_id if dfa else {state_id}

		# Sink nodes must keep all possible transitions 
		# to itself
		self.transit_matrix[state_id] = {symbol : sink_transit \
			for symbol in self.alphabet}

		for state in self.transit_matrix:
			for symbol in self.alphabet:
				# Every undefined transition must now point
				# to the sink state
				if not self.transit_matrix[state][symbol]:
					keep_sink_state = True
					self.transit_matrix[state][symbol] = sink_transit

		# If no need for sink state
		if not keep_sink_state:
			self.transit_matrix.pop(state_id)

	def __getnulltransitions__(self, null_symbol="e"):
		null_transitions = {}

		for state in self.transit_matrix:
			# Promote a blind search starting in every possible
			# state of the transition matrix. DFS was choosen 
			# because it uses less memory than the BFS.

			null_transitions[state] = {state}
			active_vertexes = [state]
			predecessor_track = {state : None}

			while active_vertexes:
				cur_vertex = active_vertexes.pop()

				if null_symbol not in self.transit_matrix[cur_vertex]:
					# By definition, a undefined null transition is
					# the current vertex itself
					self.transit_matrix[cur_vertex][null_symbol] = {cur_vertex}

				for null_t_vertex in self.transit_matrix[cur_vertex][null_symbol]:
					if null_t_vertex not in predecessor_track:
						predecessor_track[null_t_vertex] = cur_vertex
						active_vertexes.append(null_t_vertex)

						# Each reached state is a null_transition for
						# the current state.
						null_transitions[state].update({null_t_vertex})

		return null_transitions

	def __blindsearch__(self, start_state):
		stack = [start_state]
		visited_states = {start_state}

		while stack:
			cur_state = stack.pop()

			for symbol in self.transit_matrix[cur_state]:
				adj_vertex = self.transit_matrix[cur_state][symbol]

				if adj_vertex and adj_vertex not in visited_states:
					visited_states.update({adj_vertex})
					stack.append(adj_vertex)

		return visited_states

	def __testequivalence__(self, vertex_a, vertex_b):
		return (vertex_a in self.final_states and
			vertex_b in self.final_states) or \
			(vertex_a not in self.final_states and
			vertex_b not in self.final_states)

	def print(self):
		print("Automaton transition matrix:")
		for state in sorted(self.transit_matrix.keys()):
			
			state_label = state
	
			if state in self.final_states:
				state_label = "[" + state_label + "]"
			else:
				state_label = " " + state_label + " "

			if state == self.initial_state:
				state_label = "*" + state_label + "*"
			else:
				state_label = " " + state_label + " "

			print(state_label, end=" : |")
			
			entries = self.transit_matrix[state]

			for c in self.alphabet:
				print(entries[c], end="|")

			print()

		print("\nAutomaton properties:",
			"\n\talphabet:", self.alphabet,
			"\n\tstart state:", self.initial_state,
			"\n\tfinal states:", self.final_states)

	def gen_input_file(self):
		print(",".join(self.alphabet))
		print(self.initial_state)
		for state in sorted(self.transit_matrix.keys()):

			aux_label = state
			if state in self.final_states:
				aux_label = "["  + aux_label + "]"
			print(aux_label, end=",")

			for symbol in self.alphabet:
				aux_states = self.transit_matrix[state][symbol]
				if type(aux_states) != type(""):
					aux_states = ",".join(aux_states)
				print("{", aux_states, "}", sep="", 
					end="," if symbol != self.alphabet[-1] else "")
			print()

	def nfa_to_dfa(self, state_prefix="DFA"):
		# Init DFA ("Deterministic Finite Automaton")
		dfa_var = Automaton(
			alphabet=self.alphabet,
			transit_matrix={},
			initial_state=None, 
			final_states=set())

		# Initial configuration of the resultant automaton
		initial_state_name = state_prefix + "0"
		dfa_var.initial_state = initial_state_name
		list_to_proc = [initial_state_name]
		mapping = {initial_state_name : {self.initial_state}}

		while len(list_to_proc):
			cur_state = list_to_proc.pop(0)
			dfa_var.transit_matrix[cur_state] = {}

			for c in dfa_var.alphabet:
				aux = set()

				for nfa_state in mapping[cur_state]:
					aux.update(self.transit_matrix[nfa_state][c])

				if aux:
					if self.__searchset__(mapping, aux) is None:
						new_state_name = state_prefix + str(len(mapping))
						mapping[new_state_name] = aux
						list_to_proc.append(new_state_name)
						transit_name = new_state_name
						if self.final_states.intersection(aux):
							dfa_var.final_states.update({transit_name})
					else:
						transit_name = self.__searchset__(mapping, aux)
				else:
					transit_name = set()

				dfa_var.transit_matrix[cur_state][c] = transit_name

		return dfa_var	

	def nfae_to_nfa(self, null_symbol="e"):
		nfa = Automaton(
			alphabet=self.alphabet,
			initial_state=self.initial_state)

		if null_symbol in nfa.alphabet:
			nfa.alphabet.remove(null_symbol)

		# First, calculate T_e(p) for all states p from NFAe
		null_transitions = self.__getnulltransitions__(null_symbol)

		# Each entry of the NFA transit matrix is in the form
		# T_NFA(p, c) = T_NFAe_e(T_NFAe(T_NFAe_e(p), c))
		for state in self.transit_matrix:
			nfa.transit_matrix[state] = {}

			# Check if current state is a NFA final state
			# (by definition if, in the null transitions
			# function, p has at least one final state (i.e.
			# has a non null intersection) of NFAe, then
			# p is a final state of NFA.
			if self.final_states.intersection(null_transitions[state]):
				nfa.final_states.update({state})

			for symbol in nfa.alphabet:
				if symbol != null_symbol:
					nfa_state_transit = set()

					# Calculating T_NFAe(<for states>, c)
					for nfae_null_t_state in null_transitions[state]:
						transit_aux = self.transit_matrix[nfae_null_t_state][symbol]

						if type(transit_aux) != type(set()):
							transit_aux = {transit_aux}

						nfa_state_transit.update(transit_aux)

					# Calculating T_NFAe_e(<for states of prev result)
					aux = set()
					for aux_state in nfa_state_transit:
						aux.update(null_transitions[aux_state])
					nfa_state_transit.update(aux)

					nfa.transit_matrix[state][symbol] = nfa_state_transit

		return nfa

	def copy(self):
		return Automaton(
			alphabet=self.alphabet,
			transit_matrix=self.transit_matrix,
			initial_state=self.initial_state,
			final_states=self.final_states)

	def complement(self, dfa=False, sink_id="SINK"):
		"""
			A complementary Automaton has all
			non-final states transformed into
			finals and final states transformed
			into non-finals. Also, it's transi-
			tion matrix has to be complete, so
			a additional sink state need to be
			added to fulfil that requeriment if
			the current automaton has at least
			one undefined transition.
		"""

		# First, the automaton must be an DFA
		if not dfa:
			dfa_automaton = self.nfae_to_nfa()
			dfa_automaton = dfa_automaton.nfa_to_dfa()
		else:
			dfa_automaton = self.copy()

		# Try to insert a sink state in order to keep
		# the complementary automaton transition matrix
		# full
		dfa_automaton.__insertsinkstate__(sink_id)

		# Get the complementary set of states
		compl_final_states = set(dfa_automaton.transit_matrix.keys()) \
			- dfa_automaton.final_states

		complementary = Automaton(
			alphabet=dfa_automaton.alphabet, 
			transit_matrix=dfa_automaton.transit_matrix,
			initial_state=dfa_automaton.initial_state, 
			final_states=compl_final_states)

		return complementary

	def concatenate(self, automaton):
		pass

	def union(self, automaton):
		pass

	def load_regex(self, regex):
		pass

	def intersection(self, automaton):
		pass

	def minimize(self, dfa=False, sink_id="SINK"):
		# Step 0: in order to minimize a automaton,
		# we need to verify three characteristics:
		# 0.1: Automaton must be a DFA
		if not dfa:
			minimal = self.nfae_to_nfa()
			minimal = minimal.nfa_to_dfa()
		else:
			minimal = self.copy()
		
		# 0.2: Transition matrix must be full. So, try
		# to generate a sink state to keep the transi-
		# tion matrix full. This state, if created, will 
		# be removed in the last minimization step.
		minimal.__insertsinkstate__(sink_id)

		# 0.3: Last subitem is to perform a blind search
		# and remove all unreachable (for all symbols) sta-
		# tes starting from the initial state
		visited_nodes = minimal.__blindsearch__(minimal.initial_state)
		nodes_to_remove = set(minimal.transit_matrix.keys()) - \
			visited_nodes

		for node in nodes_to_remove:
			minimal.pop(node)

		# Step 1: Fill the equivalence matrix
		key_order = list(minimal.transit_matrix.keys())
		transit_mat_len = len(key_order)
		equivalence_mat = []

		# 1.1: First, fill all trivially equivalent states
		# A trivially equivalent states is such as both
		# states are final or not final simultaneously.
		equivalence_mat = [[[None] \
			for _ in range(transit_mat_len)] \
			for __ in range(transit_mat_len)]

		for row in range(transit_mat_len - 1):
			for col in range(row + 1, transit_mat_len):
				equivalence_mat[row][col] = equivalence_mat[row][col]
				if minimal.__testequivalence__(key_order[row], key_order[col]):
					equivalence_mat[row][col] = []

		# 1.2: Then, run a algorithm to find out non-trivial
		# equivalent states
		for row in range(transit_mat_len - 1):
			for col in range(row + 1, transit_mat_len):
				if equivalence_mat[row][col] is not None:
					for symbol in minimal.alphabet:
						target_row = key_order.index(minimal.transit_matrix[key_order[row]][symbol])
						target_col = key_order.index(minimal.transit_matrix[key_order[col]][symbol])
						if target_row != target_col:
							if equivalence_mat[target_row][target_col] is None:
								for row_k, row_l in equivalence_mat[row][col]:
									equivalence_mat[row_k][row_l] = None
								equivalence_mat[row][col] = None
							else:
								equivalence_mat[target_row][target_col].append({row, col})

		# Step 2: Unify equivalent states. States may be 
		# renamed freely if desired.

		# FIX HERE!!!!!!!!!!!!!!!!!1
		for row in range(transit_mat_len - 1):
			for col in range(row + 1, transit_mat_len):
				if equivalence_mat[row][col] is not None:
					new_state_label = key_order[row] + key_order[col]

					minimal.transit_matrix[new_state_label] = {}
					for symbol in minimal.alphabet:
						minimal.transit_matrix[new_state_label][symbol] = \
							minimal.transit_matrix[key_order[row]][symbol] + \
							minimal.transit_matrix[key_order[col]][symbol]
				else:
					key_order.pop(row)
					key_order.pop(col)

		for key in key_order:
			minimal.transit_matrix.pop(key)

		# Step 3: Delete states that can't lead to a final
		# state. In this case, more blind search is needed.
		# If no final state is reached, delete state and its
		# transitions.
		for state in minimal.transit_matrix:
			visited_nodes = minimal.__blindsearch__(state)
			
			if not visited_nodes.intersection(minimal.final_states):
				minimal.transit_matrix.pop(state)

	def glud(self, dfa=False, initial_symbol="S", null_symbol="e"):
		# First, the automaton must be an DFA
		if not dfa:
			dfa_automaton = self.nfae_to_nfa()
			dfa_automaton = dfa_automaton.nfa_to_dfa()
		else:
			dfa_automaton = self.copy()

		glud_list = OrderedDict()
		glud_list[initial_symbol] = ["(" + self.initial_state + ")"]

		for state in self.transit_matrix:
			glud_list[state] = []

			for symbol in self.alphabet:
				if self.transit_matrix[state][symbol]:
					glud_list[state].append(symbol + \
						"(" + self.transit_matrix[state][symbol] + ")")

			if not glud_list[state]:
				glud_list.pop(state)

		for final_state in self.final_states:
			glud_list[final_state].append(null_symbol)

		return glud_list

	def load_glud(self, filepath):
		pass
		
if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], "<filepath>")
		exit(1)

	print("-- Original automaton --")
	g = Automaton(sys.argv[1])
	g.print()

	print("\n-- NFA automaton --")
	ne = g.nfae_to_nfa()
	ne.print()

	print("\n-- DFA automaton --")
	d = ne.nfa_to_dfa()
	d.print()

	print("\n-- Minimal DFA automaton --")
	d_min = d.minimize()
	d_min.print()

	print("\n-- Complementary automaton --")
	c = d.complement()
	c.print()

	print("\n-- Minimal Complementary automaton --")
	c_min = c.minimize()
	c_min.print()

	print("\n-- GLUD --")
	glud = d.glud()
	for variable in glud:
		for rules in glud[variable]:
			print(variable, "->", rules)
	
