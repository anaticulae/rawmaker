# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila


def dump_wspaces(pages) -> str:

    def dumper(items: list) -> str:
        raw = [utila.from_tuple(item) for item in items]
        return raw

    dumped = serializeraw.dump_pagecontent(pages, pagedumper=dumper)
    return dumped


def load_wspaces(content: str, pages: tuple = None) -> iamraw.PageContents:

    def loader(items: list) -> iamraw.PageContents:
        loaded = [utila.parse_tuple(item) for item in items]
        return loaded

    loaded = serializeraw.load_pagecontent(
        content=content,
        pages=pages,
        pageloader=loader,
    )
    return loaded


def dump_words(pages) -> str:

    def dumper(words: list) -> str:
        result = []
        for word in words:
            word = [rawchar(char) for char in word]
            result.append(word)
        return result

    dumped = serializeraw.dump_pagecontent(pages, pagedumper=dumper)
    return dumped


def load_words(content: str, pages: tuple = None) -> iamraw.PageContents:

    def loader(pages: list) -> iamraw.PageContents:
        loaded = [[fromraw(char) for char in word] for word in pages]
        return loaded

    loaded = serializeraw.load_pagecontent(
        content=content,
        pages=pages,
        pageloader=loader,
    )
    return loaded


def rawchar(item) -> str:
    char = ord(item._text)
    raw = f'{char}|{utila.from_tuple(item.bbox)}|{item.fontsize}|{item.fontname}'
    return raw


def fromraw(item: str) -> tuple:
    text, bounding, fontsize, fontname = item.split('|')
    text = chr(int(text))
    bounding = utila.parse_tuple(bounding)
    fontsize = float(fontsize)
    result = (text, bounding, fontsize, fontname)
    return result
