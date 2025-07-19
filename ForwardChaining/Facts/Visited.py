import collections
import collections.abc

collections.Mapping = collections.abc.Mapping

from experta import Field , Fact

class Visited(Fact):
    state_hash = Field(str , mandatory=True , default="") 
