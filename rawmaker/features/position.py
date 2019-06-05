# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""
Save position of element by object hash
"""

from typing import List

from iamraw import Document
from utila import Flag
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import dump
from yaml import load


def work(document: Document) -> str:
    return ''


class DocumentItemHasher:

    def __init__(self):
        self.data = {}

    def hashitem(self, item, position):
        hashid = hash(item)
        # assert that hashid is not saved before, 'collision %s'  % item
        # TODO: Investigate later, how to avoid collision
        assert hashid not in self.data, 'collision %s' % item
        # while hashid in self.data:
        #     hashid += 1
        self.data[hashid] = position

    def position(self, item):
        hashid = hash(item)
        try:
            current = self.data[hashid]
            return current
        except KeyError:
            raise ItemNotFound('Item is not stored: %s %d' % (item, hashid))

    def __eq__(self, value):
        # TODO: Very slow, improve this
        if value is None:
            return False
        if str(sorted(value.data.keys())) != str(sorted(self.data.keys())):
            return False
        if str(sorted(value.data.values())) != str(sorted(self.data.values())):
            return False
        return True


def load_hasher(content: str) -> DocumentItemHasher:
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)

    result = []
    for page in loaded:
        hasher = DocumentItemHasher()
        for item in page['content']:
            key, position = item.split(maxsplit=1)
            hasher.data[int(key)] = position
        result.append(hasher)
    return result


def dump_hasher(itemhashers):
    result = []
    for index, item in enumerate(itemhashers):
        page = [
            '%s %s' % (key, position) for key, position in item.data.items()
        ]
        result.append({
            'page': index,
            'content': page,
        })
    dumped = dump(result)
    return dumped


def hash_document(document: Document) -> List[DocumentItemHasher]:
    result = []
    for page in document:
        hasher = DocumentItemHasher()
        result.append(hasher)
        for item in page:
            print(item)
    return result


class ItemNotFound(ValueError):
    pass


def commandline():
    return Flag(
        longcut=name(),
        message='Extract position for evey element in document',
    )


def name():
    return 'position'
