import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import *
from DFSSolver.Facts.Bridge import Bridge
from DFSSolver.Facts.Visited import Visited
from DFSSolver.Facts.Log import Log
from itertools import combinations


class StateStack(Fact):
    stack = Field(list, mandatory=True)
 