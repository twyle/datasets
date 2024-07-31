from typing import Optional

from pydantic import BaseModel, Field


class Config(BaseModel):
    data_dir: str = Field(
        description='Where to save the dataset'
    )
    secret_file: str = Field(
        description='The file containing the youtube api oauth details'
    )
    type: str = Field(
        description='The type of resource which could be videos, playlists or channels'
    )
    ids: Optional[set[str]] = Field(description="The video or playlist or channel ids", default_factory=set)
    names: Optional[set[str]] = Field(description="The video or playlist or channel names", default_factory=set)
    temperature: Optional[int] = Field(description="The model temperature", default=0)
    model: Optional[str] = Field(description="The model to use", default="llama3-8b-8192")
    playlist_ids: Optional[set[str]] = Field(description="The playlist ids", default_factory=set)
    playlist_names: Optional[set[str]] = Field(description="The playlist names", default_factory=set)
    
    
    