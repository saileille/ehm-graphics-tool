import copy
import json
import os
from typing import Any

from PIL import Image, ImageOps
from config import IMAGE_EXTENSIONS
from globals import SCRIPT_DIRECTORY


class Settings:
    """Basic settings."""

    def __init__(self):
        """Initialise object."""
        settings: dict[str, Any] = {}
        with open(os.path.join(SCRIPT_DIRECTORY, "settings.json")) as file:
            settings = json.load(file)

        assert type(settings["graphics_folder"]) == str
        assert type(settings["source_folder"]) == str

        self.graphics_folder = os.path.normpath(settings["graphics_folder"])
        self.source_folder = os.path.normpath(settings["source_folder"])

        # Create templates.
        templates: dict[str, GraphicsSettings] = {}
        if "templates" in settings:
            for name, template in settings["templates"].items():
                templates[name] = GraphicsSettings("", template, self.source_folder)

        # Create instructions either from templates or directly.
        self.instructions: dict[str, GraphicsSettings] = {}
        for folder, instruction in settings["instructions"].items():
            assert type(folder) == str
            real_folder = os.path.join(self.graphics_folder, os.path.normpath(folder))

            if type(instruction) == str:
                self.instructions[real_folder] = copy.copy(templates[instruction])
                self.instructions[real_folder].folder = real_folder

            elif type(instruction) == dict:
                self.instructions[real_folder] = GraphicsSettings(real_folder, instruction, self.source_folder) # type: ignore

            else:
                print(str(type(instruction))) # type: ignore
                raise SyntaxError


class GraphicsSettings:
    """Settings for a specific game graphics folder."""

    def __init__(self, folder: str, config: dict[str, Any], source_folder: str):
        """Initialise object."""
        assert type(config["width"]) == int
        assert type(config["height"]) == int

        self.folder = folder
        self.total_width = config["width"]
        self.total_height = config["height"]

        self.opacity = 1.0
        if "opacity" in config:
            assert type(config["opacity"]) == float
            self.opacity = config["opacity"]

        self.trim = False
        if "trim" in config:
            assert type(config["trim"]) == bool
            self.trim = config["trim"]

        self.padding_top = 0
        if "padding_top" in config:
            assert type(config["padding_top"]) == int
            self.padding_top = config["padding_top"]

        self.padding_right = 0
        if "padding_right" in config:
            assert type(config["padding_right"]) == int
            self.padding_right = config["padding_right"]

        self.padding_bottom = 0
        if "padding_bottom" in config:
            assert type(config["padding_bottom"]) == int
            self.padding_bottom = config["padding_bottom"]

        self.padding_left = 0
        if "padding_left" in config:
            assert type(config["padding_left"]) == int
            self.padding_left = config["padding_left"]

        self.extension: str | None = None
        if "extension" in config:
            assert type(config["extension"]) == str
            self.extension = f".{config['extension']}".lower()

        self.mask: Mask | None = None
        if "mask" in config:
            source = os.path.join(source_folder, os.path.normpath(config["mask"]["image"]))
            self.mask = Mask(source, config["mask"]["opacity"])

    @property
    def ratio(self):
        """Get the image aspect ratio."""
        return self.real_width / self.real_height

    @property
    def ratio_inverted(self):
        """Get the image aspect ratio as height / width."""
        return self.real_height / self.real_width

    @property
    def real_width(self):
        return self.total_width - self.padding_left - self.padding_right

    @property
    def real_height(self):
        return self.total_height - self.padding_top - self.padding_bottom

    def process_image(self, image: Image.Image, save_as: str, duplicates: set[str], image_centre_y: float, image_centre_x: float, extension: str, folder: str):
        """Process the image according to the settings."""
        image = self.trim_image(image, image_centre_y, image_centre_x)
        image = ImageOps.contain(image, (self.real_width, self.real_height))

        if self.opacity != 1.0:
            transparency = Image.new(image.mode, (image.width, image.height), "#00000000")
            image = Image.blend(transparency, image, self.opacity)

        if self.mask is not None:
            image = self.mask.apply(image)

        image = self.add_padding(image, extension)

        root = self.folder.format(folder=folder)
        try:
            os.makedirs(root)
        except FileExistsError:
            pass

        if self.extension is not None:
            extension = self.extension

        save_locations = copy.copy(duplicates)
        save_locations.add(save_as)

        for name in save_locations:
            image.save(os.path.join(root, name + extension))

    def trim_image(self, image: Image.Image, image_centre_y: float, image_centre_x: float):
        """Trim the image."""
        if self.trim == False:
            return image

        image_ratio = image.width / image.height
        target_ratio = self.ratio

        # No need to do anything.
        if target_ratio == image_ratio:
            return image

        # Turning the image sideways so the same operation works no matter what.
        transposed = False
        centre = image_centre_y
        if target_ratio < image_ratio:
            image = image.transpose(Image.Transpose.ROTATE_90)
            transposed = True
            target_ratio = self.ratio_inverted
            centre = image_centre_x

        # Remove from top and bottom.
        new_height = round(image.width / target_ratio)

        trim = image.height - new_height
        trim_centre = image.height * centre

        # Calculate the top y-axis of the trim.
        # It cannot be smaller than 0.
        # It cannot be larger than the y-axis to be trimmed.
        top_y = min(max(round(trim_centre - (new_height / 2)), 0), trim)

        bottom_y = top_y + new_height

        image = image.crop((0, top_y, image.width, bottom_y))
        if transposed:
            image = image.transpose(Image.Transpose.ROTATE_270)

        return image

    def add_padding(self, image: Image.Image, extension: str):
        """Add padding to the image."""
        if self.real_width == self.total_width and self.real_height == self.total_height:
            return image

        mode = IMAGE_EXTENSIONS[extension[1:]]
        padded_image = None

        if mode == "RGBA":
            padded_image = Image.new(mode, (self.total_width, self.total_height), "#00000000")
        elif mode == "RGB":
            padded_image = Image.new(mode, (self.total_width, self.total_height), "#000000")

        assert type(padded_image) == Image.Image

        padded_image.paste(image, (self.padding_left, self.padding_top))
        return padded_image


class Mask:
    """Mask image and its opacity."""

    def __init__(self, source: str, opacity: float):
        """Initialise object."""
        self.source = source
        self.opacity = opacity
        self.mask = Image.open(self.source)

    def apply(self, image: Image.Image):
        """Apply the mask."""
        return Image.blend(image, self.mask, self.opacity)


settings = Settings()