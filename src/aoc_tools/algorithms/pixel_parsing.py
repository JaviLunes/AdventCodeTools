# coding=utf-8
"""Define the PixelParser pixels-to-string conversion tool."""

# Standard library imports:
from collections.abc import Iterable
from pathlib import Path

# Local application imports:
from aoc_tools.manage.puzzle_solving import read_puzzle_input

# Set constants:
DATA_PATH = Path(__file__).parent / "data"


class PixelChar:
    """Group of 4x6 on/off pixels encoding a single string character."""
    def __init__(self, pixels: list[str], on: str = "█", off: str = " "):
        self.pixels = self._encode(pixels=pixels, on=on, off=off)

    def __repr__(self) -> str:
        return str(self.pixels)

    def __eq__(self, other: "PixelChar") -> bool:
        return self.pixels == other.pixels

    def __hash__(self) -> int:
        return hash(self.pixels)

    @staticmethod
    def _encode(pixels: list[str], on: str, off: str) -> str:
        """Transform the lines of string pixels into a 1|0 string number."""
        return "".join(pixels).replace(on, "0").replace(off, "1")


class PixelParser:
    """Tool for converting on/off pixelated images into sets of string characters."""
    def __init__(self, off_pixel: str = ".", on_pixel: str = "#"):
        self.off = off_pixel
        self.on = on_pixel
        self.char_map = self._load_characters_map()

    @staticmethod
    def _load_characters_map() -> dict[PixelChar, str]:
        """Generate a map of PixelChar objects to their represented string characters."""
        lines = read_puzzle_input(input_file=DATA_PATH / "pixel_characters.txt")
        groups = [lines[i:i + 7] for i in range(0, len(lines), 7)]
        return {PixelChar(pixels=g[1:]): g[0].replace("## ", "") for g in groups}

    def process(self, pixel_lines: list[str]) -> str:
        """Transform a 40 x 6 pixels image into an 8-characters string."""
        on, off = self.on, self.off
        self._validate_image(pixel_lines=pixel_lines)
        characters = self._separate_chars(pixel_lines=pixel_lines)
        pixel_chars = [PixelChar(pixels=pixels, on=on, off=off) for pixels in characters]
        return "".join(self.char_map[pixel_char] for pixel_char in pixel_chars)

    def _validate_image(self, pixel_lines: list[str]):
        """Check that the provided image meets the requirements to be processed."""
        assert len(pixel_lines) == 6  # 6-row image.
        assert set("".join(pixel_lines)) == {self.off, self.on}  # Only on/off chars.
        for line in pixel_lines:
            assert len(line) == 8 * 5  # 8 x (four-wide letter + white space) width.
            assert all(line[j] == self.off for j in range(4, 41, 5))  # Char separations.

    @staticmethod
    def _separate_chars(pixel_lines: list[str]) -> Iterable[list[str]]:
        """Slice provided lines of pixels by vertical separators between pixel chars."""
        for j in range(8):
            char_start = j * 5
            char_end = (j + 1) * 5 - 1
            yield [line[char_start:char_end] for line in pixel_lines]
