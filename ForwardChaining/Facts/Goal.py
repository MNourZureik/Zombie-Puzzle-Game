import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import Fact, Field


class Goal(Fact):
    path = Field(list, mandatory=True, default=lambda: [])
    time = Field(int, mandatory=True, default=0)
