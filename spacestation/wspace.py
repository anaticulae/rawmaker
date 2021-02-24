# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import rawmaker.features
import rawmaker.miner.char
import rawmaker.reader


def extract(document: str, pages: tuple = None):
    with rawmaker.reader.read(document) as pdf:
        document = rawmaker.features.extract_content(
            pdf,
            converter=rawmaker.miner.char.CharPDFConvert,
            strip=True,
            pages=pages,
        )
    result = []
    for page in document:
        if utila.should_skip(page.page, pages):
            continue
        extracted = extract_page(page)
        result.append(iamraw.PageContent(page=page.page, content=extracted))
    return result


MAXDIFF = configo.HolyTable(
    items=[
        (7.0, 2.0),
        (10.0, 2.0),
        (15.0, 3.0),
        (20.0, 4.0),
        (25.0, 5.0),
    ],
    right_outranges_none=False,
    left_outranges_none=False,
)


def diffme(fontsize: float) -> tuple:
    # assert 4.0 <= fontsize <= 100, str(fontsize)
    # xdiff, ydiff
    xdiff = MAXDIFF(fontsize)
    return (xdiff, 10.0)


def extract_page(chars: list, maxdiff: callable = diffme) -> list:
    if not chars:
        return []
    result = []
    chars = sameline(chars)
    last = chars[0].bbox
    for char in chars[1:]:
        text = char._text  # pylint:disable=W0212
        bbox = char.bbox
        if text == ' ':
            continue
        xdiff_max, ydiff_max = maxdiff(char.fontsize)
        # x0, y0, x1, y1
        xdiff = last[2] - bbox[0]
        ydiff = last[3] - bbox[3]
        # rectangle between
        if abs(ydiff) > ydiff_max:
            # new line
            last = char
            continue
        if abs(xdiff) > xdiff_max:
            # new word
            # x0, y0, x1, y1
            bounding = iamraw.BoundingBox(
                min(last[2], bbox[0]),
                min(last[1], bbox[1]),
                max(last[2], bbox[0]),
                max(last[3], bbox[3]),
            )
            result.append(bounding)
            last = char
            continue
        last = char.bbox
    return result


def sameline(
        chars,
        diff_max=10.0,  # TODO: HOLY VALUE
):
    # sort by x0
    chars = sorted(chars, key=lambda x: x.bbox[0])
    # sort by y0
    chars = sorted(chars, key=lambda x: x.bbox[3])

    clusterd = utila.same_line_cluster(
        chars,
        min_elements=1,
        max_diff=diff_max,
        matcher=lambda x: x.bbox[3],
    )
    # sort top down
    # TODO: REMOVE AFTR HAVING STABLE LINE CLUSTER
    clusterd = sorted(clusterd, key=lambda x: x.center.bbox[3])
    result = [sorted(line, key=lambda x: x.bbox[0]) for line in clusterd]
    result = utila.flatten(result)
    return result
