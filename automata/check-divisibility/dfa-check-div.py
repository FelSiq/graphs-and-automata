import sys

"""
	This script generates a transition matrix of a 
	Deterministic Finite Automaton (DFA) that accepts
	only multiples of a given "number" writen in a
	given "base".

	Ex.: 
	- Accepts only numbers multiple of "5" in
	binary (base 2) form.
	- Accepts only numbers multiple of "13" in
	base 16 (hexadecimal).

"""

INVAL_STATE_SYM = "-"

# I'm only giving support up to base 16, but this alphabet can
# easily be upgraded with a little patience
BASE_SYMBOLS = [str(i) for i in range(10)] + ["A", "B", "C", "D", "E", "F"]

# Form of a State identifier
def state_form(number):
	return "S" + str(number)

# Conver a number to any base up to 16
def conv_to_base(number, base):
	if number == 0:
		return "0"
	new_num = ""
	while number:
		new_num = BASE_SYMBOLS[number % base] + new_num
		number //= base
	return new_num

# Generate the transition matrix of the Deterministic Finite Automaton (DFA)
def gen_transition_matrix(number, base=2):
	# Create a empty transition matrix with
	# "number" lines by "base" (0, 1, ...) symbols of the
	# "base" alphabet (ex.: base 2 has alphabet {0, 1})
	transition_mat = dict()
	for i in range(number):
		transition_mat[state_form(i)] = [INVAL_STATE_SYM] * base

	for i in range(number * base + 1):
		next_state = i % number
		cur_state = state_form(0)

		for c in conv_to_base(i, base):
			c_num = int(c, base=base)
			aux = transition_mat[cur_state][c_num]

			if aux == INVAL_STATE_SYM:
				transition_mat[cur_state][c_num] = state_form(next_state)
				aux = state_form(next_state)

			cur_state = aux

	return transition_mat

def test(cases, mat, num, base):
	n = len(cases)
	ans = [True] * n
	
	for i in range(n):
		cur_state = state_form(0)

		for c in cases[i]:
			cur_state = mat[cur_state][int(c, base=base)]

		if cur_state != state_form(0):
			ans[i] = False 

	return ans

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("usage:", sys.argv[0], "<number> [base] [test cases comma separated]")
		exit(1)

	try:
		base = int(sys.argv[2])
	except:
		base = 2

	number = int(sys.argv[1])

	transition_mat = gen_transition_matrix(number, base)

	for state in sorted(transition_mat.keys(), key=lambda k: int(k[1:])):
		print(state, "\t:", transition_mat[state])

	try:
		if len(sys.argv) >= 4:
			test_cases = sys.argv[3].split(",")
			ans = test(test_cases, transition_mat, number, base)

			print("Test cases:")
			for test, res in zip(test_cases, ans):
				print(test, ":", res)

	except Exception as e:
		print(e)

