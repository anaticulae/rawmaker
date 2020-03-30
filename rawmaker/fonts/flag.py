# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import enum
import math


class FontFlag(enum.Enum):
    FixedPitch = 1
    Serif = 2
    Symbolic = 3
    Script = 4
    Nonsymbolic = 6
    Italic = 7
    # font does not contain any upper case letter - this is used for titles etc.
    AllCap = 17
    # contains uppercase and lowercase letters
    SmallCap = 18
    ForceBold = 19


def flags(flag: int) -> tuple:
    """Parse font flag according to adobe pdf specification.

    >>> flags(3)
    (<FontFlag.FixedPitch: 1>, <FontFlag.Serif: 2>)
    >>> flags(70)
    (<FontFlag.Serif: 2>, <FontFlag.Symbolic: 3>, <FontFlag.Italic: 7>)
    >>> flags(35)
    (<FontFlag.FixedPitch: 1>, <FontFlag.Serif: 2>, <FontFlag.Nonsymbolic: 6>)
    >>> flags(262176)
    (<FontFlag.Nonsymbolic: 6>, <FontFlag.ForceBold: 19>)
    """
    assert flag >= 0, f'negative flag {flag}'
    binary = format(flag, 'b')[::-1]  # reverse binary
    result = []
    for key in FontFlag:
        try:
            index = key.value - 1
            value = binary[index]
        except IndexError:
            continue
        else:
            if value == '1':
                result.append(key)
    result = sorted(result, key=lambda x: x.value)
    return tuple(result)


def toflag(items: tuple) -> int:
    """Convert tuple of `FontFlag`s to single flag.

    >>> toflag((FontFlag.Nonsymbolic, FontFlag.ForceBold))
    262176
    """
    result = 0
    for item in items:
        result += math.pow(2, item.value - 1)
    result = int(result)
    return result
