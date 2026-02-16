"""Automatic saving of all files or something."""
import os
import sys
import traceback
from types import TracebackType


def show_exception_and_exit(exc_type: type[BaseException], exc_value: BaseException, tb: TracebackType):
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)


sys.excepthook = show_exception_and_exit


from globals import CONFIG_NAME
from config import CONFIG_IMAGES, generate_config_images, process_config_files
from settings import settings


def load_configs():
    """Find and load all configuration files in the source folder."""
    for root, _, _ in os.walk(settings.source_folder):
        if os.path.exists(os.path.join(root, CONFIG_NAME)):
            process_config_files(root, CONFIG_NAME)


def main():
    """The main function."""
    load_configs()
    generate_config_images()

    for config in CONFIG_IMAGES:
        config.process_image()

if __name__ == "__main__":
    main()
    input("Done")