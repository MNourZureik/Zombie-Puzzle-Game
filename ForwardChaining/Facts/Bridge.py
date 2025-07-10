import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import Fact, Field


class Bridge(Fact):
    """

    Summary:
        left: all persons on the left
        right: all persons on the right
        light: the position of the light
        time: time exceeded for now
        path: current path for now

    """

    left = Field(list, mandatory=True, default=lambda: [])
    right = Field(list, mandatory=True, default=lambda: [])
    light = Field(str, mandatory=True, default="")
    time = Field(int, mandatory=True, default=0)
    path = Field(list, mandatory=True, default=lambda: [])
    level = Field(int, mandatory=True, default=0)
