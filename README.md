OrbisChallenge2014
------------------
My participation in OrbisChallenge 2014 (which ran for a length of a 24-hour period), in which I had to supply a driver in [Tron](http://www.classicgamesarcade.com/game/21670/tron-game.html) to compete with the AI, and potentially to compete against AIs of different strategies.

My approach was to reduce the game to the (commonly known in AI as the) ["search problem"](http://en.wikipedia.org/wiki/Boolean_satisfiability_problem#Algorithms_for_solving_SAT), and applying the minimax rule for minimizing potential loss of outcome of a series of decisions for consecutive moves (within the evaluation threshold, where both players get to move in one direction for each decision frame) for an instance of the game. 

A majority of representing a configuration of Tron had already been implemented in the starter code, but due to the simplicity of the game there is little to no deviation in representations of a configuration of state of a Tron game for optimizing decision procedures.


TODO
====
- Document my approach more throughly, with references to the code
- Fix some bugs in my implementation of minimax
- Determine a favourable heuristic, `h(n)` for [IDA*](http://en.wikipedia.org/wiki/IDA*) graph traversal
- Add [alpha-beta pruning](http://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) to execution of minimax for performance improvement
- Modularize decision rules for the decision procedure so that when the user goes to run the simulation from the command-line, they can choose which set of rules their driver takes for that instance of the game
- Add a *smart* minimax bound whereby a maximum depth is determined at the beginning such that each branch of the search problem is bounded by that depth to satisfy a global time constraint.
- Add efficient bulk loading of multiple simulations
