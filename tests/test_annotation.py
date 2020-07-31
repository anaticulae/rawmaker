# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw

import rawmaker.features.annotation
import rawmaker.reader
import tests.resources


def test_annotation_mining_annotations(capsys):
    extracted = None
    with rawmaker.reader.read(power.DOCU13_PDF) as pdf:
        extracted = rawmaker.features.annotation.extract_annotations(pdf)
    assert len(extracted) == tests.resources.VIM_PAGE_COUNT

    # no logging errors from unsupported annotation
    _, err = capsys.readouterr()
    assert not err


@pytest.mark.xfail(reason='annotation is disabled right now')
def test_annotation_work():
    result = rawmaker.features.annotation.work(power.DOCU13_PDF)
    assert len(result) > 200


@pytest.fixture
def vim_guide_annotation():
    extracted = None
    with rawmaker.reader.read(power.DOCU13_PDF) as pdf:
        extracted = rawmaker.features.annotation.extract_annotations(pdf)
    return extracted


def test_annotation_dump_and_load(vim_guide_annotation):  #pylint:disable=W0621
    annotation = vim_guide_annotation
    without_none = [
        item for item in annotation if item.pagelinks or item.hyperlinks
    ]

    dumped = serializeraw.dump_annotations(annotation)
    loaded = serializeraw.load_annotations(dumped)

    assert loaded == without_none
