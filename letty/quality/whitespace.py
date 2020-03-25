# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import re
import typing

import serializeraw
import utila

PageWhitespace = collections.namedtuple('PageWhitespaces', 'page, content')
PageWhitespaces = typing.List[PageWhitespace]


def determine(path: str, pages: tuple = None) -> PageWhitespaces:
    data = serializeraw.create_pagetextnavigators_frompath(path, pages=pages)
    result = []
    for item in data:
        extracted = analyse_page(item)
        result.append(extracted)
    return result


INNER_WHITESPACE = r'\b\s{2,}\b'
CONTENT_ENDING = r'\b\n'

COMMON = '(' + INNER_WHITESPACE + '|' + CONTENT_ENDING + ')'


def analyse_page(page) -> PageWhitespace:
    counter = collections.Counter()
    for line in page:
        text = line.text
        for item in re.finditer(COMMON, text):
            counter[len(utila.extract_match(item))] += 1
    result = PageWhitespace(page=page.page, content=counter.most_common())
    return result
