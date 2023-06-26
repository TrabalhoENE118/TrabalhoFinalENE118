#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from .library import Library
from .utilities import Utilities
from .exceptions import InvalidColor


class MetaFore(type):
    """ Overrides AttributeError when __getattr__ called. """
    def __getattr__(cls, color: str):
        raise InvalidColor(f'{InvalidColor.__name__}: {color}')


class Fore(metaclass=MetaFore):

    _utils = Utilities()
    _END: str = Library.END
    _COLORS: dict = Library.COLORS
    _FOREGROUND_256: str = Library.FOREGROUND_256
    _FOREGROUND_RGB: str = Library.FOREGROUND_RGB
    DEFAULT_FOREGROUND_256: str = Library.DEFAULT_FOREGROUND_256
    DEFAULT_FOREGROUND_RGB: str = Library.DEFAULT_FOREGROUND_RGB
    default_foreground_256: str = DEFAULT_FOREGROUND_256
    default_foreground_rgb: str = DEFAULT_FOREGROUND_RGB

    for _color, _code in _COLORS.items():
        vars()[_color] = f'{_FOREGROUND_256}{_code}{_END}'
        vars()[_color.upper()] = f'{_FOREGROUND_256}{_code}{_END}'

    @classmethod
    def rgb(cls, r: int | str, g: int | str, b: int | str) -> str:
        """ Combination with text returns color text.

        Args:
            r: Sets the Red color.
            g: Sets the Green color.
            b: Sets the Blue color.

        Returns:
            str: Foreground RGB code.
        """
        r, g, b = cls._utils.is_percentages((r, g, b))

        pattern: str = f'{cls._FOREGROUND_RGB}{r};{g};{b}{cls._END}'
        if not any((r, g, b)):
            pattern: str = cls.DEFAULT_FOREGROUND_RGB

        return pattern

    @classmethod
    def RGB(cls, r: int | str, g: int | str, b: int | str) -> str:
        """ Combination with text returns color text.

        Args:
            r: Sets the Red color.
            g: Sets the Green color.
            b: Sets the Blue color.

        Returns:
            str: Foreground RGB code.
        """
        return cls.rgb(r, g, b)


class fore(Fore):
    """ This will be deprecated in the future, do not use this for version >= 2.0.0,
        instead please use Fore class (See issue #28). """
    pass
