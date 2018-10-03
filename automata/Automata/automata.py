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
		regex=None,
		grammar=None,
		sep=",",
		null_symbol="e"):

		"""
			Attributes description:

			filepath	: Source file where the automaton properties
					are specified. The input file must follow the
					model right below:
					
					<alphabet with m symbols separated by "sep>
					<initial state>
					<state_0>, {delta(<state_0>, symbol_0)}, ..., {delta(<state_0>, symbol_m)}
					<state_1>, {delta(<state_1>, symbol_0)}, ..., {delta(<state_1>, symbol_m)}
					...
					<state_n>, {delta(<state_n>, symbol_0)}, ..., {delta(<state_n>, symbol_m)}
					
					Final states must be marked with square brackets ("[]") around their
					identifier in the transition matrix identifier declaration.

					Example:
					
					a,b
					q0
					q0,{q1},{q0}
					[q1],{q2,q1,q0},{q1,q2}
					q2,{},{q0}

					In the exemple above, the alphabet is {a,b} and the automaton has
					three states, {q0, q1, q2} and a single final state {q1} (marked with
					square brackets around it's identifier).

			The parameters below only make sense if no filepath is given.
			alphabet	: The alphabet of the new automaton. Must be a <list> type.

			transit_matrix	: The transition matrix of automaton. Must be a <dictionary> type structure,
					with each key being a state and each value is another <dictionary> containing
					all alphabet as keys and it's values must be <set> containing all states rea-
					ched by the current state and the current symbol. The transition matrix
					of the previous example would be:

					transit_matrix = {
						"q0" : {"a" : {q1} ,"b" : {q0}}
						"q1" : {"a" : {q1, q2, q0} ,"b" : {q1, q2}}
						"q2" : {"a" : {} ,"b" : {q0}}
					}

			initial_state	: A <string> containing the identifier of the automaton initial state.

			final_states	: A <set> type structure containing all automaton final state idenfiers.

			regex		: A string containing a basic "regex"-like pattern in order to be converted
					to a automaton. The operations supported are defined below:
					
					Let "a" and "b" be linear expressions (a set of symbols in a given alphabet).

					1. Concatenation: ab
					2. Union: a + b
					3. (Kleene Star) Sucessive concatenation: a*
					4. (Kleene Sum): a+

			grammar		: A filepath containing a set of rules in URLG ("Unitary Right Linear Grammar")
					form. The model of the input file must follow the pattern given below:

					<terminal symbols list separated by "sep">
					<Variable symbols list separated by "sep">
					<initial variable identifier>
					<s_a> -> symbol_x(<s_i>)
					<s_b> -> symbol_y(<s_j>)
					<s_c> -> symbol_z(<s_k>)
					...
					<s_z> -> symbol_w(<s_w>)

					Where all variables to the right must be around parenthesis "()".

					Example:
					a,b,c
					S,A,B
					S
					S -> a(A)
					A -> b(A)
					A -> a(B)
					B -> c
					B -> e

					Where the variables are {S, A, B} and the terminal symbols {a, b, c}.
					"e" is the null transition/empty string symbol.

			null_symbol	: Symbol used as null_transition/empty string. Must be
					given when both loading a regex or a grammar.
		"""

		# "transit_matrix" is already a formal representation
		# of both the set of automaton possible states and
		# the transition function.
		self.transit_matrix = copy.deepcopy(transit_matrix) \
			if transit_matrix is not None and transit_matrix else OrderedDict()

		self.alphabet = copy.deepcopy(alphabet) \
			if alphabet is not None and alphabet else []

		self.initial_state = initial_state

		self.final_states = copy.deepcopy(final_states) \
			if final_states is not None and final_states else set()

		if filepath is not None:
			self.__readautomaton__(filepath=filepath, sep=sep)

		elif regex is not None:
			self.load_regex(regex, null_symbol=null_symbol)

		elif grammar is not None:
			self.load_grammar(grammar, null_symbol=null_symbol)

	def __readautomaton__(self, filepath, sep=","):
		# Regex used to get each state set of 
		# the transition matrix in the input file
		re_get_set = re.compile(r"{([^}]*)}")

		# Regex used to get the state identifier of
		# each entry of the transition matrix also
		# from the input file
		re_get_state = re.compile(r"^\s*([^\s(" + sep + \
			")]+)\s*" + sep)

		# This matrix determines if each state is a final
		# state. The identifier adopted in this application
		# for final states is [final_states_name] (between
		# square brackets [..]).
		re_det_final_states = re.compile(r"\[[^\]]+\]")
		re_sbrackets = re.compile(r"\[|\]")

		with open(filepath) as f:
			self.alphabet = f.readline().strip().split(sep)
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
					entries[symbol] = set(set_str.split(sep))
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

			for symbol in self.alphabet:
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

	def __buildnewautomaton__(self, automaton, null_symbol="e"):
		"""
			This method unify two automatons structure,
			needed for both operations of concatenation and
			union and, by consequence, intersection.

			Basics for all mentioned operation:
			-	Expand the transition matrix, containing
				all states to both alphabets

				(transit_func : (Q1 U Q2) X (A1 U A2) -> (Q1 U Q2),
				where Q1 and Q2 are the states of automaton 1 and 2
				respectivelly and A1 and A2 are the alphabet of
				automatons 1 and 2, respectivelly).

			-	The resultant alphabet has the two alphabets
				plus the null transition symbol

		"""
		unified_transit_mat = copy.deepcopy(self.transit_matrix)

		# Add undefined transitions for all states of the current
		# automaton to the symbols of the second automaton alphabet
		# which are not in the current automaton alphabet
		for vertex in self.transit_matrix:
			for symbol in automaton.alphabet + [null_symbol]:
				if symbol not in unified_transit_mat[vertex]:
					unified_transit_mat[vertex][symbol] = set()
				else:
					if type(unified_transit_mat[vertex][symbol]) != type(set()):
						unified_transit_mat[vertex][symbol] = \
							{unified_transit_mat[vertex][symbol]}

		# Verify if second automaton states has conflicting names/id
		# in relation of the first automaton
		second_transit_mat = copy.deepcopy(automaton.transit_matrix)
		rename_struct = {}
		for vertex in automaton.transit_matrix:
			if vertex in unified_transit_mat:
				new_vertex_label = self.__stateidsintegrity__(\
					unified_transit_mat.keys(), 
					vertex, 
					fill_symbol="B")

				rename_struct[vertex] = new_vertex_label
				second_transit_mat[new_vertex_label] = second_transit_mat.pop(vertex)

		for vertex in second_transit_mat:
			for symbol in automaton.alphabet:
				if type(second_transit_mat[vertex][symbol]) != type(set()):
					second_transit_mat[vertex][symbol] = \
						{second_transit_mat[vertex][symbol]}

				for target_vertex in second_transit_mat[vertex][symbol]:
					if target_vertex and target_vertex in rename_struct:
						second_transit_mat[vertex][symbol] = \
							rename_struct[target_vertex]

		# Don't forget the final state list
		second_final_states = copy.deepcopy(automaton.final_states)
		for state in second_final_states:
			if state in self.transit_matrix:
				second_final_states.remove(state)

				new_vertex_label = self.__stateidsintegrity__(\
					unified_transit_mat.keys(), state, 
					fill_symbol="B")

				second_final_states.update({new_vertex_label})

		# Neither the initial state
		second_initial_state = copy.copy(automaton.initial_state)
		second_initial_state = self.__stateidsintegrity__(\
			self.transit_matrix.keys(), 
			second_initial_state, 
			fill_symbol="B")

		# Unify both transit matrix and add undefined transitions to
		# the second automaton states for symbols in current automaton
		# alphabet which are not present in the second automaton alpha-
		# bet.
		for vertex in second_transit_mat:
			unified_transit_mat[vertex] = second_transit_mat[vertex]

			for symbol in self.alphabet + [null_symbol]:
				if symbol not in unified_transit_mat[vertex]:
					unified_transit_mat[vertex][symbol] = set()
				else:
					if type(unified_transit_mat[vertex][symbol]) != type(set()):
						unified_transit_mat[vertex][symbol] = \
							{unified_transit_mat[vertex][symbol]}

		# Construct new alphabet. New alphabet must not have
		# repeated symbols and must contain null transition symbol
		unified_alphabet = copy.copy(self.alphabet)
		for symbol in automaton.alphabet + [null_symbol]:
			if symbol not in unified_alphabet:
				unified_alphabet += [symbol]

		return unified_transit_mat, unified_alphabet, \
			second_initial_state, second_final_states

	def __stateidsintegrity__(self, state_list, 
		state_id, fill_symbol="@"):
		
		while state_id in state_list:
			state_id += fill_symbol

		return state_id

	def print(self, undefined_symbol="-", sort_state_names=False):
		print("Automaton transition matrix:")

		max_id_len = 4 + max([len(state) \
			for state in self.transit_matrix.keys()])

		for state in sorted(self.transit_matrix.keys()) \
			if sort_state_names else self.transit_matrix.keys():
			
			state_label = state
	
			if state in self.final_states:
				state_label = "[" + state_label + "]"
			else:
				state_label = " " + state_label + " "

			if state == self.initial_state:
				state_label = "*" + state_label + "*"
			else:
				state_label = " " + state_label + " "

			print("{vid:<{fill}}".format(vid=state_label, fill=max_id_len), end=" : |")
			
			entries = self.transit_matrix[state]

			for c in self.alphabet:
				print("{vid:<{fill}}".format(\
					vid=str(entries[c]), fill=max_id_len) if entries[c] \
						else max_id_len * undefined_symbol, end="|")

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

		if self.initial_state in self.final_states:
			dfa_var.final_states.update({initial_state_name})

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

		for vertex in nfa.transit_matrix:
			if null_symbol in nfa.transit_matrix[vertex]:
				nfa.transit_matrix[vertex].remove(null_symbol)

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

	def concatenate(self, automaton, null_symbol="e"):
		"""
			The concatenation of two automatons:
			- Build a null transition between all first automaton
				final states and the initial state of the second
				automaton.

			- The initial state of the resultant automaton is the
				initial state of the first automaton.

			- The final states of the resultant automaton is the
				final states of the second automaton.
		"""
		unified_transit_mat, unified_alphabet, \
			second_initial_state, second_final_states = \
				self.__buildnewautomaton__(automaton, null_symbol)

		# Add null transitions between first automaton final
		# states and second automaton initial state
		for final_state in self.final_states:
			unified_transit_mat[final_state][null_symbol] = \
				{second_initial_state}

		# Return concatenated automaton
		return Automaton(
			transit_matrix = unified_transit_mat,
			alphabet = unified_alphabet,
			final_states = second_final_states,
			initial_state = self.initial_state)

	def union(self, automaton, initial_state_id="US", 
		final_state_id="UF", null_symbol="e"):

		"""
			The union of two automatons is pretty much
			similar to the concatenation.

			- Build a null transition connecting a new dummy
				initial state to both initial states

			- Build a null transition connecting a new dummy
				final state to all final states of both
				automatons

			- All initial and final states of both automatons
				are downgraded to common states.
		"""

		unified_transit_mat, unified_alphabet, \
			second_initial_state, second_final_states = \
				self.__buildnewautomaton__(automaton, null_symbol)

		initial_state_id = self.__stateidsintegrity__(\
			unified_transit_mat.keys(), initial_state_id)
		final_state_id = self.__stateidsintegrity__(\
			unified_transit_mat.keys(), final_state_id)

		# Create a new dummy initial state and connect
		# it to both initial states of both automatons
		unified_transit_mat[initial_state_id] = {}
		for symbol in unified_alphabet:
			unified_transit_mat[initial_state_id][symbol] = set()
		unified_transit_mat[initial_state_id][null_symbol] = \
			{self.initial_state, second_initial_state}

		# Create a new dummy final state, and connect all previous final
		# states (of both automatons) to this new state via null transition
		for vertex in self.final_states.union(second_final_states):
			unified_transit_mat[vertex][null_symbol].update({final_state_id})
		unified_transit_mat[final_state_id] = {symbol : set() \
			for symbol in unified_alphabet} 

		return Automaton(
			alphabet=unified_alphabet,
			initial_state=initial_state_id,
			final_states={final_state_id},
			transit_matrix=unified_transit_mat)

	def intersection(self, 
		automaton, 
		sink_id="SINK", 
		null_symbol="e", 
		initial_state_id="US", 
		final_state_id="UF"):

		"""
			A intersection of automatons uses the
			DeMorgan's Law:

			intersection(A, B) := !(union(!A, !B))

			Which means that
			
			intersection(Automaton_A, Automaton_B) :=
				complement(
					union(
						complement(Automaton_A), 
						complement(Automaton_B)
					)
				)

			So be it.
		"""
		c_aut_a = self.complement(
			dfa=False, 
			sink_id=sink_id)

		c_aut_b = automaton.complement(
			dfa=False, 
			sink_id=sink_id)

		union_result = c_aut_a.union(c_aut_b, 
			initial_state_id=initial_state_id, 
			final_state_id=final_state_id,
			null_symbol=null_symbol)

		return union_result.complement(
			dfa=False, 
			sink_id=sink_id)

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
			minimal.transit_matrix.remove(node)

		# Step 1: Fill the equivalence matrix
		key_order = list(minimal.transit_matrix.keys())
		transit_mat_len = len(key_order)

		# 1.1: First, fill all trivially equivalent states
		# A trivially equivalent states is such as both
		# states are final or not final simultaneously.
		equivalence_mat = [[[None] \
			for _ in range(transit_mat_len)] \
			for __ in range(transit_mat_len)]

		for row in range(transit_mat_len - 1):
			for col in range(row + 1, transit_mat_len):
				equivalence_mat[col][row] = equivalence_mat[row][col]
				if minimal.__testequivalence__(key_order[row], key_order[col]):
					equivalence_mat[row][col][0] = []

		# 1.2: Then, run a algorithm to find out non-trivial
		# equivalent states
		for row in range(transit_mat_len - 1):
			for col in range(row + 1, transit_mat_len):
				if equivalence_mat[row][col][0] is not None:
					for symbol in minimal.alphabet:
						target_row = key_order.index(\
							minimal.transit_matrix[key_order[row]][symbol])

						target_col = key_order.index(\
							minimal.transit_matrix[key_order[col]][symbol])

						if target_row != target_col:
							if equivalence_mat[target_row][target_col][0] is None:
								# Recursive process of marking all "not equivalent" 
								# memoized pairs
								stack = [{row, col}]
								
								while stack:
									row_k, col_l = stack.pop()

									if equivalence_mat[row_k][col_l][0] is not None:
										for memoized_pairs in equivalence_mat[row_k][col_l][0]:
											stack.append(memoized_pairs)

									equivalence_mat[row_k][col_l][0] = None

								# No need to verify the remaining symbols of the alphabet
								break
							else:
								equivalence_mat[target_row][target_col][0].append({row, col})

		# Step 2: Unify equivalent states. States may be 
		# renamed freely if desired.

		rename_struct = {}
		for row in range(transit_mat_len - 1):
			for col in range(row + 1, transit_mat_len):
				if equivalence_mat[row][col][0] is not None:
					# States are equivalent, aglomerate then into a single one
					new_state_label = key_order[row] + key_order[col]
					rename_struct[key_order[row]] = new_state_label
					rename_struct[key_order[col]] = new_state_label

					minimal.transit_matrix[new_state_label] = {}
					for symbol in minimal.alphabet:
						minimal.transit_matrix[new_state_label][symbol] = \
							minimal.transit_matrix[key_order[row]][symbol]

		# Remove equivalent states from transit_matrix
		for vertex in rename_struct:
			minimal.transit_matrix.pop(vertex)

		# Rename all removed states to the new aglomerated label
		for vertex in minimal.transit_matrix:
			for symbol in minimal.alphabet:
				cur_transit_vertex = minimal.transit_matrix[vertex][symbol]
				if cur_transit_vertex and cur_transit_vertex in rename_struct:
					minimal.transit_matrix[vertex][symbol] = rename_struct[cur_transit_vertex]

		# Don't forget to check the final state list and the initial state
		if minimal.initial_state in rename_struct:
			minimal.initial_state = rename_struct[minimal.initial_state]

		for final_state in copy.copy(minimal.final_states):
			if final_state in rename_struct:
				minimal.final_states.remove(final_state)
				minimal.final_states.update({rename_struct[final_state]})

		# Step 3: Delete states that can't lead to a final
		# state. In this case, more blind search is needed.
		# If no final state is reached, delete state and its
		# transitions.
		non_useful_states = []
		for state in minimal.transit_matrix:
			visited_nodes = minimal.__blindsearch__(state)
			if not visited_nodes.intersection(minimal.final_states):
				non_useful_states.append(state)

		for state in non_useful_states:
			# Remove all transitions associated with that useless state
			for vertex in minimal.transit_matrix:
				for symbol in minimal.alphabet:
					if minimal.transit_matrix[vertex][symbol] == state:
						minimal.transit_matrix[vertex][symbol] = set()

			# Pop state from minimal automaton transition matrix
			minimal.transit_matrix.pop(state)

		# End of minimization, return minimal automaton
		return minimal

	def grammar(self, dfa=False, initial_symbol="S", 
		null_symbol="e", gen_output=False):

		# First, the automaton must be an DFA
		if not dfa:
			dfa_automaton = self.nfae_to_nfa()
			dfa_automaton = dfa_automaton.nfa_to_dfa()
		else:
			dfa_automaton = self.copy()

		urlg_list = OrderedDict()
		urlg_list[initial_symbol] = ["(" + self.initial_state + ")"]

		for state in self.transit_matrix:
			urlg_list[state] = []

			for symbol in self.alphabet:
				if self.transit_matrix[state][symbol]:
					urlg_list[state].append(symbol + \
						"(" + self.transit_matrix[state][symbol] + ")")

			if not urlg_list[state]:
				urlg_list.pop(state)

		for final_state in self.final_states:

			if final_state not in urlg_list:
				urlg_list[final_state] = []

			urlg_list[final_state].append(null_symbol)

		if gen_output:
			print(",".join(self.alphabet), "\n", 
				initial_symbol, sep="")
			for variable in urlg_list:
				for rules in urlg_list[variable]:
					print(variable, "->", rules)

		return urlg_list

	def load_grammar(self, 
		filepath, 
		sep=",", 
		null_symbol="e", 
		final_sink_id="SINK",
		sink_null_transitions=True):

		"""
			The given grammar must be in the type "Unitary Right 
			Linear Grammar" (URLG), which means that only a ma-
			ximum of a single terminal symbol must be given in 
			each rule and all terminal symbols must be strictly 
			in the left of the variables. Example:

			S -> a(A)
			A -> b(A)
			A -> c(B)
			B -> c(A)
			B -> e

			Where {a, b, c} are terminal symbols, {S, A, B} are va-
			riables and "e" is the null transition symbol (a.k.a. 
			lambda).
		"""

		with open(filepath) as f:
			self.alphabet = f.readline().strip().split(sep) + \
				[null_symbol]
			var_list = f.readline().strip().split(sep)
			self.initial_state = f.readline().strip()
			self.final_states = set()

			self.transit_matrix = OrderedDict()
			for var in var_list:
				self.transit_matrix[var] = {symbol : set() \
					for symbol in self.alphabet}

			re_readline = re.compile("""
				\s*(\w+)		# Read right variable identifier
				\s*->			# Read predefined transition symbol
				\s*([^\(\s]+)?		# Read terminal symbol, if any
				\s*(?:\(([^\)\s]+)\))?	# Read transition state, if any
				""", re.IGNORECASE | re.VERBOSE)

			# Sink final state which all empty strings or terminal symbol only
			# rules will point to. If not used in the end, it must be removed.
			self.transit_matrix[final_sink_id] = \
				{symbol : set() for symbol in self.alphabet}

			pop_sink_state = True
			for line in f:
				match = re_readline.search(line)
				if match:
					ascendent, symbol, incident = match.groups()
					if incident is None:
						# If no incident node is given, the transition
						# will be to the additional sink final state
						# artificially created previously
						if symbol == null_symbol and not sink_null_transitions:
							self.final_states.update({ascendent})
						else:
							self.transit_matrix[ascendent][symbol].update({final_sink_id})
							pop_sink_state = False
					else:
						if symbol is not None:
							# If no terminal symbol is given, then 
							# assume it is a null transition
							self.transit_matrix[ascendent][symbol].update({incident})
						else:
							self.transit_matrix[ascendent][null_symbol].update({incident})

			if pop_sink_state:
				self.transit_matrix.remove(final_sink_id)
			else:
				self.final_states.update({final_sink_id})


	def kleene_star(self, 
		start_state_id="KS", 
		end_state_id="KE", 
		null_symbol="e"):

		pass

	def load_regex(self, regex, null_symbol="e"):
		pass

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("""
			Program used to work with Finite Automatons, just for 
			study purposes. This implementation tries to follow 
			stricly the formal definitions from theoretical com-
			puter science and formal languages.""".replace("\t\t\t", ""), 
			"\n-----------------------------------------",
			"\nusage:", sys.argv[0], "<filepath> <operation> [...] [-simpleout]",
			"""
			-----------------------------------------
			Operation list: <operation> can be (case insensitive):

			0. nop: 
				0.0. Description:
				Just load and print the automaton.

			1. convnfa	
				1.0. Extra arguments:
				[null symbol, default is "e"]: Symbol to represent the null
				transition symbol / empty string (also known as "lambda" 
				symbol in theoretical computer science and formal languages).

				1.1. Description:
				Transform a given NFAe (Non-deterministic Finite Automaton 
				with Null Transitions) to NFA (Non-deterministic Finite Au-
				tomaton)

			2. convdfa 
				2.0. Extra arguments:
				[-stateprefix string, default is "DFA"]: Prefix for state na-
				mes of the created DFA automaton.

				2.1. Description:
				Transform a given NFA (Non-deterministic Finite Automaton)
				to DFA (Deterministic Finite Automaton).

			3. grammar 
				3.0. Extra arguments:
				[-nullsymbol symbol, default is "e"]
				[-initialstate variable, default is "S"]: Variable label to
				use as first grammar symbol.

				3.1. Description:
				generate a URLG (Unitary Right Linear Grammar) of a given
				DFA (Deterministic Finite Automaton).

			4. loadgrammar 
				4.0. Extra arguments:
				[-sep separator, default is ","]: separator used in the in-
				put file.
				[-sinknull, enabled by default]: should epsilons transitions
				become transitions to a sink state (if enable)? or should 
				they promote the state correspondent of the variable to a 
				final state instead (if disabled)?

				4.1. Description:
				generate the automaton of the given URLG (Unitary Right Linear
				Grammar).

			5. compl 
				5.0. Extra arguments:
				[-sinkid sink_state_name, default is "SINK"]:

				5.1. Description:
				generate the complementary automaton.

			6. min 
				6.0. Extra arguments:
				[-sinkid sink_state_name, defualt is "SINK"] 
				[-isdfa, disabled by default]:

				6.1. Description:
				minimize the given automaton.

			7. intersec 
				7.0. Mandatory arguments:
				<filepath2>: path of the second automaton to promote a
				intersection.

				7.1. Extra arguments:
				[-sinkid sink_state_name, default is "SINK"]: name of the
				sink state, if necessary, to fullfil the transition matrices.

				7.2 Description:

			8. union

			9. concat

			10. loadregex
			""".replace("\t\t\t", ""))
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

	print("\n-- Unitary Right Linear Grammar --")
	gram = d.grammar(gen_output=True)

	print("\n-- Union --")
	uni = d.union(d)
	uni.print()
	
	print("\n-- Intersection --")
	inter = d.intersection(d)
	inter.print()
	
	print("\n-- Intersection --")
	inter = d.intersection(d)
	inter.print()

	#a=Automaton()
	#a.load_grammar(filepath=sys.argv[1], sink_null_transitions=False)
	#a.print()
