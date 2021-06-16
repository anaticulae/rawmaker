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
    wspaces = spacestation.serialize.load_wspaces(source, pages=pages)
    document = [wordspace(page) for page in wspaces]
    grouped = document_worddist(document)
    dumped = spacestation.serialize.dump_document_worddist(grouped)
    return dumped


def document_worddist(pages):
    grouped = collections.defaultdict(list)
    for _, content in pages:
        for fontsize, distance in content.items():
            fontsize = utila.roundme(fontsize, digits=2)
            grouped[fontsize].extend(distance)
    result = spacestation.serialize.DocumentWordDist()
    for var, operation in (
        ('mode', statistics.mode),
        ('mean', statistics.mean),
        ('median', statistics.median),
        ('count', len),
    ):
        current = {
            fontsize: utila.roundme(operation(content), digits=3)
            for fontsize, content in grouped.items()
        }
        for fontsize, value in current.items():
            getattr(result, var)[fontsize] = value
    return result


def wordspace(page) -> dict:
    collected = collections.defaultdict(list)
    content = page.content
    for wspace in content:
        fontsize = utila.roundme(wspace[3] - wspace[1], digits=1)
        width = utila.roundme(wspace[2] - wspace[0], digits=2)
        collected[fontsize].append(width)
    collected: dict = dict(collected)
    return page.page, collected
