from .config import Config
from typing import Any, Callable
from .utils import get_youtube_client
from .helpers import get_video_descriptions, parse_video_timestamps_batch, save_timestamps
from youtube import YouTube
from .models import TimeStamps
from langchain_groq import ChatGroq
from langchain.base_language import BaseLanguageModel
from youtube.schemas import (
    SearchFilter, SearchOptionalParameters, SearchPart, YouTubeRequest, YouTubeResponse
)
from youtube.models import Search


def search_for_video(video_title: str, youtube: YouTube) -> str | None:
    query: str = video_title
    max_results: int = 4
    part: SearchPart = SearchPart()
    optional_parameters: SearchOptionalParameters = SearchOptionalParameters(
        q=query,
        maxResults=max_results,
        type=['video']
    )
    search_request: YouTubeRequest = YouTubeRequest(
        part=part,
        optional_parameters=optional_parameters
    )
    response: YouTubeResponse = youtube.search(search_schema=search_request)
    search_results: list[Search] = response.items
    if not search_results:
        return None
    return search_results[0].resource_id


def get_video_ids(video_names: list[str], youtube: YouTube) -> list[str]:
    video_ids: list[str] = []
    for video_name in video_names:
        video_id: str = search_for_video(video_title=video_name, youtube=youtube)
        if video_id:
            video_ids.append(video_id)
    return video_ids


def generate_videos_timestamps(config: Config) -> tuple[list[TimeStamps] | None, list[dict[str, str]] | None]:
    print("Generating video timestamps")
    if config.ids:
        video_ids: list[str] = list(config.ids)
    else:
        video_ids: list[str] = get_video_ids(
            video_names=list(config.names), 
            youtube=get_youtube_client(config=config)
        )
    if not video_ids:
        return None, None
    descriptions: list[str] = get_video_descriptions(
        video_ids=video_ids, 
        youtube=get_youtube_client(config=config)
    )
    llm: BaseLanguageModel = ChatGroq(
        temperature=config.temperature, 
        model_name=config.model
    )
    timestamps, descriptions = parse_video_timestamps_batch(
        video_descriptions=descriptions,
        llm=llm
    )
    return timestamps, descriptions
    

def generate_playlists_timestamps(config: Config) -> None:
    print("Generating playlist timestamps")

def generate_channels_timestamps(config: Config) -> None:
    print("Generating channels timestamps")


strategy: dict[str, Callable] = dict(
    videos=generate_videos_timestamps,
    channels=generate_channels_timestamps,
    playlists=generate_playlists_timestamps
)


def generate_timestamps(config: Config) -> None:
    print("Generating the timestamps")
    timestamps, descriptions = strategy[config.type](config)
    # if timestamps and descriptions:
        # for timestamp, description in zip(timestamps, descriptions):
        #     save_timestamps(timestamps=timestamp, video_description=description, config=config)