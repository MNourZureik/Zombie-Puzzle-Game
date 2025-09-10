import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import *
from DFSSolver.Facts.Bridge import Bridge
from DFSSolver.Facts.Visited import Visited
from DFSSolver.Facts.Log import Log
from itertools import combinations
from DFSSolver.Facts.StateStack import StateStack


class Puzzle(KnowledgeEngine):

    def __init__(self, find_all_solutions=False):
        super().__init__()
        self.find_all_solutions = find_all_solutions
        self.solutions = []

    @DefFacts()
    def init(self):
        initial_bridge = Bridge(
            left=self.people,
            right=[],
            light="left",
            time=0,
            path=[],
            state_hash=f"{frozenset(self.people)}|{frozenset([])}|left",
            parent_hash=None,
        )
        yield StateStack(stack=[initial_bridge])
        yield Log(**initial_bridge)

    people = ["Lab Assistant", "Scientist", "Me", "Worker"]
    people_time = {
        people[0]: 1,
        people[1]: 2,
        people[2]: 5,
        people[3]: 10,
    }

    def get_best_solution(self):
        def return_none():
            return None

        def return_min():
            return min(self.solutions, key=lambda x: x['time'])

        actions = {
            False: return_none,
            True:  return_min,
        }

        return actions[bool(self.solutions)]()


    # --- GOAL CHECK ---
    @Rule(
        AS.f << StateStack(stack=MATCH.stack),
        TEST(lambda stack: len(stack) > 0 and len(stack[0]["left"]) == 0 and stack[0]["time"] <= 17),
        salience=100,
    )
    def goal_at_top_of_stack(self, f, stack):
        goal_state = stack[0]
        self.solutions.append({"time": goal_state["time"], "path": goal_state["path"]})
        
        def do_halt():
            self.halt()

        def do_modify():
            updated_stack = list(stack)
            updated_stack.pop(0)
            self.modify(f, stack=updated_stack)

        actions = {
            False: do_halt,
            True: do_modify,
        }

        actions[self.find_all_solutions]()


    # --- PRUNING RULES ---
    @Rule(
        AS.f << StateStack(stack=MATCH.stack),
        Visited(state_hash=MATCH.state_hash),
        TEST(lambda stack, state_hash: len(stack) > 0 and list(stack)[0]["state_hash"] == state_hash),
        salience=20 
    )
    def prune_visited_head(self, f, stack):
        """This rule prunes states that have already been visited."""
        current_stack = list(stack)
        current_stack.pop(0)
        self.modify(f, stack=current_stack)

    @Rule(
        AS.f << StateStack(stack=MATCH.stack),
        TEST(lambda stack: len(stack) > 0 and int(list(stack)[0]["time"]) > 17),
        salience=20 
    )
    def prune_time_exceeded_head(self, f, stack):
        """This rule prunes states that exceed the time limit."""
        current_stack = list(stack)
        current_stack.pop(0)
        self.modify(f, stack=current_stack)


    # --- EXPANSION RULE ---
    @Rule(
        AS.f << StateStack(stack=MATCH.stack),
        TEST(
            lambda stack: len(stack) > 0 and len(list(stack)[0]["left"]) > 0
        ),
        salience=10,
    )
    def expand_valid_head(self, f, stack):
        current_stack = list(stack)
        current_bridge = current_stack.pop(0)

        self.declare(Visited(state_hash=current_bridge["state_hash"]))

        new_moves = []

        def light_on_the_left():
            nonlocal new_moves
            new_moves = self._generate_moves_for_left_light(current_bridge)

        def light_on_the_right():
            nonlocal new_moves
            new_moves = self._generate_moves_for_right_light(current_bridge)

        light_actions = {
            "left": light_on_the_left,
            "right": light_on_the_right,
        }
        light_actions.get(current_bridge["light"])()

        for move in new_moves:
            self.declare(Log(**move))
        updated_stack = new_moves + current_stack
        self.modify(f, stack=updated_stack)

    # --- HALT CONDITION ---
    @Rule(
        StateStack(stack=MATCH.stack),
        TEST(lambda stack: len(list(stack)) == 0),
        salience=-100,
    )
    def no_more_states(self):
        self.halt()

    # --- HELPER METHODS ---
    def _generate_moves_for_left_light(self, bridge):
        moves = []
        for p1, p2 in combinations(bridge["left"], 2):
            time_step = max(self.people_time[p1], self.people_time[p2])
            moves.append(self._create_new_bridge_state(bridge, [p1, p2], [], time_step))
        return moves

    def _generate_moves_for_right_light(self, bridge):
        moves = []
        for p in bridge["right"]:
            time_step = self.people_time[p]
            moves.append(self._create_new_bridge_state(bridge, [], [p], time_step))
        return moves

    def _create_new_bridge_state(self, parent, to_right, to_left, time_step):
        new_left = list(parent["left"])
        new_right = list(parent["right"])
        new_path = list(parent["path"])
        new_light = ""

        def set_light_to_left():
            nonlocal new_light
            new_light = "left"

        def set_light_to_right():
            nonlocal new_light
            new_light = "right"

        light_actions = {0: set_light_to_left, 2: set_light_to_right}
        light_actions.get(len(to_right))()

        for p in to_right:
            new_left.remove(p)
            new_right.append(p)
        for p in to_left:
            new_right.remove(p)
            new_left.append(p)

        new_time = parent["time"] + time_step
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

        return Bridge(
            left=new_left,
            right=new_right,
            light=new_light,
            time=new_time,
            path=new_path,
            state_hash=state_hash,
            parent_hash=parent["state_hash"],
        )