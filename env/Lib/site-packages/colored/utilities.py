#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from .exceptions import InvalidStyle, InvalidColor, InvalidHexColor
from .library import Library


class Utilities:

    def __init__(self):
        self._COLORS: dict = Library.COLORS
        self._HEX_COLORS: dict = Library.HEX_COLORS
        self._STYLES: dict = Library.STYLES

    def is_color_exist(self, name: str) -> bool:
        """ Checks for valid color by name or by hex style name or number,
            and raise a InvalidColor or InvalidHexColor exception if it doesn't exist.

        Args:
            name: Sets the name of the style or the number.

        Returns:
              bool: True if exist.
        """
        if name.startswith('#'):
            if name not in self._HEX_COLORS.values():
                raise InvalidColor(f'{InvalidHexColor.__name__}: {name}')

        elif name not in self._COLORS.keys() and name not in self._COLORS.values():
            raise InvalidColor(f'{InvalidColor.__name__}: {name}')

        return True

    def is_style_exist(self, name: str) -> bool:
        """ Checks for valid style and raise a InvalidStyle exception
            if it doesn't exist.

        Args:
            name: Sets the name of the style or the number.

        Returns:
              bool: True if exist.
        """
        if name not in self._STYLES.keys() and name not in self._STYLES.values():
            raise InvalidStyle(f'{InvalidStyle.__name__}: {name}')

        return True

    @staticmethod
    def convert_percentages(percent: str | int) -> int | str:
        """ Convert percentages to color number with range 0-255:

        Args:
            percent: Sets the percent number.

        Returns:
            int | str: Returns the number of the range 0-255.
        """
        percentages = {}
        for number in range(256):
            percentage = int((number / 255) * 100)
            percentages[f'{percentage}%'] = number
        try:
            per = percentages[percent]
        except KeyError:
            per = percent[:-1]

        return per

    def is_percentages(self, numbers: tuple) -> list:
        """ Checks a tuple of numbers and convert a percentage number
        to RGB color number.

        Args:
            numbers: Sets percentages of numbers.

        Returns:
            list: List with RGB numbers.
        """
        rgb_list = []
        for num in numbers:
            if str(num).endswith('%'):
                rgb_list.append(self.convert_percentages(str(num)))
            else:
                rgb_list.append(num)
        return rgb_list
