import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import Fact, Field


# For checking goal state .
class Goal(Fact):
    path = Field(list, mandatory=True, default=lambda: [])
    time = Field(int, mandatory=True, default=0)

    def print_path(self, time, path):
        print(f"\n✅ Time Estimated : {time} minutes.\n")
        print("Decisions :")
        print("/" * 50)  # Separator for clarity
        print("\n")
        for i, step in enumerate(path, start=1):
            print(f"Decision {i}: {step}")
        print("\n")
        print("/" * 50)
