import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Engine.Puzzle import Puzzle
from Facts.Bridge import Bridge


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
