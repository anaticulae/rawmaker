# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Save position of element by object hash"""

import contextlib
import statistics

import iamraw
import utila


class DocumentItemHasher:

    # TODO: REMOVE THIS SENSELESS CLASS?
    def __init__(self, page: int = -1):
        self.data = {}
        self.page = page

    def hashitem(self, item: str, position):
        hashid = hash(item)
        # assert that hashid is not saved before, 'collision %s'  % item
        # TODO: Investigate later, how to avoid collision
        assert hashid not in self.data, 'collision "%s"' % item
        # while hashid in self.data:
        #     hashid += 1
        self.data[hashid] = position

    def position(self, item):
        hashid = hash(item)
        try:
            current = self.data[hashid]
            return current
        except KeyError as error:
            # TODO: CHANGE TO KEY ERROR
            raise ItemNotFound(f'not stored: {item} {hashid}') from error

    def __eq__(self, value):
        return value and (str(self) == str(value))

    def __str__(self):
        result = ['DocumentItemHasher, size: %d' % len(self.data)]
        for key, value in self.data.items():
            result.append('%s %s' % (key, value))
        return utila.NEWLINE.join(result)


def load_hasher(content: str) -> DocumentItemHasher:
    loaded = utila.yaml_from_raw_or_path(content)
    result = []
    for page in loaded:
        pagenumber = int(page['page'])
        hasher = DocumentItemHasher(page=pagenumber)
        for item in page['content']:
            key, position = item.split(maxsplit=1)
            hasher.data[int(key)] = iamraw.BoundingBox.from_str(position)
        result.append(hasher)
    return result


def hash_positions(
    document: iamraw.Document,
    pages=None,
) -> iamraw.PageContentTextPositions:
    assert isinstance(document, iamraw.Document), type(document)
    collected = []
    with utila.SkipCollector(pages) as collector:
        for page in document:
            pagenumber = page.page
            if collector.skip(pagenumber):
                continue
            hasher = DocumentItemHasher(pagenumber)
            collected.append(hasher)
            index = 0
            for item in page:
                try:
                    # TODO: REMOVE?
                    # Not every element has text
                    _ = item.text
                except AttributeError:
                    continue
                # TODO: COMPUTE FOR OTHER LINES THAN ZERO
                mean = mean_height(item.lines[0])
                hasher.hashitem(
                    index,
                    iamraw.TextPosition(bounding=item.box, mean=mean),
                )
                index += 1
    result = []
    for page in collected:
        pagenumber = page.page
        content = dict(page.data)
        result.append(
            iamraw.PageContentTextPosition(
                content=content,
                page=pagenumber,
            ))
    return result


def mean_height(chars):
    height = []
    for char in chars:
        with contextlib.suppress(AttributeError):
            height.append(char.box.y1 - char.box.y0)
    if not height:
        return 0.0
    mean = statistics.mean(height)
    return utila.roundme(mean)


class ItemNotFound(ValueError):
    pass
