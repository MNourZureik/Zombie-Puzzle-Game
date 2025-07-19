import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from ForwardChaining.Engine.Puzzle import Puzzle
from ForwardChaining.Facts.Bridge import Bridge
from ForwardChaining.Facts.Goal import Goal
from ForwardChaining.Utils.PrettyPrint import print_path, print_search_tree

initial_left = ["Me", "Lab Assistant", "Worker", "Scientist"]
initial_right = []
initial_light = "left"

en = Puzzle()
en.reset()
en.declare(
    Bridge(
        left=initial_left,
        right=initial_right,
        light="left",
        time=0,
        path=[],
        level=0,
        state_hash=f"{frozenset(initial_left)}|{frozenset(initial_right)}|{initial_light}",
        parent_hash=None,
    ),
)

print(
    "========================================================================================================="
)
en.run()
print(
    "========================================================================================================="
)

print(
    "/////////////////////////////////////////////////////////// Goal Paths ///////////////////////////////////////////////////////////"
)
for fact in en.facts.values():
    if isinstance(fact, Goal):
        print_path(path=fact["path"], time=fact["time"])
        print(
            f"Number Of The Facts In The Search Tree : {len(en.facts) - en.number_of_exceeded_time_states}"
        )
        print(
            f"Number Of Facts That Exceeded The Desired Time : {en.number_of_exceeded_time_states}"
        )
        print(f"Number Of Duplicated Facts States : {en.number_of_duplicated_facts}")
        print(f"Number Of ALL Declared States : {en.number_of_all_states}")

print(
    "///////////////////////////////////////////////////////////End Goal Paths ///////////////////////////////////////////////////////"
)

print_search_tree(en.facts)
