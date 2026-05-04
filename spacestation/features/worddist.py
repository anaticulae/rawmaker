# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import statistics

import iamraw
import serializeraw
import utilo


def work(source: str, pages: tuple = None) -> str:
    wspaces = serializeraw.load_wspaces(source, pages=pages)
    document = [wordspace(page) for page in wspaces]
    grouped = document_worddist(document)
    dumped = serializeraw.dump_document_worddist(grouped)
    return dumped


def document_worddist(pages):
    grouped = collections.defaultdict(list)
    for _, content in pages:
        for fontsize, distance in content.items():
            fontsize = utilo.roundme(fontsize, digits=2)
            grouped[fontsize].extend(distance)
    result = iamraw.DocumentWordDist()
    for var, operation in (
        ('mode', statistics.mode),
        ('mean', statistics.mean),
        ('median', statistics.median),
        ('count', len),
        ('maxx', max),
        ('minn', min),
    ):
        current = {
            fontsize: utilo.roundme(operation(content), digits=3)
            for fontsize, content in grouped.items()
        }
        for fontsize, value in current.items():
            getattr(result, var)[fontsize] = value
    return result


def wordspace(page) -> dict:
    collected = collections.defaultdict(list)
    for wspace in page.content:
        fontsize = utilo.roundme(wspace[3] - wspace[1], digits=1)
        width = utilo.roundme(wspace[2] - wspace[0], digits=2)
        collected[fontsize].append(width)
    collected: dict = dict(collected)
    return page.page, collected
