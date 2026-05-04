# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import re

import serializeraw
import utilo

PageWhitespace = collections.namedtuple('PageWhitespaces', 'page, content')
PageWhitespaces = list[PageWhitespace]


def determine(path: str, pages: tuple = None) -> PageWhitespaces:
    data = serializeraw.ptn_frompath(
        path,
        pages=pages,
        logging=False,
    )
    analyzed = [analyse_page(item) for item in data]
    result = quality(analyzed)
    return result


INNER_WHITESPACE = r'\b\s{2,}\b'
CONTENT_ENDING = r'\b\n'

COMMON = '(' + INNER_WHITESPACE + '|' + CONTENT_ENDING + ')'


def analyse_page(page) -> PageWhitespace:
    counter = collections.Counter()
    for line in page:
        text = line.text
        for item in re.finditer(COMMON, text):
            counter[len(utilo.extract_match(item))] += 1
    counter[2] += len(page)
    result = PageWhitespace(page=page.page, content=counter.most_common())
    return result


def quality(pages) -> int:
    result = sum([page.content[0][1] for page in pages if page.content], 0)
    return result
