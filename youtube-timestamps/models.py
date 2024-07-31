from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional


class TimeStamp(BaseModel):
    timestamp: str = Field(description="The time stamp")
    title: str = Field(description="The time stamp title")
    

class TimeStamps(BaseModel):
    video_id: str = Field(description="The video id provided")
    time_stamps: Optional[list[TimeStamp]] = Field(description="The list of time stamps", default_factory=list)