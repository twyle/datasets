import os
from argparse import ArgumentParser, Namespace
from os import path
from typing import Any
from youtube import YouTube
from .config import Config


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        prog='youtube-timestamps-extractor',
        description='Generate timestamps from youtube videos',
        epilog='Thanks for using %(prog)s! :)',
    )
    parser.add_argument('--secret-file', help='Secrets file path', type=str, required=True)
    parser.add_argument('--GROQ_API_KEY', help="The GROQ API key", type=str, required=True)
    # parser.add_argument(
    #     '--overwrite-function-docstring', nargs='?', default=False, type=bool
    # )
    # parser.add_argument('--directories-ignore', nargs='*', default=[], type=str)
    # parser.add_argument('--files-ignore', nargs='*', default=[], type=str)
    parser.add_argument(
        '--type',
        nargs='?',
        default='videos',
        choices=['videos', 'playlists', 'channels'],
        type=str,
    )
    parser.add_argument('--ids', nargs='*', default=[], type=str)
    parser.add_argument('--names', nargs='*', default=[], type=str)
    args = parser.parse_args()
    if not path.exists(args.secret_file):
        print(f"The secrets file path '{args.secret_file}' does not exist!")
        raise SystemExit(1)
    resource: str = args.type
    if not args.ids and not args.names:
        print(f"You have to provide either ids or names of the {resource}")
        raise SystemExit(1)
    os.environ['GROQ_API_KEY'] = args.GROQ_API_KEY
    # paths: list[str] = args.path
    # for entry in paths:
    #     if not path.exists(entry):
    #         print(f"The target path '{entry}' doesn't exist")
    #         raise SystemExit(1)
    # if args.OPENAI_API_KEY:
    #     os.environ['OPENAI_API_KEY'] = args.OPENAI_API_KEY
    # if not os.environ.get('OPENAI_API_KEY', None):
    #     print('You have not provided the open ai api key.')
    #     raise SystemExit(1)
    return args


def create_application_config(args: Namespace) -> Config:
    config: Config = Config(
        out_file=args.out_file,
        secret_file=args.secret_file,
        type=args.type
    )
    if args.ids:
        config.ids = set(args.ids)
    if args.names:
        config.names = set(args.names)
    return config

def get_youtube_client(config: Config) -> Any:
    client_secrets_file: str = config.secret_file
    youtube = YouTube(client_secret_file=client_secrets_file)
    youtube.authenticate()
    return youtube