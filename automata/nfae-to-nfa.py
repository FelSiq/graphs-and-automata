from Automata.automata import Automaton
import sys
import copy

"""
	This scripts convert a Non-Deterministic Finite
	Automaton with Null Transitiions (NFAe) to a Non-
	Deterministic Finite Automaton.

	There's already a code to convert a NFA to a Det-
	erministic Finite Automaton (DFA) in this same
	repository. You may use they combined with the
	help of the program argument "output formated",
	which prints the output automaton with the for-
	mat of these program inputs.

	--------

	The main strategy to convert a NFAe to a NFA is to
	use the fact that the transition of the state s for
	symbol c in the NFA transition matrix is

	T_NFA(s, c) = T_NFAe_e(T_NFAe(T_NFAe_e(s), c))

	Where
		- T_NFA(x, a) is the transition of a NFA in state "x" for symbol "a"
		- T_NFAe(x, a) is the transition of a NFAe in state "x" for symbol "a"
		- T_NFAe_e(x) is the Null Transition of a NFAe in state "x",
			noting that T_NFAe_e(x) = T*_NFAe(x, e) (extended notation
			for automaton transitions)

	That's the trick. This works because:

	FORMAL EXPLANATION IMPOSSIBLE TO READ:
		With T_e(p) meaning the "Null Transition of state p",
		formally written as

		T_e(p) = T*(p, e) =	{p}, if T_e(p) is undefined
					{p} U T(p, e) U {y in T(p, e)}{T_e(y)}, otherwise.
		where "e" is the empty string.

	Same explanation without symbols:
		The Null Transition of a state "p" is just the state {p},
		if the Null Transition of this same state is undefined (i.e.
		doesn't have a corresponding entry in the transition matrix).

		Otherwise, the Null Transition is a set which always contains
		"p" and all the elements of the Null Transition for "p" in the 
		Transition Matrix AND all the Null Transitions, calculated
		recursively, of all the states in that Null Transition set.

	SIMPLIFIED EXPLANATION for mercy:
		In other worlds, you travel the automaton like a freak, star-
		ting from the state "p" and every state you can ever reach 
		wasting a maximum of a single symbol "c" you put in a sack 
		and call it "Transition of 'p' for symbol 'c'" in the NFA
		transition matrix at position T(p, c).

"""

def get_null_transitions(nfae_t_mat, null_symbol="e"):
	null_transitions = {}

	for state in nfae.transit_matrix:
		# Promote a blind search starting in every possible
		# state of the transition matrix. DFS was choosen 
		# because it uses less memory than the BFS.

		null_transitions[state] = {state}
		active_vertexes = [state]
		predecessor_track = {state : None}

		while active_vertexes:
			cur_vertex = active_vertexes.pop()

			for null_t_vertex in nfae_t_mat[cur_vertex][null_symbol]:
				if null_t_vertex not in predecessor_track:
					predecessor_track[null_t_vertex] = cur_vertex
					active_vertexes.append(null_t_vertex)

					# Each reached state is a null_transition for
					# the current state.
					null_transitions[state].update({null_t_vertex})

	return null_transitions

def build_nfa(nfae, invalid_symbol="----", null_symbol="e"):
	nfa = Automaton(
		alphabet=copy.deepcopy(nfae.alphabet),
		initial_state=nfae.initial_state)

	nfa.alphabet.remove(null_symbol)

	# First, calculate T_e(p) for all states p from NFAe
	null_transitions = get_null_transitions(
		nfae.transit_matrix, 
		null_symbol)

	# Each entry of the NFA transit matrix is in the form
	# T_NFA(p, c) = T_NFAe_e(T_NFAe(T_NFAe_e(p), c))
	for state in nfae.transit_matrix:
		nfa.transit_matrix[state] = {}

		# Check if current state is a NFA final state
		# (by definition if, in the null transitions
		# function, p has at least one final state (i.e.
		# has a non null intersection) of NFAe, then
		# p is a final state of NFA.
		if nfae.final_state.intersection(null_transitions[state]):
			nfa.final_state.update({state})

		for symbol in nfa.alphabet:
			if symbol != null_symbol:
				nfa_state_transit = set()

				# Calculating T_NFAe(<for states>, c)
				for nfae_null_t_state in null_transitions[state]:
					nfa_state_transit.update(\
						nfae.transit_matrix[nfae_null_t_state][symbol])

				# Calculating T_NFAe_e(<for states of prev result)
				aux = set()
				for aux_state in nfa_state_transit:
					aux.update(null_transitions[aux_state])
				nfa_state_transit.update(aux)

				nfa.transit_matrix[state][symbol] = nfa_state_transit

	return nfa

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("usage:", sys.argv[0], 
			"<NFAe filepath> <null symbol>",
			"[output formated (0/1) - default to 0]")
		exit(1)

	try:
		output_formated = int(sys.argv[3])
	except:
		output_formated = False

	nfae = Automaton(sys.argv[1])
	nfa = build_nfa(nfae, null_symbol=sys.argv[2])

	if not output_formated:
		print("NFAe (Non-Deterministic Finite",
			"Automaton with Null Transitions):")
		nfae.print()
		print()

		print("NFA (Non-Deterministic Finite Automaton):")
		nfa.print()
	else:
		nfa.gen_input_file()

