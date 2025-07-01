import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine, Rule, TEST, MATCH, NOT, AS
from Facts.Bridge import Bridge
from Facts.Goal import Goal
from Facts.Visited import Visited
from RulesDecorators.MovePairRule import move_pair
from RulesDecorators.ReturnOneRule import return_one
from Utils.PrettyPrint import print_path


class Puzzle(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.number_of_exceeded_time_states = 0
        self.number_of_all_states = 2
        self.number_of_duplicated_facts = 0

    people = ["Me", "Lab Assistant", "Worker", "Scientist"]
    people_time = {
        people[0]: 1,
        people[1]: 2,
        people[2]: 5,
        people[3]: 10,
    }

    def _move_two_persons_to_the_right(
        self, left, right, time, original_path, added_path, person1, person2, time_step
    ):
        new_left = list(left)
        new_right = list(right)
        new_path = list(original_path) + added_path

        new_left.remove(person1)
        new_left.remove(person2)
        new_right.append(person1)
        new_right.append(person2)

        new_time = time + time_step

        self.declare(
            Bridge(
                left=new_left,
                right=new_right,
                light="right",
                time=new_time,
                path=new_path,
            )
        )
        self.number_of_all_states += 1

    def _return_one_person_back(
        self, left, right, original_path, added_path, time, time_step, person_returned
    ):
        new_left = list(left)
        new_right = list(right)

        new_left.append(person_returned)
        new_right.remove(person_returned)

        new_time = time + time_step
        new_path = list(original_path) + added_path

        self.declare(
            Bridge(
                left=new_left,
                right=new_right,
                light="left",
                time=new_time,
                path=new_path,
            )
        )
        self.number_of_all_states += 1

    # ---------------------
    # Move Two Left to Right
    # ---------------------

    # 1. You and Lab Assistant (2 minutes to pass)
    @move_pair(people[0], people[1])
    def move_you_and_lab_assistant(self, left, right, time, path):
        self._move_two_persons_to_the_right(
            left=left,
            right=right,
            time=time,
            time_step=2,
            original_path=path,
            added_path=[f"{self.people[0]} and {self.people[1]} crossed"],
            person1=self.people[0],
            person2=self.people[1],
        )

    # 2. You and Worker (5 minutes to pass)
    @move_pair(people[0], people[2])
    def move_you_and_worker(self, left, right, time, path):
        self._move_two_persons_to_the_right(
            left=left,
            right=right,
            time=time,
            time_step=5,
            original_path=path,
            added_path=[f"{self.people[0]} and {self.people[2]} crossed"],
            person1=self.people[0],
            person2=self.people[2],
        )

    # # 3. You + Scientist (10 minutes)
    @move_pair(people[0], people[3])
    def move_you_and_scientist(self, left, right, time, path):
        self._move_two_persons_to_the_right(
            left=left,
            right=right,
            time=time,
            time_step=10,
            original_path=path,
            added_path=[f"{self.people[0]} and {self.people[3]} crossed"],
            person1=self.people[0],
            person2=self.people[3],
        )

    # # 4. Lab Assistant + Worker (5 minutes)
    @move_pair(people[1], people[2])
    def move_lab_assistant_and_worker(self, left, right, time, path):
        self._move_two_persons_to_the_right(
            left=left,
            right=right,
            time=time,
            time_step=5,
            original_path=path,
            added_path=[f"{self.people[1]} and {self.people[2]} crossed"],
            person1=self.people[1],
            person2=self.people[2],
        )

    # # 5. Lab Assistant + Scientist (10 minutes)
    @move_pair(people[1], people[3])
    def move_lab_assistant_and_scientist(self, left, right, time, path):
        self._move_two_persons_to_the_right(
            left=left,
            right=right,
            time=time,
            time_step=10,
            original_path=path,
            added_path=[f"{self.people[1]} and {self.people[3]} crossed"],
            person1=self.people[1],
            person2=self.people[3],
        )

    # 6. Worker + Scientist (10 minutes)
    @move_pair(people[2], people[3])
    def move_worker_and_scientist(self, left, right, time, path):
        self._move_two_persons_to_the_right(
            left=left,
            right=right,
            time=time,
            time_step=10,
            original_path=path,
            added_path=[f"{self.people[2]} and {self.people[3]} crossed"],
            person1=self.people[2],
            person2=self.people[3],
        )

    # # ---------------------
    # # Return From Right to Left
    # # ---------------------

    # 1. you returned (1 minute)
    @return_one(people[0])
    def return_you(self, left, right, time, path):
        self._return_one_person_back(
            left=left,
            right=right,
            original_path=path,
            added_path=[f"{self.people[0]} returned"],
            time=time,
            time_step=self.people_time[self.people[0]],
            person_returned=self.people[0],
        )

    # 2. lab_assistant returned (2 minute)
    @return_one(people[1])
    def return_lab_assistant(self, left, right, time, path):
        self._return_one_person_back(
            left=left,
            right=right,
            original_path=path,
            added_path=[f"{self.people[1]} returned"],
            time=time,
            time_step=self.people_time[self.people[1]],
            person_returned=self.people[1],
        )

    # 3. worker returned (5 minute)
    @return_one(people[2])
    def return_worker(self, left, right, time, path):
        self._return_one_person_back(
            left=left,
            right=right,
            original_path=path,
            added_path=[f"{self.people[2]} returned"],
            time=time,
            time_step=self.people_time[self.people[2]],
            person_returned=self.people[2],
        )

    # 4. scientist returned (10 minute)
    @return_one(people[3])
    def return_scientist(self, left, right, time, path):
        self._return_one_person_back(
            left=left,
            right=right,
            original_path=path,
            added_path=[f"{self.people[3]} returned"],
            time=time,
            time_step=self.people_time[self.people[3]],
            person_returned=self.people[3],
        )

    # ---------------------
    # Prevent Duplicate States
    # ---------------------
    @Rule(
        Bridge(left=MATCH.left, right=MATCH.right, light=MATCH.light),
        NOT(Visited(state_hash=MATCH.hash_code)),
        salience=2,
    )
    def add_state_to_visited(self, left, right, light):
        hash_code = f"{frozenset(left)}|{frozenset(right)}|{light}"
        self.declare(Visited(state_hash=hash_code))
        self.number_of_all_states += 1

    @Rule(
        AS.bs << Bridge(left=MATCH.left, right=MATCH.right, light=MATCH.light),
        Visited(state_hash=MATCH.hash_code),
        TEST(
            lambda left, right, light, hash_code: (
                f"{frozenset(left)}|{frozenset(right)}|{light}"
            )
            == hash_code
        ),
        salience=1,
    )
    def delete_duplicate_state(self, bs):
        self.number_of_duplicated_facts += 1
        self.retract(bs)

    # ---------------------
    # Time Limit Check
    # ---------------------

    @Rule(
        AS.bs << Bridge(time=MATCH.time, path=MATCH.path),
        TEST(lambda time: time > 17),
        salience=3,
    )
    def time_exceeded(self, bs, path, time):
        print_path(time=time, path=path)
        self.number_of_exceeded_time_states += 1
        self.retract(bs)

    # ---------------------
    # Check Goal State
    # ---------------------
    @Rule(
        Bridge(
            left=MATCH.left,
            right=MATCH.right,
            light="right",
            time=MATCH.time,
            path=MATCH.path,
        ),
        TEST(lambda left: len(left) == 0),
        TEST(lambda time: time <= 17),
        salience=3,
    )
    def goal_reached(self, time, path):
        self.declare(Goal(path=path, time=time))
        self.number_of_all_states += 1
