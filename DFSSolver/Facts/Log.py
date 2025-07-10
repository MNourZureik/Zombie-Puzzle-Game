from experta import Fact, Field

class Log(Fact):
    
    left = Field(list, mandatory=True, default=lambda: [])
    right = Field(list, mandatory=True, default=lambda: [])
    light = Field(str, mandatory=True, default="")
    time = Field(int, mandatory=True, default=0)
    path = Field(list, mandatory=True, default=lambda: [])
