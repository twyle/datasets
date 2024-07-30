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
from os import path
from .constants import INSTRUCTION


def get_video_descriptions(video_ids: list[str], youtube: YouTube) -> list[str]:
    response: YouTubeListResponse = youtube.find_videos_by_ids(video_ids)
    videos: list[Video] = response.items
    video_descriptions: list[dict[str, str]] = []
    for video in videos:
        video_descriptions.append(dict(video_id=video.id, video_description=video.snippet.description))
    return video_descriptions


def generate_datapoint(timestamps: TimeStamps, video_description: dict[str, str]) -> dict:
    data: dict = dict(
        instruction=INSTRUCTION,
        input=video_description['video_description'],
        output=timestamps.dict()
    )
    return data


def save_timestamps(
    timestamps: list[TimeStamps], 
    video_description: dict[str, str], 
    config: Config
    ) -> None:
    save_path: str = config.out_file
    if not path.exists(save_path):
        with open(save_path, 'w') as f:
            json.dump([], f)
    with open(save_path, 'r') as f:
        all_data: list[dict] = json.load(f)
    data: dict = generate_datapoint(timestamps=timestamps, video_description=video_description)
    all_data.append(data)
    with open(save_path, 'w') as f:
        json.dump(all_data, f, indent=4)


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