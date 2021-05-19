# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import utila

import rawmaker.text.chars
import rawmaker.text.data

MAX_DIFF = configo.HolyTable(
    items=[
        (6, 1.0),
        (12, 1.0),
        (16, 1.0),
        (22, 10.0),
        (24, 10.0),
        (48, 15.0),
    ],
    left_outranges_none=False,
    right_outranges_none=False,
)


def parses(
    source: str,
    pages: tuple,
    word_length_min: int = 1,
    difftable: configo.HolyTable = MAX_DIFF,
) -> rawmaker.text.data.WordBoxPages:
    extracted = rawmaker.text.chars.extract_chars(source, pages)
    pages = [
        extract_page(
            page,
            word_length_min=word_length_min,
            difftable=difftable,
        ) for page in extracted
    ]
    boundings = [wordbox_boundings(page) for page in pages]

    # adjust page numbers
    for page, bounding in zip(extracted, boundings):
        bounding.page = page.page
    return boundings


def extract_page(
    page,
    word_length_min: int = 1,
    difftable: configo.HolyTable = MAX_DIFF,
) -> rawmaker.text.data.PageLines:
    # remove white space
    page = [item for item in page if item.get_text().strip()]

    lines = utila.same_line_cluster(
        page,
        min_elements=word_length_min,  # support single chars
        matcher=lambda x: x.bbox[3],
    )
    # ensure top bottom
    lines = sorted(lines, key=lambda bounding: bounding.center[3])  # y1

    result = []
    for line in lines:
        # ensure left right
        line = sorted(line, key=lambda x: x[0])  # x0
        merged = merge_line(line, difftable=difftable)
        result.append(merged)
    return rawmaker.text.data.PageLines(lines=result)


def merge_line(line, difftable: configo.HolyTable):
    if not line:
        return []
    diffs = [
        after[0] - current[2] for current, after in zip(line[0:-1], line[1:])
    ]
    result = [[line[0]]]
    for char, diff in zip(line[1:], diffs):
        if diff > difftable(char.fontsize):
            result.append([char])
        else:
            result[-1].append(char)
    return result


def wordbox_boundings(page) -> rawmaker.text.data.WordBoxPage:
    result = []
    for line in page:
        for word in line:
            bounding = utila.rectangle_max([char.bbox for char in word])
            result.append(bounding)
    wordbox = rawmaker.text.data.WordBoxPage(content=result)
    return wordbox
