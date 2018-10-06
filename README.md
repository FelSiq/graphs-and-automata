# graphs-and-automata
Some stuff made with Graphs, Theoretical Computer Science tools and Artificial Inteligence. Here you  may find

# Automata directory
## Automata subdirectory
Some code based on theoretical computer science and formal languages research area. Has some Finite Automatons implementations, such as 
- Non-Deterministic Automaton with Null Transitions to Non-Deterministic Finite Automaton conversion 
- Non-Deterministic Finite Automaton to Deterministic Finite Automaton conversion
- Finite Automaton Complementary calculation
- Regex to Finite Automaton
- Finite Automata Concatenation
- Finite Automata Union
- Finite Automata Intersection (using DeMorgan's Law)
- Finite Automaton minimization
- Finite Automaton to Unitary Right Linear Gramatic (URLG)
- Unitary Right Linear Gramatic to Finite Automaton
- Regex simulation

And some more operations. If you're interested in the subject, you should check it out sometime. Theres HUGE usage help text when you try to execute the program without the correct command line arguments, so you're safe to go alone in this adventure. From the usage help system / source code text:

```
Program used to work with Finite Automatons, just for 
study purposes. This implementation tries to follow 
stricly the formal definitions from theoretical com-
puter science and formal languages. 
----------------------------------------- 
usage: automata.py <filepath or regular expression*> <operation> [...] [-simpleout] [-run string] 
(*Regular expression accepted only when <operation>=loadregex, otherwise give always filepath) 
-----------------------------------------
The "-run" parameter can be used to pass a input string to the pro-
duced automaton, in order to check if it accepts or rejects it.
-----------------------------------------
If "-simpleout" is enabled, the produced automaton will be printed
as this program input format, so it can be feed again with another
operation easily.
-----------------------------------------
Operation list: <operation> can be (case insensitive):
(...)
```

Some program output examples:
```
-----------------------------------------
input: python3 automata.py ../test-cases/4.in print
-----------------------------------------
Automaton transition matrix:
* q0 * : |{'q0'}|------|{'q1'}|
  q1   : |------|{'q1'}|{'q2'}|
 [q2]  : |{'q2'}|------|------|

Automaton properties: 
	alphabet: ['a', 'b', 'e'] 
	start state: q0 
	final states: {'q2'}
-----------------------------------------
input: python3 automata.py ../test-cases/5.in print
-----------------------------------------
Automaton transition matrix:
* q0 * : |{'q1'}|------|------|------|
  q1   : |------|------|------|{'q2'}|
  q2   : |------|------|------|{'q5', 'q3'}|
  q3   : |------|{'q4'}|------|------|
  q4   : |------|------|------|{'q5', 'q3'}|
  q5   : |------|------|------|{'q6'}|
  q6   : |------|------|{'q7'}|------|
 [q7]  : |------|------|------|------|

Automaton properties: 
	alphabet: ['o', 'i', '!', 'e'] 
	start state: q0 
	final states: {'q7'}
-----------------------------------------
input : python3 automata.py ../test-cases/7.in convdfa
-----------------------------------------
Automaton transition matrix:
* DFA0 * : |DFA1    |--------|
  DFA1   : |DFA2    |DFA3    |
 [DFA2]  : |DFA2    |DFA3    |
  DFA3   : |DFA4    |DFA3    |
 [DFA4]  : |DFA2    |DFA3    |

Automaton properties: 
	alphabet: ['a', 'b'] 
	start state: DFA0 
	final states: {'DFA4', 'DFA2'}
-----------------------------------------
```

I'm not considering updating that code anymore.

## check-divisibility subdirectory
Given a basis and a input string representing a number with that base, creates a Deterministic Finite Automaton capable of verifying if the given number is or is not a multiple of a given number. Commentary from the source code:

```
	This script generates a transition matrix of a 
	Deterministic Finite Automaton (DFA) that accepts
	only multiples of a given "number" writen in a
	given "base".
	Ex.: 
	- Accepts only numbers multiple of "5" in
	binary (base 2) form.
	- Accepts only numbers multiple of "13" in
	base 16 (hexadecimal).
```

# constraint-satisfaction-problems directory
Some implementations inspired on Artificial Inteligence area. Here you'll find a
- Coloring Maps problem solution using various heuristics, like LCV ("Least Constraining Value"), DH ("Degree Heuristic") and MRV ("Minimum Remaining Value") using Constraint Propagation (Arc Consistency algorithm) + Forward Checking.
- Sudoku solving using MRV ("Minimum Remaining Value") heuristic.
- n-queens problem, solving with Minimum Conflicts Heuristic (but implementation is in python so its slow as fuck, tho).

# basic-graph-search directory
Mainly implementation of some variations of the most classical search algorithms of Computer Science, namely BFS (Breadth-First Search), DFS (Depth-First Search), BS (Beam Search), HC (Hill Climbing), A* (a.k.a. Branch and Bound with admissible heuristic) and BestFS (Best-First Search). The majority of those implementations showcases a bunch of variants of the same algorithm on the same source code, so even if you think you know everything about it, maybe they can deserve a quick check in the name of curiosity.

There's also a very interesting IDA* (Iterative Deepening A*) application, which is a Rubik Cube Solve. I've tried implementing it with pure A*, which is frighteningly fast but, as you may guess, also a memory-eater freak. So, the "solution" I've found in order to fix this is to implement it as IDA*, which is much more slow but does not drown your machine primary memory. Currently, it does solve up to a 15-move configuration in order of a few minutes. I'm out of ideas of how to scale it up to 20 moves, which is a acceptable level of a Rubik Solver Toy Program. In order to compile it, just

```
make
```
and run with
```
./rubik-solver test-cases/0.in
```
Note that my test case is incorporated in the main code because i'm lazy. The input of the program must be a text file with the following format:
```
W,W,W
W,W,W
W,W,W
Y,Y,Y
Y,Y,Y
Y,Y,Y
G,G,G
G,G,G
G,G,G
B,B,B
B,B,B
B,B,B
R,R,R
R,R,R
R,R,R
O,O,O
O,O,O
O,O,O
```
Where all pieces can change it's place (with LEGAL moves, otherwise program will run forever) EXCEPT the centered ones. In other words: the color sequence of the faces (in the solved state) is fixed as follows: W -> Y -> G -> B -> R -> O.
Example output:

```
Start configuration:
      Y O W 
      O W R 
      O W W 
R Y Y G B B O Y R B W B 
W G B O R R B B R W O G 
W G O Y Y G R G G O O G 
      B B Y 
      R Y Y 
      W G R 

Solving...
Result:
      W W W 
      W W W 
      W W W 
G G G R R R B B B O O O 
G G G R R R B B B O O O 
G G G R R R B B B O O O 
      Y Y Y 
      Y Y Y 
      Y Y Y 

Step by step solution:
1	: O <-
2	: O <-
3	: G ->
4	: O ->
5	: R <-
6	: Y <-
7	: Y <-
8	: B <-
9	: R ->
10	: W <-
```

And that's all, for now.
