import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine, Rule, TEST, MATCH, NOT, AS, L, Fact, Field
from DFSSolver.Facts.Bridge import Bridge
from DFSSolver.Facts.Visited import Visited
from DFSSolver.Facts.Log import Log
from itertools import combinations


class StateStack(Fact):
    stack = Field(list, mandatory=True)


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

    @Rule()
    def startup(self):
        initial_bridge = Bridge(
            left=self.people,
            right=[],
            light="left",
            time=0,
            path=[],
            state_hash=f"{frozenset(self.people)}|frozenset([])|left",
            parent_hash=None,
        )
        self.declare(StateStack(stack=[initial_bridge]))
        self.declare(Log(**initial_bridge))

    # --- GOAL CHECK ---
    # This rule has the highest priority. It checks the top of the stack for a goal state.
    @Rule(
        AS.f << StateStack(stack=MATCH.stack),
        TEST(lambda stack: len(stack[0]["left"]) == 0 and stack[0]["time"] <= 17),
        salience=100,
    )
    def goal_at_top_of_stack(self, f, stack):
        goal_state = stack[0]
        self.solution_found = {"time": goal_state["time"], "path": goal_state["path"]}
        self.halt()

    # --- PRUNING RULE ---
    # This rule prunes the top of the stack if it's invalid (time exceeded or already visited).
    @Rule(
        AS.f << StateStack(stack=MATCH.stack & L(lambda l: len(l) > 0)),
        TEST(
            lambda stack, facts: stack[0]["time"] > 17
            or any(
                isinstance(fact, Visited)
                and fact["state_hash"] == stack[0]["state_hash"]
                for fact in facts.values()
            )
        ),
        salience=50,
    )
    def prune_invalid_head(self, f, stack):
        stack.pop(0)
        self.modify(f, stack=stack)

    # --- EXPANSION RULE ---
    # This is the main DFS rule. It fires if the stack head is not a goal and not invalid.
    @Rule(
        AS.f << StateStack(stack=MATCH.stack),
        salience=10,
    )
    def expand_valid_head(self, f, stack):
        current_bridge = list(stack).pop(0)

        self.declare(Visited(state_hash=current_bridge["state_hash"]))
        # self.declare(Log(**current_bridge))

        new_moves = self._generate_moves(current_bridge)
        for move in new_moves:
            self.declare(Log(**move))
        updated_stack = new_moves + list(stack)
        self.modify(f, stack=updated_stack)

    # --- HALT CONDITION ---
    @Rule(StateStack(stack=L(lambda l: len(l) == 0)), salience=-100)
    def no_more_states(self):
        self.halt()

    # --- HELPER METHODS ---
    def _generate_moves(self, bridge):
        moves = []
        light_pos = bridge["light"]

        if light_pos == "left":
            for p1, p2 in combinations(bridge["left"], 2):
                time_step = max(self.people_time[p1], self.people_time[p2])
                moves.append(
                    self._create_new_bridge_state(bridge, [p1, p2], [], time_step)
                )
        else:  # light is right
            for p in bridge["right"]:
                time_step = self.people_time[p]
                moves.append(self._create_new_bridge_state(bridge, [], [p], time_step))
        return moves

    def _create_new_bridge_state(self, parent, to_right, to_left, time_step):
        new_left = list(parent["left"])
        new_right = list(parent["right"])
        new_path = list(parent["path"])
        new_light = "right" if to_right else "left"

        for p in to_right:
            new_left.remove(p)
            new_right.append(p)
        for p in to_left:
            new_right.remove(p)
            new_left.append(p)

        new_time = parent["time"] + time_step
        state_hash = f"{frozenset(new_left)}|{frozenset(new_right)}|{new_light}"

        if to_right:
            new_path.append(f"{to_right[0]} and {to_right[1]} crossed")
        else:
            new_path.append(f"{to_left[0]} returned")

        return Bridge(
            left=new_left,
            right=new_right,
            light=new_light,
            time=new_time,
            path=new_path,
            state_hash=state_hash,
            parent_hash=parent["state_hash"],
        )
