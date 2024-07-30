from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional


class TimeStamp(BaseModel):
    start_time: Optional[str] = Field(description="Start time")
    end_time: Optional[str] = Field(description="End time")
    title: Optional[str] = Field(description="The time stamp title")
    

class TimeStamps(BaseModel):
    video_id: str = Field(description="The video id provided")
    time_stamps: list[TimeStamp] = Field(description="The list of time stamps")