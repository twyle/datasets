from argparse import Namespace

from .config import Config
# from .docstring_generator import generate_project_docstrings
# from .extensions import function_code_queue, source_code_queue
from .utils import create_application_config, parse_arguments
from .generate_timestamps import generate_timestamps


def main():
    args: Namespace = parse_arguments()
    config: Config = create_application_config(args)
    # print(config.names)
    generate_timestamps(config=config)


if __name__ == '__main__':
    main()