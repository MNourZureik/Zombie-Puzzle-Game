from experta import *

from Facts.Bridge import Bridge


def return_one(person , salience=0):
    def rule_decorator(func):
        return Rule(
            Bridge(
                left=MATCH.left,
                right=MATCH.right,
                light="right",
                time=MATCH.time,
                path=MATCH.path,
            ),
            TEST(lambda right: person in right and len(right) > 1),
            TEST(lambda left: person not in left),
            salience=salience,
        )(func)

    return rule_decorator
