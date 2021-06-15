# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import statistics

import utila

import spacestation.serialize


def work(source: str, pages: tuple = None) -> str:
    wordpages = spacestation.serialize.load_words(source, pages=pages)
    document = pages_chardist(wordpages)
    grouped = group_chardist(document)
    dumped = spacestation.serialize.dump_document_chardist(grouped)
    return dumped


def group_chardist(pages):
    """Determine document char dist(mode, mean, median) for multiple pages."""
    grouped = collections.defaultdict(list)
    for _, content in pages:
        for fontsize, distances in content:
            fontsize = utila.roundme(fontsize, digits=2)
            for distance in distances:
                grouped[fontsize].append(distance)
    computed = []
    for operation in (
            statistics.mode,
            statistics.mean,
            statistics.median,
    ):
        computed.append({
            fontsize: utila.roundme(operation(content), digits=3)
            for fontsize, content in grouped.items()
        })
    result = spacestation.serialize.DocumentCharDist()
    for fontsize, value in computed[0].items():
        result.mode[fontsize] = value
    for fontsize, value in computed[1].items():
        result.mean[fontsize] = value
    for fontsize, value in computed[2].items():
        result.median[fontsize] = value
    return result


def pages_chardist(pages):
    """Iterate over pages and determine chardist for every single word."""
    result = []
    for page in pages:
        paged = []
        for word in page.content:
            dist = chardist(word)
            if not dist:
                continue
            paged.append(dist)
        result.append((page.page, paged))
    return result


def chardist(word):
    """Deterine char dist`s for a single word."""
    if not word:
        return None
    if word[-1][0] == ' ':
        # cut last white space char
        word = word[:-1]
    if len(word) <= 2:
        return None
    x1 = word[0][1][2]
    fontsizes = []
    result = []
    for _, bounding, fontsize, _ in word[1:]:
        xdiff = bounding[0] - x1
        result.append(xdiff)
        x1 = bounding[2]
        fontsizes.append(fontsize)
    fontsize = utila.mode(fontsizes)
    result: tuple = utila.roundme(result, digits=5, convert=False)
    return fontsize, result
