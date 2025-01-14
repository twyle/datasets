from .config import Config
from typing import Any, Callable
from .utils import get_youtube_client
from .helpers import get_video_descriptions, parse_video_timestamps_batch, save_timestamps
from youtube import YouTube
from .models import TimeStamps
from langchain_groq import ChatGroq
from langchain.base_language import BaseLanguageModel
from youtube.schemas import (
    SearchFilter, SearchOptionalParameters, SearchPart, YouTubeRequest, YouTubeResponse, 
    YouTubeListResponse
)
from typing import Iterator, Generator
from youtube.models import Search
import itertools


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

def search_for_playlist(playlist_title: str, youtube: YouTube) -> str | None:
    query: str = playlist_title
    max_results: int = 4
    part: SearchPart = SearchPart()
    optional_parameters: SearchOptionalParameters = SearchOptionalParameters(
        q=query,
        maxResults=max_results,
        type=['playlist']
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


def get_playlist_ids(playlist_names: list[str], youtube: YouTube, channel_id: str = None) -> list[str]:
    pass


def get_channel_ids(channel_names: list[str], youtube: YouTube) -> list[str | None]:
    channel_ids: list[str] = []
    for channel_name in channel_names:
        try:
            response: Search = youtube.find_channel_by_name(display_name=channel_name)
        except ValueError as e:
            pass
        else:
            channel_id: str = response.channel_id
            channel_ids.append(channel_id)
    return channel_ids
        


def generate_videos_timestamps(config: Config) -> None:
    print("Generating video timestamps")
    if config.ids:
        video_ids: list[str] = list(config.ids)
    else:
        video_ids: list[str] = get_video_ids(
            video_names=list(config.names), 
            youtube=get_youtube_client(config=config)
        )
    if video_ids:
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
        save_timestamps(timestamps=timestamps, video_descriptions=descriptions, config=config)
        print(timestamps)


def get_playlist_videos(playlist_id: str, youtube: YouTube) -> Generator:
    playlist_items_iterator: Iterator = youtube.get_playlist_items_iterator(
        playlist_id=playlist_id, max_results=25
    )
    for playlist_items in playlist_items_iterator:
        video_ids: list[str] = [video.content_details.video_id for video in playlist_items]
        yield video_ids
    

def generate_playlists_timestamps(config: Config) -> tuple[list[TimeStamps] | None, list[dict[str, str]] | None]:
    print("Generating playlist timestamps")
    if config.ids:
        playlist_ids: list[str] = list(config.ids)
    else:
        playlist_ids: list[str] = get_playlist_ids(
            playlist_names=list(config.names), 
            youtube=get_youtube_client(config=config)
        )
    if not playlist_ids:
        return None, None
    youtube: YouTube = get_youtube_client(config=config)
    all_descriptions: list[list[str]] = []
    all_timestamps: list[list[TimeStamps]] = []
    for playlist_id in playlist_ids:
        for video_ids in get_playlist_videos(playlist_id=playlist_id, youtube=youtube):
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
            all_timestamps.append(timestamps)
            all_descriptions.append(descriptions)
    all_descriptions = list(itertools.chain.from_iterable(all_descriptions))
    all_timestamps = list(itertools.chain.from_iterable(all_timestamps))
    return all_timestamps, all_descriptions


def get_channel_playlists(channel_id: str, youtube: YouTube) -> Generator:
    playlists_iterator: Iterator = youtube.get_playlists_iterator(
        channel_id=channel_id, max_results=25
    )
    for playlists in playlists_iterator:
        playlist_ids: list[str] = [playlist.id for playlist in playlists]
        yield playlist_ids


def generate_channels_timestamps(config: Config) -> tuple[list[TimeStamps] | None, list[dict[str, str]] | None]:
    print("Generating channels timestamps")
    youtube: YouTube = get_youtube_client(config=config)
    if config.ids:
        if config.playlist_ids:
            playlist_ids: list[str] = list(config.playlist_ids)
        elif config.playlist_names:
            playlist_ids: list[str] = get_playlist_ids(
                playlist_names=list(config.playlist_names), 
                youtube=get_youtube_client(config=config),
                channel_id=config.ids[0]
            )
        else:
            print("Getting all the playlists")
            playlist_ids: list[str] = list(get_channel_playlists(channel_id=list(config.ids)[0], youtube=youtube))
    else:
        channel_ids: list[str] = get_channel_ids(
            channel_names=list(config.names), 
            youtube=get_youtube_client(config=config)
        )
        if config.playlist_ids:
            playlist_ids: list[str] = list(config.playlist_ids)
        elif config.playlist_names:
            playlist_ids: list[str] = get_playlist_ids(
                playlist_names=list(config.playlist_names), 
                youtube=get_youtube_client(config=config),
                channel_id=channel_ids[0]
            )
        else:
            print("Getting all the playlists")
            playlist_ids: list[str] = list(get_channel_playlists(channel_id=list(config.ids)[0], youtube=youtube))
    if not playlist_ids:
        return None, None
    playlist_ids = list(itertools.chain.from_iterable(playlist_ids))
    all_descriptions: list[list[str]] = []
    all_timestamps: list[list[TimeStamps]] = []
    for playlist_id in playlist_ids:
        for video_ids in get_playlist_videos(playlist_id=playlist_id, youtube=youtube):
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
            # save_timestamps(timestamps=timestamps, video_description=descriptions, config=config)
            all_timestamps.append(timestamps)
            all_descriptions.append(descriptions)
    all_descriptions = list(itertools.chain.from_iterable(all_descriptions))
    all_timestamps = list(itertools.chain.from_iterable(all_timestamps))
    return all_timestamps, all_descriptions


strategy: dict[str, Callable] = dict(
    videos=generate_videos_timestamps,
    channels=generate_channels_timestamps,
    playlists=generate_playlists_timestamps
)


def generate_timestamps(config: Config) -> None:
    print("Generating the timestamps")
    strategy[config.type](config)