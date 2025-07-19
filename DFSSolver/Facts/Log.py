from experta import Fact, Field
from schema import Or

class Log(Fact):
    
    left = Field(list, mandatory=True, default=lambda: [])
    right = Field(list, mandatory=True, default=lambda: [])
    light = Field(str, mandatory=True, default="")
    time = Field(int, mandatory=True, default=0)
    path = Field(list, mandatory=True, default=lambda: [])
    state_hash = Field(str, mandatory=False)
    parent_hash = Field(Or(str, None), mandatory=False, default=None)
