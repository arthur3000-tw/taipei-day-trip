from enum import Enum, IntEnum

class TimeEnum(str, Enum):
    morning = "morning"
    afternoon = "afternoon"


class PriceEnum(IntEnum):
    morning = 2000
    afternoon = 2500