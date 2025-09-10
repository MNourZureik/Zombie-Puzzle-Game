import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from BFSSolver.Engine.Puzzle import Puzzle
from BFSSolver.Facts.Bridge import Bridge
from BFSSolver.Facts.CurrentLevel import CurrentLevel
from BFSSolver.Facts.Log import Log
from BFSSolver.Utils.PrettyPrint import print_path, print_search_tree

 
en = Puzzle()
en.reset()

initial_left = ["Me", "Lab Assistant", "Worker", "Scientist"]
initial_right = []
initial_light = "left"
initial_hash = f"{frozenset(initial_left)}|{frozenset(initial_right)}|{initial_light}"

en.declare(
    Bridge(
        left=initial_left,
        right=initial_right,
        light=initial_light,
        time=0,
        path=[],
        level=0,
        state_hash=initial_hash,
        parent_hash=None,
        processed=False
    ),
    CurrentLevel(level=0),
    Log(
        left=initial_left,
        right=initial_right,
        light=initial_light,
        time=0,
        path=[],
        level=0,
        state_hash=initial_hash,
        parent_hash=None,
    )
)

print("=========================================================================================================")
print("Running the puzzle solver to find all possible solutions...")
en.run()
print("Solver has finished.")
print("=========================================================================================================")


print(
    "/////////////////////////////////////////////////////////// Best Solution (BFS-like) //////////////////////////////////////////////////////////"
)
best_solution = en.get_best_solution()

if best_solution:
    print("Found the optimal solution!")
    print_path(path=best_solution["path"], time=best_solution["time"])
    print(f"\n--- Search Statistics ---")
else:
    print("No solution was found within the time limit.")

print(
    "/////////////////////////////////////////////////////////// End Best Solution ///////////////////////////////////////////////////////")

print_search_tree(en.facts)
