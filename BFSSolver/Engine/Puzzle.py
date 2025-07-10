import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine, Rule, TEST, MATCH, NOT, AS, L
from BFSSolver.Facts.Bridge import Bridge
from BFSSolver.Facts.Visited import Visited
from BFSSolver.Facts.CurrentLevel import CurrentLevel
from BFSSolver.Facts.Log import Log
from itertools import combinations


class Puzzle(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.solution_found = None

    people = ["Me", "Lab Assistant", "Worker", "Scientist"]
    people_time = {
        people[0]: 1,
        people[1]: 2,
        people[2]: 5,
        people[3]: 10,
    }

    def get_best_solution(self):
        return self.solution_found

    # ---------------------
    # CORE BFS LOGIC
    # ---------------------

    # go to the next level :
    @Rule(
        AS.cl << CurrentLevel(level=MATCH.level),
        NOT(Bridge(level=MATCH.level, processed=False)),
        salience=-10,
    )
    def advance_level(self, cl, level):
        self.retract(cl)
        self.declare(CurrentLevel(level=level + 1))

    # Mark the Current Level as Processed :
    @Rule(
        AS.b << Bridge(level=MATCH.level, processed=False),
        CurrentLevel(level=MATCH.level),
        salience=10,
    )
    def mark_as_processed(self, b):
        self.modify(b, processed=True)

    # Clean The Tree From Processed Levels :
    @Rule(AS.b << Bridge(processed=True), salience=-5)
    def cleanup_processed(self, b):
        self.retract(b)

    # ---------------------
    # MOVEMENT RULES
    # ---------------------

    def _generate_moves_for_left_light(self, bridge):
        for p1, p2 in combinations(bridge["left"], 2):
            time_step = max(self.people_time[p1], self.people_time[p2])
            self._declare_new_bridge_state(bridge, [p1, p2], [], time_step)

    def _generate_moves_for_right_light(self, bridge):
        for p in bridge["right"]:
            time_step = self.people_time[p]
            self._declare_new_bridge_state(bridge, [], [p], time_step)

    def _declare_new_bridge_state(self, parent_bridge, to_right, to_left, time_step):
        new_left = list(parent_bridge["left"])
        new_right = list(parent_bridge["right"])
        new_path = list(parent_bridge["path"])
        new_light = ""

        for p in to_right:
            new_left.remove(p)
            new_right.append(p)
        for p in to_left:
            new_right.remove(p)
            new_left.append(p)

        new_time = parent_bridge["time"] + time_step

        def set_light_to_left():
            nonlocal new_light
            new_light = "left"

        def set_light_to_right():
            nonlocal new_light
            new_light = "right"

        light_actions = {0: set_light_to_left, 2: set_light_to_right}
        light_actions.get(len(to_right))()

        state_hash = f"{frozenset(new_left)}|{frozenset(new_right)}|{new_light}"

        def path_to_right():
            new_path.append(f"{to_right[0]} and {to_right[1]} crossed")

        def path_to_left():
            new_path.append(f"{to_left[0]} returned")

        actions = {
            0: path_to_left,
            2: path_to_right,
        }

        actions.get(len(to_right))()

        self.declare(
            Bridge(
                left=new_left,
                right=new_right,
                light=new_light,
                time=new_time,
                path=new_path,
                level=parent_bridge["level"] + 1,
                state_hash=state_hash,
                parent_hash=parent_bridge["state_hash"],
                processed=False,
            )
        )
        self.declare(
            Log(
                left=new_left,
                right=new_right,
                light=new_light,
                time=new_time,
                path=new_path,
                level=parent_bridge["level"] + 1,
                state_hash=state_hash,
                parent_hash=parent_bridge["state_hash"],
            )
        )

    # Expand all possible moves when the light on the left :
    @Rule(
        AS.b
        << Bridge(left=MATCH.left, light=L("left"), level=MATCH.level, processed=True),
        CurrentLevel(level=MATCH.level),
        TEST(lambda b: NOT(Visited(state_hash=b["state_hash"])) and b["time"] <= 17),
        TEST(lambda left: len(left) > 1),
        salience=5,
    )
    def expand_moves_for_left_light(self, b):
        self.declare(Visited(state_hash=b["state_hash"]))
        self._generate_moves_for_left_light(b)

    # Expand all possible moves when the light on the right :
    @Rule(
        AS.b
        << Bridge(
            right=MATCH.right, light=L("right"), level=MATCH.level, processed=True
        ),
        CurrentLevel(level=MATCH.level),
        TEST(
            lambda b: NOT(Visited(state_hash=b["state_hash"]))
            and b["time"] <= 17
        ),
        TEST(lambda right: len(right) > 0),
        salience=5,
    )
    def expand_moves_for_right_light(self, b):
        self.declare(Visited(state_hash=b["state_hash"]))
        self._generate_moves_for_right_light(b)

    # ---------------------
    # GOAL AND DUPLICATE RULES
    # ---------------------

    @Rule(
        AS.b << Bridge(time=MATCH.t, left=MATCH.l),
        TEST(lambda t, l: t > 17 or len(l) == 0),
    )
    def time_exceeded(self, b, t, l):
        self.retract(b)  # Prune this path

    @Rule(
        AS.b << Bridge(time=MATCH.t, left=MATCH.l),
        TEST(lambda t, l: t <= 17 and len(l) == 0),
        salience=10,
    )
    def goal(self, b):
        self.solution_found = {"time": b["time"], "path": b["path"]}
        self.halt()

    @Rule(AS.b << Bridge(state_hash=MATCH.sh), Visited(state_hash=MATCH.sh))
    def prune_duplicates(self, b):
        self.retract(b)
