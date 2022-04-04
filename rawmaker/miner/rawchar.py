# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""RawCharacter
============

The concept of `RawItem`s aims to store the full pdf information by
current items to use them for further analysis. This information are
`rawmaker` internal and will be removed before serializing the data.
"""

import contextlib

import iamraw
import pdfminer.layout


class RawChar(iamraw.Char):

    def __init__(self, ltchar: pdfminer.layout.LTChar, **kwargs):
        super().__init__(**kwargs)
        self.ltchar = ltchar


class RawUnicodeChar(iamraw.UnicodeChar):

    def __init__(self, ltchar: pdfminer.layout.LTChar, **kwargs):
        super().__init__(**kwargs)
        self.ltchar = ltchar


def special_char(item: str, fontname: str = None) -> str:
    """\
    >>> special_char('š')
    's'
    >>> special_char('é')
    'e'
    >>> special_char('∗')
    '*'
    """
    if not item:
        return None
    if 27 <= ord(item[0]) <= 128:
        return item
    if fontname and 'LMMath' in fontname:
        with contextlib.suppress(KeyError):
            return SPECIAL_CHARS_LMMath[item]
    with contextlib.suppress(KeyError):
        return SPECIAL_CHARS_TABLE[item]
    return None


def special_chars(text: str) -> str:
    """\
    >>> special_chars('Řůř')
    'Rur'
    >>> special_chars('öäüÖÄÜ')
    'öäüÖÄÜ'
    """
    collected = []
    for char in text:
        converted = special_char(char)
        if converted is None:
            continue
        collected.append(converted)
    result = ''.join(collected)
    return result


def parse_special_chars(table: str) -> dict:
    result = {
        line.split()[0]: line.split()[1]
        for line in table.strip().splitlines()
        if line and not line.strip().startswith('#')
    }
    return result


SPECIAL_CHARS_LMMath = parse_special_chars("""
\u03B1          α        # alpha
\u03B2          β        # beta
# \u2211          −        # minus
\u2206          ∆
\u223c          ∼
\u2212          −        # minus
\u03c0          π
\u03c6          φ
\u03c9          ω
\u25e6          ◦
\u03c4          τ
\u03c1          ρ
\xb7            ·
\xb5            µ
# \u03B1          a        # alpha
# \u03B2          b        # beta
# \u2212          -        # minus
# \u03c0          p
# \u03c6          o
# \u03c9          w
""")

# TODO: REQUIRE BETTER APPROACH OF REPLACING `LEGATURES`
SPECIAL_CHARS_TABLE = parse_special_chars("""
# legiaturen
\uFB00      ff
\uFB01      fi
\uFB02      fl
\uFB03      ffi

\u2217      *        # hcdiss171p9
\x03        *        # hcdiss171p9

\xA8        ¨

# umlaute
\xC4        Ä
\xD6        Ö
\xDC        Ü
\xE4        ä
\xF6        ö
\xFC        ü

\u0161      s       š
\xE9        e       é

\xa1        i       ¡
\xc0        A       À
\xc1        A       Á
\xc2        A       Â
\xc3        A       Ã
# \xc4        A       Ä
\xc5        A       Å
\xc6        A       Æ
\xc7        C       Ç
\xc8        E       È
\xc9        E       É
\xca        E       Ê
\xcb        E       Ë
\xcc        I       Ì
\xcd        I       Í
\xce        I       Î
\xcf        I       Ï
\xd0        D       Ð
\xd1        N       Ñ
\xd2        O       Ò
\xd3        O       Ó
\xd4        O       Ô
\xd5        O       Õ
# \xd6        O       Ö
\xd8        O       Ø
\xd9        U       Ù
\xda        U       Ú
\xdb        U       Û
# \xdc        U       Ü
\xdd        Y       Ý
\xe0        a       à
\xe1        a       á
\xe2        a       â
\xe3        a       ã
# \xe4        a       ä
\xe5        a       å
\xe6        a       æ
\xe7        c       ç
\xe8        e       è
\xe9        e       é
\xea        e       ê
\xeb        e       ë
\xec        l       ì
\xed        l       í
\xee        l       î
\xef        l       ï
\xf0        o       ð
\xf1        n       ñ
\xf2        o       ò
\xf3        o       ó
\xf4        o       ô
\xf5        o       õ
# \xf6        ö       ö
\xf8        o       ø
\xf9        u       ù
\xfa        u       ú
\xfb        u       û
# \xfc        ü       ü
\xfd        y       ý
\xff        y       ÿ
Ř           R
ř           r
ů           u
Ů           U
""")
