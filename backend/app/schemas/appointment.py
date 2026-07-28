from pydantic import BaseModel
from datetime import date, time
from typing import List


class TimeSlot(BaseModel):
    time: str        
    available: bool  


class AvailabilityResponse(BaseModel):
    date: date
    slots: List[TimeSlot]