import os
from argparse import ArgumentParser, Namespace
from os import path
from typing import Any, Callable
from datasets import Dataset
from typing import Generator
import json
from huggingface_hub import whoami    
from urllib3.exceptions import MaxRetryError, SSLError
from ssl import SSLEOFError
from dataset_cards import youtube_card


def upload_youtube_timestamps_dataset(dataset_name: str) -> Dataset:
    ds_path: str = "data/youtube-timestamps"
    def data_generator(data_dir: str = ds_path) -> Generator:
        for file_name in os.listdir(data_dir):
            file_path: str = os.path.join(data_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                timestamps: dict = json.load(f)
                for timestamp in timestamps:
                    yield timestamp
    dataset: Dataset = Dataset.from_generator(data_generator)
    try:
        user: str = whoami()['name']
        repo_id = f'{user}/{dataset_name}'
        dataset.push_to_hub(repo_id)
        youtube_card.push_to_hub(repo_id)
    except Exception as e:
        print(f"There was an error when uploading the dataset: '{e}'")
            
    
strategy: dict[str, Callable] = {
    'youtube-timestamps': upload_youtube_timestamps_dataset
}


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        prog='dataset-uploader',
        description='Uploads datasets to huggingface',
        epilog='Thanks for using %(prog)s! :)',
    )
    parser.add_argument(
        '-d', 
        '--dataset', 
        help='The dataset to upload', 
        type=str, 
        choices=['youtube-timestamps'],
        required=True
        )
    parser.add_argument('--dataset-name', help='The dataset name', type=str, default='youtube-timestamps')
    args = parser.parse_args()
    return args


def main():
    args: Namespace = parse_arguments()
    strategy[args.dataset](dataset_name=args.dataset_name)

if __name__ == '__main__':
    main()