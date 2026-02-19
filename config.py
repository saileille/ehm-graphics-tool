"""Configuration for folders and images."""
import copy
import json
import os
from typing import Any

from PIL import Image

from globals import IMAGE_EXTENSIONS, SLASHES
from settings import settings


class ConfigEntry:
    """Configuration for folders and files."""

    def __init__(self, directory: str, filename: str, config: dict[str, Any]):
        """Initialise object."""
        self.directory = directory
        self.filename = filename
        self.extension: str = ""
        self.source = os.path.normpath(os.path.join(directory, filename))
        self.is_folder = filename == ""

        self.ignore: bool | None = None
        if "ignore" in config:
            assert type(config["ignore"]) == bool
            self.ignore = config["ignore"]

        self.override: set[str] = set()
        if "override" in config:
            for path in config["override"]:
                abs_path = os.path.join(settings.graphics_folder, os.path.normpath(path))
                try:
                    assert abs_path in settings.instructions
                except AssertionError:
                    print(abs_path)
                    raise AssertionError
                self.override.add(abs_path)

        self.include: set[str] = set()
        if "include" in config:
            for path in config["include"]:
                abs_path = os.path.join(settings.graphics_folder, os.path.normpath(path))
                assert abs_path in settings.instructions
                self.include.add(abs_path)

        self.exclude: set[str] = set()
        if "exclude" in config:
            for path in config["exclude"]:
                abs_path = os.path.join(settings.graphics_folder, os.path.normpath(path))
                assert abs_path in settings.instructions
                self.exclude.add(abs_path)

        # Between 0.0 and 1.0, indicates where the Y-axis centre of the trimming is.
        # 0.0 -> trim from the bottom, preserving the top
        # 1.0 -> trim from the top, preserving the bottom
        # 0.5 -> trim equally from top and bottom
        self.image_centre_y: float | None = None
        if "image_centre_y" in config:
            assert type(config["image_centre_y"]) == float
            self.image_centre_y = config["image_centre_y"]

        # Between 0.0 and 1.0, indicates where the X-axis centre of the trimming is.
        # 0.0 -> trim from the right, preserving the left
        # 1.0 -> trim from the left, preserving the right
        # 0.5 -> trim equally from left and right
        self.image_centre_x: float | None = None
        if "image_centre_x" in config:
            assert type(config["image_centre_x"]) == float
            self.image_centre_x = config["image_centre_x"]

        self.save_as: str = ""
        if "save_as" in config:
            assert type(config["save_as"]) == str
            self.save_as = config["save_as"]

        self.folder: str | None = None
        if "folder" in config:
            assert type(config["folder"]) == str
            self.folder = config["folder"]

        self.duplicates: set[str] = set()
        if "duplicates" in config:
            self.duplicates = set(config["duplicates"])

        if self.is_folder:
            assert self.save_as == ""
            assert len(self.duplicates) == 0

        if len(self.override) != 0:
            # Override cannot coexist with include and exclude.
            assert len(self.include) + len(self.exclude) == 0
        else:
            # Path cannot be in both include and exclude.
            for path in self.include:
                assert path not in self.exclude

    @staticmethod
    def get_default():
        """Get a default ConfigEntry."""
        config = ConfigEntry("", "", {})
        config.ignore = False
        config.image_centre_y = 0.5
        config.image_centre_x = 0.5
        config.folder = ""

        return config

    @staticmethod
    def create_image_config(img_directory: str, img_name: str, img_extension: str, config_file_dirs: list[str], config_default: ConfigEntry):
        """Create a ConfigEntry for an image."""
        path = os.path.join(img_directory, img_name)
        config = copy.deepcopy(config_default)

        for dir in config_file_dirs:
            if not path.startswith(dir):
                continue

            entries = CONFIG_FILES[dir]
            entries.sort(key=lambda entry: (entry.is_folder, entry.source))

            for entry in entries:
                if (
                    (not entry.is_folder and entry.source != path)
                    or (entry.is_folder and not img_directory.startswith(entry.directory))
                ):
                    continue

                config.overwrite(entry)

        config.directory = img_directory
        config.filename = img_name
        config.extension = img_extension
        config.source = path
        config.is_folder = False

        if config.save_as == "":
            config.save_as = img_name

        if config.folder == "":
            config.folder = os.path.basename(img_directory)

        return config

    def overwrite(self, other: ConfigEntry):
        """Replace contents of this object with another."""
        if other.ignore is not None:
            self.ignore = other.ignore

        if other.image_centre_y is not None:
            self.image_centre_y = other.image_centre_y

        if other.image_centre_x is not None:
            self.image_centre_x = other.image_centre_x

        if other.save_as != "":
            self.save_as = other.save_as

        if other.folder is not None:
            self.folder = other.folder

        self.duplicates = copy.copy(other.duplicates)

        if len(other.override) != 0:
            self.override = copy.copy(other.override)
            return other

        self.override.update(other.include)
        for path in other.exclude:
            self.override.remove(path)

    def process_source_image(self):
        """Process copies of the image and save them to the game's graphics folder."""
        image = Image.open(os.path.join(self.directory, self.filename + self.extension))

        mode = IMAGE_EXTENSIONS[self.extension[1:]]
        if image.mode != mode:
            image = image.convert()

        assert (
            type(self.image_centre_y) == float
            and type(self.image_centre_x) == float
            and type(self.folder) == str
        )

        for path in self.override:
            settings.instructions[path].process_image(copy.copy(image), self.save_as, self.duplicates, self.image_centre_y, self.image_centre_x, self.extension, self.folder)


def process_config_files(directory: str, filename: str):
    """Read the config files and process their information."""
    data = {}
    with open(os.path.join(directory, filename), encoding="utf-8") as file:
        data = json.load(file)

    for source, config in data.items():
        is_folder = source[-1] in SLASHES
        source_dir = os.path.join(directory, os.path.normpath(source))

        # Special case if the source is a dot.
        # Indicates that the configuration applies to this folder.
        if source == ".":
            source_dir = directory
            is_folder = True

        filename = ""
        if not is_folder:
            (source_dir, filename) = os.path.split(source_dir)

        if directory in CONFIG_FILES:
            CONFIG_FILES[directory].append(ConfigEntry(source_dir, filename, config))
        else:
            CONFIG_FILES[directory] = [ConfigEntry(source_dir, filename, config)]


def generate_config_images():
    """Generate a ConfigEntry for every image that is going to be processed."""
    config_default = ConfigEntry.get_default()
    config_file_dirs = sorted(CONFIG_FILES.keys())

    for root, _, files in os.walk(settings.source_folder):
        for file in files:
            (name, extension) = os.path.splitext(file)
            extension = extension.lower()
            if extension[1:] not in IMAGE_EXTENSIONS:
                continue

            config = ConfigEntry.create_image_config(root, name, extension, config_file_dirs, config_default)
            if not config.ignore:
                CONFIG_IMAGES.append(config)


CONFIG_FILES: dict[str, list[ConfigEntry]] = {}
CONFIG_IMAGES: list[ConfigEntry] = []