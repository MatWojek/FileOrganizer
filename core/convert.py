#!/usr/bin/python3

import os
from PIL import Image
import cairosvg

class Convert:
    def __init__(self, source_dir: str, conversion_type: str) -> None:
        self.source_dir = os.path.abspath(source_dir.rstrip("/"))
        self.conversion_type = conversion_type
        self.dest_dir = os.path.join(self.source_dir, f"_{conversion_type}")
        os.makedirs(self.dest_dir, exist_ok=True)

        # Maping conversion types to method
        self.conversion_methods = {
            ".jpg -> .png": self._convert_jpg_to_png,
            ".png -> .jpg": self._convert_png_to_jpg,
            ".png -> .svg": self._convert_png_to_svg,
            ".svg -> .png": self._convert_svg_to_png,
        }

    def convert(self) -> None:
        """Main method to handle conversion based on the type."""
        if self.conversion_type not in self.conversion_methods:
            raise ValueError(f"Unsupported conversion type: {self.conversion_type}")

        conversion_method = self.conversion_methods[self.conversion_type]

        for filename in os.listdir(self.source_dir):
            file_path = os.path.join(self.source_dir, filename)
            if not os.path.isfile(file_path):
                continue

            name, ext = os.path.splitext(filename.lower())
            conversion_method(file_path, name, ext)

    def _convert_jpg_to_png(self, file_path: str, name: str, ext: str) -> None:
        """Convert .jpg to .png."""
        if ext != ".jpg":
            return
        new_file = os.path.join(self.dest_dir, f"{name}.png")
        with Image.open(file_path) as img:
            img.convert("RGB").save(new_file, "PNG")

    def _convert_png_to_jpg(self, file_path: str, name: str, ext: str) -> None:
        """Convert .png to .jpg."""
        if ext != ".png":
            return
        new_file = os.path.join(self.dest_dir, f"{name}.jpg")
        with Image.open(file_path) as img:
            img.convert("RGB").save(new_file, "JPEG")

    def _convert_png_to_svg(self, file_path: str, name: str, ext: str) -> None:
        """Convert .png to .svg."""
        if ext != ".png":
            return
        new_file = os.path.join(self.dest_dir, f"{name}.svg")
        with open(file_path, "rb") as png_file:
            png_data = png_file.read()
            cairosvg.svg2svg(bytestring=png_data, write_to=new_file)

    def _convert_svg_to_png(self, file_path: str, name: str, ext: str) -> None:
        """Convert .svg to .png."""
        if ext != ".svg":
            return
        new_file = os.path.join(self.dest_dir, f"{name}.svg")
        with open(file_path, "rb") as png_file:
            svg_data = png_file.read()
            cairosvg.svg2svg(bytestring=svg_data, write_to=new_file)