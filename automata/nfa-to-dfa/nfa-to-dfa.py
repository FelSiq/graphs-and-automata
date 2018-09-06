import sys
import re
import copy

"""
This program converts a Non-Deterministic Finite
Automaton (NFA) to a Deterministic Finite Automaton 
(DFA).
"""

def init_automaton(alphabet=None, 
	transit_matrix=None,
	initial_state=None, 
	final_state=None):

	return {
		"alphabet" : alphabet,
		"transit_matrix" : transit_matrix,
		"initial_state": initial_state,
		"final_state" : final_state
	}

def print_automaton(automaton):
	if automaton is None:
		return

	print("Automaton transition matrix:")
	for state in sorted(automaton["transit_matrix"].keys()):
		print(state, end=":\t|")
		
		entries = automaton["transit_matrix"][state]
		for c in automaton["alphabet"]:
			print(entries[c], end="|")
		print()

	print("\nAutomaton properties:",
		"\nalphabet:", automaton["alphabet"],
		"\nstart state:", automaton["initial_state"],
		"\nfinal states:", automaton["final_state"])

def read_automaton(filepath):
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

	# "transit_matrix" is already a formal representation
	# of both the set of automaton possible states and
	# the transition function.
	automaton = init_automaton(
		alphabet=[], 
		transit_matrix={},
		initial_state=None, 
		final_state=set())

	with open(filepath) as f:
		automaton["alphabet"] = f.readline().strip().split(",")
		automaton["initial_state"] = f.readline().strip()

		for line in f:
			new_state = re_get_state.search(line).group(1)
			# Check if state is a final state
			# Notation adopted: [final_state_name]
			# (in input file)
			if re_det_final_state.match(new_state):
				new_state = re_sbrackets.sub("", new_state)
				automaton["final_state"].update({new_state})

			entries = {}
			for symbol, set_str in zip(automaton["alphabet"], re_get_set.findall(line)):
				entries[symbol] = set(set_str.split(","))
				if "" in entries[symbol]:
					entries[symbol].remove("")

			automaton["transit_matrix"][new_state] = entries
			
	return automaton

def set_equal(a, b):
	# Verify if both sets are equal
	return len(a - b)==0 and len(b - a)==0

def search_set(mapping, aux):
	for state in mapping:
		if set_equal(mapping[state], aux):
			return state
	return None

def build_dfa(nfa, invalid_symbol="----", state_prefix="ADF"):
	# Init DFA ("Determinist Finite Automaton")
	dfa = init_automaton(
		alphabet=copy.deepcopy(nfa["alphabet"]),
		transit_matrix={},
		initial_state=None, 
		final_state=set())

	# Initial configuration of the resultant automaton
	initial_state_name = state_prefix + "0"
	dfa["initial_state"] = initial_state_name
	list_to_proc = [initial_state_name]
	mapping = {initial_state_name : {nfa["initial_state"]}}

	while len(list_to_proc):
		cur_state = list_to_proc.pop(0)
		dfa["transit_matrix"][cur_state] = {}

		for c in dfa["alphabet"]:
			aux = set()

			for nfa_state in mapping[cur_state]:
				aux.update(nfa["transit_matrix"][nfa_state][c])

			if aux:
				if search_set(mapping, aux) is None:
					new_state_name = state_prefix + str(len(mapping))
					mapping[new_state_name] = aux
					list_to_proc.append(new_state_name)
					transit_name = new_state_name
					if nfa["final_state"].intersection(aux):
						dfa["final_state"].update({transit_name})
				else:
					transit_name = search_set(mapping, aux)
			else:
				transit_name = invalid_symbol

			dfa["transit_matrix"][cur_state][c] = transit_name

	return dfa	

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], "<nfa filepath> [print nfa (0/1)]")
		exit(1)

	try:
		print_nfa = int(sys.argv[2])
	except:
		print_nfa = True

	nfa = read_automaton(sys.argv[1])

	if print_nfa:
		print("NFA (Non-deterministic Finite Automaton):")
		print_automaton(nfa)
		print()

	dfa = build_dfa(nfa)
	print("DFA (Deterministic Finite Automaton):")
	print_automaton(dfa)
