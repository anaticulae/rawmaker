# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from iamraw import BoundingBox
from iamraw import Document
from pytest import fixture
from pytest import raises

from rawmaker.features.text import extract_content
from rawmaker.miner.position import DocumentItemHasher
from rawmaker.miner.position import ItemNotFound
from rawmaker.miner.position import dump_hasher
from rawmaker.miner.position import hash_positions
from rawmaker.miner.position import load_hasher
from rawmaker.reader import read
from tests.resource import VIM_GUIDE_PDF

BBox = BoundingBox.from_str  # pylint:disable=invalid-name


@fixture
def sample_hasher() -> DocumentItemHasher:
    hasher = DocumentItemHasher()
    item, position = 'ThisIsJustATest', BBox('10.0 20.0 30.0 40.0')
    hasher.hashitem(item, position)
    return hasher


def test_itemhasher():
    hasher = DocumentItemHasher()
    item, position = 'ThisIsJustATest', BBox('10.0 20.0 30.0 40.0')
    hasher.hashitem(item, position)

    hashed = hasher.position(item)

    assert hashed == position


def test_key_does_not_exists():
    hasher = DocumentItemHasher()

    with raises(ItemNotFound):
        hasher.position('ItemDoesNotExits')


def test_dump_and_load_hasher(sample_hasher):
    sample_hashers = [sample_hasher]
    dumped = dump_hasher(sample_hashers)
    assert len(dumped) > 20
    loaded = load_hasher(dumped)
    assert loaded == sample_hashers


@fixture
def document() -> Document:
    extracted = None
    with read(VIM_GUIDE_PDF) as pdf:
        extracted = extract_content(pdf)
    assert extracted
    return extracted


def test_hash_document(document: Document):
    hashed = hash_positions(document)
    assert len(hashed) == document.page_count
    # sum all the data count of the page hasher
    items = sum([len(item.data) for item in hashed])
    # There are a lot of items in this document
    assert items > 30
