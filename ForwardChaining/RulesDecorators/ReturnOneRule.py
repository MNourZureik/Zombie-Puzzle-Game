from experta import *

from ForwardChaining.Facts.Bridge import Bridge


def return_one(person):
    def rule_decorator(func):
        return Rule(
            Bridge(
                left=MATCH.left,
                right=MATCH.right,
                light="right",
                time=MATCH.time,
                path=MATCH.path,
                level=MATCH.level,
                state_hash=MATCH.state_hash,
                parent_hash=MATCH.parent_hash,
            ),
            TEST(lambda right: person in right and len(right) > 1),
            TEST(lambda left: person not in left),
            salience=3,
        )(func)

    return rule_decorator
