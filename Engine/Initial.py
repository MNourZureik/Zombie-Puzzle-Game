import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Engine.Puzzle import Puzzle
from Facts.Bridge import Bridge
from Facts.Goal import Goal
from Utils.PrettyPrint import print_path

en = Puzzle()
en.reset()
en.declare(
    Bridge(
        left=["Me", "Lab Assistant", "Worker", "Scientist"],
        right=[],
        light="left",
        time=0,
        path=[],
    ),
)

print("=========================================================================================================")
en.run()
print("=========================================================================================================")

print(
    "/////////////////////////////////////////////////////////// Goal Paths ///////////////////////////////////////////////////////////"
)
for fact in en.facts.values():
    if isinstance(fact, Goal):
        print_path(path=fact["path"], time=fact["time"])
        print(f"Number Of The Facts In The Search Tree : {len(en.facts)}")
        print(
            f"Number Of Facts That Exceeded The Desired Time : {en.number_of_exceeded_time_states}"
        )
        print(f"Number Of Duplicated Facts States : {en.number_of_duplicated_facts}")
        print(f"Number Of ALL Declared States : {en.number_of_all_states}")

print(
    "///////////////////////////////////////////////////////////End Goal Paths ///////////////////////////////////////////////////////"
)


# en = PuzzleSalience()
# en.reset()
# en.declare(
#     Bridge(
#         left=["Me", "Lab Assistant", "Worker", "Scientist"],
#         right=[],
#         light="left",
#         time=0,
#         path=[],
#     ),
# )

# print(
#     "========================================================================================================="
# )
# en.run()
# print(
#     "========================================================================================================="
# )

# print(
#     "/////////////////////////////////////////////////////////// Goal Paths ///////////////////////////////////////////////////////////"
# )
# for fact in en.facts.values():
#     if isinstance(fact, Goal):
#         print_path(path=fact["path"], time=fact["time"])
#         print(f"Number Of The Facts In The Search Tree : {len(en.facts)}")
#         print(
#             f"Number Of Facts That Exceeded The Desired Time : {en.number_of_exceeded_time_states}"
#         )
#         print(f"Number Of Duplicated Facts States : {en.number_of_duplicated_facts}")
#         print(f"Number Of ALL Declared States : {en.number_of_all_states}")

# print(
#     "///////////////////////////////////////////////////////////End Goal Paths ///////////////////////////////////////////////////////"
# )
