from experta import *

from Facts.Bridge import Bridge


def move_pair(p1, p2):
    def rule_decorator(func):
        return Rule(
            Bridge(
                left=MATCH.left,
                right=MATCH.right,
                light="left",
                time=MATCH.time,
                path=MATCH.path,
            ),
            TEST(lambda left: p1 in left and p2 in left),
            TEST(lambda right: p1 not in right and p2 not in right),
            salience=3
        )(func)

    return rule_decorator
