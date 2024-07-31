from .models import TimeStamp, TimeStamps
from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import PromptTemplate
from langchain.base_language import BaseLanguageModel
from .prompts import EXTRACTION_PROMPT_V1
from youtube import YouTube
from youtube.schemas import (
    YouTubeResponse, YouTubeRequest, YouTubeListResponse
)
from youtube.models import Video, PlaylistItem
from .config import Config
import json
from os import path, mkdir
from .constants import INSTRUCTION
from uuid import uuid4


def get_video_descriptions(video_ids: list[str], youtube: YouTube) -> list[str]:
    response: YouTubeListResponse = youtube.find_videos_by_ids(video_ids)
    videos: list[Video] = response.items
    video_descriptions: list[dict[str, str]] = []
    for video in videos:
        video_descriptions.append(dict(video_id=video.id, video_description=video.snippet.description))
    return video_descriptions


def generate_datapoint(timestamps: list[TimeStamps], video_descriptions: list[dict[str, str]]) -> list[dict]:
    datapoints: list[dict] = []
    for timestamp, video_description in zip(timestamps, video_descriptions):
        data: dict = dict(
            instruction=INSTRUCTION,
            input=video_description['video_description'],
            output=timestamp.dict()
        )
        datapoints.append(data)
    return datapoints


def save_timestamps(
    timestamps: list[TimeStamps], 
    video_descriptions: list[dict[str, str]], 
    config: Config
    ) -> None:
    data_dir: str = config.data_dir
    if not path.exists(data_dir):
        mkdir(data_dir)
    file_name: str = f"{str(uuid4())}.json"
    file_path: str = path.join(data_dir, file_name)
    print(timestamps)
    print("==============")
    print(video_descriptions)
    data: dict = generate_datapoint(timestamps=timestamps, video_descriptions=video_descriptions)
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def parse_video_timestamps_batch(
    video_descriptions: list[dict[str, str]], 
    llm: BaseLanguageModel, 
    segment_str: str = EXTRACTION_PROMPT_V1
    ) -> tuple[list[TimeStamps], list[dict[str, str]]]:
    parser = PydanticOutputParser(pydantic_object=TimeStamps)
    template: PromptTemplate = PromptTemplate(template=segment_str, 
                    input_variables=["video_description", "video_id"],
                    partial_variables={"format_instructions": parser.get_format_instructions()}
                                              )
    chain = template | llm | parser
    inputs: list[dict] = [video_description for video_description in video_descriptions]
    timestamps: list[TimeStamps] = chain.batch(inputs)
    return timestamps, video_descriptions