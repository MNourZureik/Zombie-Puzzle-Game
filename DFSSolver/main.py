import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from DFSSolver.Engine.Puzzle import Puzzle
from DFSSolver.Utils.PrettyPrint import print_path, pretty_search_tree


en = Puzzle()
en.reset()
en.run()

print("=========================================================================================================")
print("Running the puzzle solver to find a solution using DFS...")

print("Solver has finished.")
print("=========================================================================================================")


print(
    "/////////////////////////////////////////////////////////// DFS Solution //////////////////////////////////////////////////////////"
)
best_solution = en.get_best_solution()

if best_solution:
    print("Found a solution!")
    print_path(path=best_solution["path"], time=best_solution["time"])
else:
    print("No solution was found within the time limit.")

print(
    "/////////////////////////////////////////////////////////// End DFS Solution ///////////////////////////////////////////////////////")

pretty_search_tree(en.facts)
