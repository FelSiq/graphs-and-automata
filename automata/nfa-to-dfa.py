from Automata.automata import Automaton
import sys
import copy

"""
This program converts a Non-Deterministic Finite
Automaton (NFA) to a Deterministic Finite Automaton 
(DFA).
"""

def set_equal(a, b):
	# Verify if both sets are equal
	return len(a - b)==0 and len(b - a)==0

def search_set(mapping, aux):
	for state in mapping:
		if set_equal(mapping[state], aux):
			return state
	return None

def build_dfa(nfa, invalid_symbol="----", state_prefix="DFA"):
	# Init DFA ("Deterministic Finite Automaton")
	dfa = Automaton(
		alphabet=copy.deepcopy(nfa.alphabet),
		transit_matrix={},
		initial_state=None, 
		final_state=set())

	# Initial configuration of the resultant automaton
	initial_state_name = state_prefix + "0"
	dfa.initial_state = initial_state_name
	list_to_proc = [initial_state_name]
	mapping = {initial_state_name : {nfa.initial_state}}

	while len(list_to_proc):
		cur_state = list_to_proc.pop(0)
		dfa.transit_matrix[cur_state] = {}

		for c in dfa.alphabet:
			aux = set()

			for nfa_state in mapping[cur_state]:
				aux.update(nfa.transit_matrix[nfa_state][c])

			if aux:
				if search_set(mapping, aux) is None:
					new_state_name = state_prefix + str(len(mapping))
					mapping[new_state_name] = aux
					list_to_proc.append(new_state_name)
					transit_name = new_state_name
					if nfa.final_state.intersection(aux):
						dfa.final_state.update({transit_name})
				else:
					transit_name = search_set(mapping, aux)
			else:
				transit_name = invalid_symbol

			dfa.transit_matrix[cur_state][c] = transit_name

	return dfa	

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], 
			"<nfa filepath> [output formated (0/1) - default to 0]")
		exit(1)

	try:
		output_formated = int(sys.argv[2])
	except:
		output_formated = False

	nfa = Automaton(sys.argv[1])
	dfa = build_dfa(nfa)

	if not output_formated:
		print("NFA (Non-deterministic Finite Automaton):")
		nfa.print()
		print()

		print("DFA (Deterministic Finite Automaton):")
		dfa.print()
	else:
		dfa.gen_input_file()
